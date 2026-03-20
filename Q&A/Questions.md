LCEL и цепочки (1-10)

Что такое LCEL и зачем он нужен?
Что такое Runnable и какие методы у него есть?
Чем invoke отличается от stream и batch?
Как работает оператор | под капотом?
Что такое RunnableParallel и когда использовать?
Что такое RunnableLambda?
Как добавить retry в цепочку?
Как добавить fallback если основная модель упала?
Что такое RunnablePassthrough и зачем?
Как передать несколько входных переменных в цепочку?


Prompts (11-18)

Чем PromptTemplate отличается от ChatPromptTemplate?
Что такое .partial() и зачем нужен?
Что такое MessagesPlaceholder?
Как вставить историю сообщений в промпт?
Что такое few-shot prompting в LangChain?
Как динамически менять system prompt в зависимости от пользователя?
Чем HumanMessage отличается от SystemMessage и AIMessage?
Как передать изображение в промпт (multimodal)?


Output Parsers (19-24)

Чем StrOutputParser отличается от PydanticOutputParser?
Что такое format_instructions и как они попадают в промпт?
Зачем Field(description=...) в Pydantic-схеме?
Что такое OutputFixingParser?
Что такое JsonOutputParser и чем отличается от Pydantic?
Что будет если модель вернёт невалидный JSON?


Retriever и VectorStore (25-33)

Чем VectorStore отличается от Retriever?
Как создать Retriever из VectorStore?
Что такое search_type="mmr" и зачем?
Что такое MultiQueryRetriever?
Что такое ContextualCompressionRetriever?
Как работает similarity_search под капотом?
Чем Chroma отличается от Faiss и Pinecone?
Что такое k в search_kwargs={"k": 4}?
Как обновить документы в векторной БД?


RAG (34-40)

Что такое RAG и из каких шагов состоит pipeline?
Зачем нужен чанкинг и как выбрать chunk_size?
Что такое chunk_overlap и зачем?
Чем RecursiveCharacterTextSplitter отличается от CharacterTextSplitter?
Как загрузить PDF в LangChain?
Что такое ParentDocumentRetriever?
Fine-tuning vs RAG — когда что выбрать?


Memory (41-44)

Что такое ConversationBufferMemory?
Чем LangChain Memory отличается от LangGraph checkpointer?
Что такое ConversationSummaryMemory и когда нужна?
Как ограничить размер памяти чтобы не переполнять контекст?


Tools и Agents (45-50)

Что такое Tool в LangChain?
Как создать кастомный Tool?
Что такое create_react_agent?
Что такое AgentExecutor?
Чем LangChain Agent отличается от LangGraph агента?
Когда использовать LangChain Agent, а когда LangGraph?