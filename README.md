# DB Retrieval LangChain Agent

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green)](https://www.langchain.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.0--flash-orange)](https://ai.google.dev/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.24-yellow)](https://sqlmodel.tiangolo.com/)

This project is an intelligent agent that interacts with a PostgreSQL database using natural language queries. It leverages LangChain, Google Generative AI (Gemini), and SQLModel to fetch database schema and execute SQL queries securely.

## 🚀 Features
- 💬 Natural language interface to query a PostgreSQL database
- 🔍 Automatic schema inspection before query generation
- 🔒 Secure query execution (only SELECT statements allowed)
- 🧩 Modular tool-based architecture
- 🤖 Powered by Google's Gemini AI model

## 📁 Project Structure
```
app/
├── agent/         # Agent logic and executor
│   ├── __init__.py
│   └── agent.py   # Main agent implementation with LangChain
├── constants/     # Configuration and environment variables
│   ├── __init__.py
│   └── config.py  # Environment variable handling
├── db/            # Database connection setup
│   ├── __init__.py
│   └── connection.py # SQLModel database connection
└── tools/         # Tools for schema fetching and query execution
    ├── __init__.py
    ├── fetchSchema.py   # Database schema inspection
    ├── runFetchQuery.py # Secure query execution
    └── tool.py          # LangChain tool definitions
main.py          # Entry point for running the agent
requirements.txt # Python dependencies
.env             # Environment variables (not tracked in git)
```

## 🛠️ Setup
1. **Clone the repository**

```zsh
git clone <repo-url>
cd db-retrival-lang-chain
```

2. **Create and activate a virtual environment**

```zsh
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```zsh
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root with the following variables:

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL_ID=gemini-2.0-flash
```

> **Note:** You need to obtain a Gemini API key from the [Google AI Studio](https://makersuite.google.com/app/apikey).

5. **Ensure your PostgreSQL database is running**

Make sure the PostgreSQL database is up and running with the credentials specified in your `.env` file.

## 🚀 Usage
Run the agent with:

```zsh
python main.py
```

The agent will process the default query in `main.py`. You can modify the query by changing the input parameter in the `executor.invoke()` function:

```python
# in main.py
result = executor.invoke({
    "input": "Your natural language query here",
})
```

### Example Queries
- "What tables are in the database?"
- "Show me all users who have admin privileges"
- "How many orders were placed in the last month?"
- "Find products with inventory less than 10"

## 🧠 How It Works
1. The agent receives a natural language query from the user
2. It always fetches the database schema first using the `fetch_db_schema` tool
3. Based on the schema and the query, it generates appropriate SQL
4. It executes the SQL using the `run_query` tool, which enforces security restrictions
5. The results are processed and returned in a human-readable format

### Security Features
- Only SELECT queries are allowed for data retrieval
- SQL injection is prevented by using parameterized queries
- Schema inspection prevents guessing of table and column names

### Architecture
The project follows a modular architecture based on LangChain's ReAct agent pattern:
- **Agent**: Orchestrates the tools and maintains conversation context
- **Tools**: Provide specific functionality like schema inspection and query execution
- **Prompt Template**: Guides the LLM behavior with specific instructions
- **Database Connection**: Manages the PostgreSQL connection using SQLModel

## 📦 Dependencies
Key dependencies include:
- **langchain** (0.3.25+): Framework for building applications with LLMs
- **langchain-google-genai**: Integration with Google's Generative AI
- **sqlmodel**: SQLAlchemy-based ORM for Python
- **psycopg2-binary**: PostgreSQL adapter for Python
- **python-dotenv**: For loading environment variables from .env file

See `requirements.txt` for the full list.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements
- [LangChain](https://www.langchain.com/) for the agent framework
- [Google Generative AI](https://ai.google.dev/) for the Gemini model
- [SQLModel](https://sqlmodel.tiangolo.com/) for the database ORM
