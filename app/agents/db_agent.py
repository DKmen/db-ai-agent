from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory

from app.tools import tools
from app.constants import config

llm = ChatGoogleGenerativeAI(
    model=config["GEMINI_MODEL_ID"], 
    temperature=0.8,
)

prompt = PromptTemplate.from_template("""
You are an intelligent agent with access to tools that help answer questions about a PostgreSQL database.

You have access to the following tools:
{tools}

Please follow this exact format when reasoning through the question and using tools:

```
Question: the user's question  
Thought: what you need to do next  
Action: the tool to use (must be one of [{tool_names}])  
Action Input: the input to the action  
Observation: the result of the action  
... (repeat Thought/Action/Action Input/Observation as needed)  
Thought: I now know the final answer  
Final Answer: your final answer
```

### 🔐 Strict Instructions:

1. **If the question is about the database**, your **first step must always be**:

   ```
   Thought: I need to see the schema before writing a SQL query.
   Action: fetch_db_schema
   Action Input: ""
   ```

   You **must not guess** the table or column names. Only write SQL after inspecting the schema returned by `fetch_db_schema`.

2. When using the `run_query` tool:

   * Always write the SQL query as a **plain text string** (no code block formatting).
   * The SQL must be **syntactically correct** and use only columns/tables present in the schema.

### ❌ Invalid SQL Example (wrong formatting and/or guessing columns):
```sql
SELECT name FROM random_table;
``` ---> ( Because it wrape around ```sql ``` )

### ✅ Valid SQL Example:
SELECT name FROM random_table;


Begin.

Question: {input}
{agent_scratchpad}
""")

history = RedisChatMessageHistory(
    session_id="user_123",
    url="redis://localhost:6379"
)

memory = ConversationBufferMemory(
    chat_memory=history,
    return_messages=True,
    memory_key="chat_history"
)

db_agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

db_agent_executor = AgentExecutor.from_agent_and_tools(
    agent=db_agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

def call_db_agent_executor(input: str):
    """
    Call the database agent executor with the given input.
    """
    return db_agent_executor.invoke({
        "input": input,
    })
