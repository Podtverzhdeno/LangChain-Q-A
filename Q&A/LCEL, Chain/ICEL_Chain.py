# Что такое LCEL и зачем он нужен?

LCEL — это не просто синтаксический сахар
Под капотом `|` создаёт объект `RunnableSequence` = каждый компонент передаёт свой output как input следующему
При этом автоматически работает стриминг, async, batch и логирование через LangSmith = без дополнительного кода


#Что такое Runnable и какие методы у него есть?

Runnable - это базовый интерфейс (абстрактный класс) который реализуют все компоненты LangChain.
Промпт - Runnable, модель - Runnable, парсер - Runnable, ретривер - Runnable.
Именно поэтому их можно соединять через |
    Три метода которые есть у каждого Runnable:
        runnable.invoke(input)           # один запрос
        runnable.stream(input)           # стриминг
        runnable.batch([input1, input2]) # параллельно
Виды Runnable которые нужно знать:
    RunnableSequence    # цепочка через |
    RunnableParallel    # параллельное выполнение нескольких цепочек
    RunnablePassthrough # пропускает input без изменений
    RunnableLambda      # оборачивает обычную Python-функцию в Runnable


# Чем invoke отличается от stream и batch?

invoke - один запрос, ждёт полного ответа
stream - один запрос, возвращает генератор токен за токеном (UX как в ChatGPT)
batch - несколько запросов параллельно, возвращает список ответов

chain.invoke({"topic": "RAG"})                              # → str
for chunk in chain.stream({"topic": "RAG"}):               # → генератор
    print(chunk, end="")
chain.batch([{"topic": "RAG"}, {"topic": "LangGraph"}])    # → [str, str]


# Как работает оператор | под капотом?

Создаёт RunnableSequence. Output левого компонента становится input правого — типы должны совпадать
chain = prompt | llm | StrOutputParser()
# prompt:          dict → ChatPromptValue
# llm:             ChatPromptValue → AIMessage
# StrOutputParser: AIMessage → str
Поэтому порядок критичен — не просто слева направо, а каждый компонент должен уметь принять то что вернул предыдущий


# Что такое RunnableParallel и когда использовать?

RunnableParallel запускает несколько цепочек параллельно на одном и том же input, возвращает словарь результатов

from langchain_core.runnables import RunnableParallel, RunnablePassthrough

chain = RunnableParallel({
    "context": retriever,           # ищет документы
    "question": RunnablePassthrough() # пропускает вопрос без изменений
}) | prompt | llm | StrOutputParser()

chain.invoke("Как оформить отпуск?")
# retriever и RunnablePassthrough работают параллельно
# prompt получает: {"context": [docs...], "question": "Как оформить отпуск?"}

Когда использовать: классический RAG - нужно одновременно получить и контекст из БД, и сохранить исходный вопрос для промпта


# Что такое RunnableLambda?

RunnableLambda - обёртка которая превращает любую Python-функцию в Runnable, чтобы её можно было встроить в LCEL цепочку через |
from langchain_core.runnables import RunnableLambda

# Обычная функция → Runnable
def format_docs(docs):
    return "\n".join([doc.page_content for doc in docs])

chain = retriever | RunnableLambda(format_docs) | prompt | llm | StrOutputParser()

# С lambda — то же самое короче
chain = retriever | RunnableLambda(lambda docs: "\n".join([d.page_content for d in docs])) | prompt | llm

# Лайфхак — LangChain сам оборачивает функцию если передать напрямую
chain = retriever | format_docs | prompt | llm  # работает без явного RunnableLambda
Когда использовать: когда нужно добавить кастомную логику между компонентами — форматирование документов, фильтрация, трансформация данных.



# Как добавить retry в цепочку?

Используется .with_retry() - встроенный метод любого Runnable
# Простой retry
chain = prompt | llm.with_retry(stop_after_attempt=3) | parser

# С настройкой какие ошибки ретраить
chain = prompt | llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True,      # случайная задержка между попытками
    retry_if_exception_type=(ValueError, OutputParserException)
) | parser
Также можно через tenacity на уровне функции:
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def plan_speech(state):
    ...
Разница: .with_retry() - на уровне цепочки, удобно встраивать в LCEL. tenacity - на уровне функции, больше контроля над логикой retry


# Как добавить fallback если основная модель упала?

Если основная модель недоступна - автоматически переключается на запасную
# Основная цепочка
main_chain = prompt | giga | parser

# Запасная цепочка
fallback_chain = prompt | chatgpt | parser

# Объединяем
chain_with_fallback = main_chain.with_fallbacks([fallback_chain])
chain_with_fallback.invoke({"topic": "RAG"})
# Если giga упал → автоматически вызовется chatgpt
Можно добавить несколько fallback по приоритету:
chain.with_fallbacks([fallback_chain_1, fallback_chain_2])


# Что такое RunnablePassthrough и зачем?

Пропускает input без изменений - нужен когда хочешь передать исходные данные дальше по цепочке параллельно с обработанными.
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

chain = RunnableParallel({
    "context": retriever,              # обрабатывает input → достаёт документы
    "question": RunnablePassthrough()  # просто пропускает input дальше как есть
}) | prompt | llm | StrOutputParser()

chain.invoke("Как оформить отпуск?")
# prompt получает:
# {"context": [docs...], "question": "Как оформить отпуск?"}
Без RunnablePassthrough исходный вопрос потерялся бы после retriever

# Как передать несколько входных переменных в цепочку?

Через словарь в invoke - все переменные промпта передаются как ключи:
prompt = ChatPromptTemplate.from_template(
    "Ты эксперт по {domain}. Ответь на вопрос: {question}"
)

chain = prompt | llm | StrOutputParser()

chain.invoke({
    "domain": "банковскому делу",
    "question": "Как оформить кредит?"
})
Если часть переменных фиксированная - используем .partial():
chain = prompt.partial(domain="банковскому делу") | llm | StrOutputParser()
chain.invoke({"question": "Как оформить кредит?"})
Если переменные приходят из разных источников - RunnableParallel:
chain = RunnableParallel({
    "context": retriever,
    "question": RunnablePassthrough()
}) | prompt | llm | StrOutputParser()