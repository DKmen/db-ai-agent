# DB AI Agent - Multi-Agent Database Assistant

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange)](https://openai.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-latest-blue)](https://www.postgresql.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-purple)](https://github.com/langchain-ai/langgraph)

This project is an intelligent multi-agent system that provides a REST API for interacting with PostgreSQL databases using natural language queries. It features a supervisor agent that coordinates between specialized agents for database operations and data visualization, built with FastAPI, LangChain, **LangGraph**, and OpenAI.

## 🚀 Features
- 🌐 **REST API**: FastAPI-based web service with CORS support
- 🤖 **Multi-Agent Architecture**: Supervisor agent coordinating specialized agents
- 💬 **Natural Language Queries**: Convert plain English to SQL and execute securely
- 📊 **Data Visualization**: Generate charts and graphs from database results
- 🔍 **Automatic Schema Inspection**: Fetch and analyze database structure dynamically
- 🔒 **Secure Query Execution**: Only SELECT statements allowed with SQL injection prevention
- 👥 **User & Session Management**: Track users and maintain conversation history
- 🗄️ **Database Migration Support**: Alembic integration for schema management
- 🐳 **Docker Support**: Easy deployment with PostgreSQL containers

## 📁 Project Structure
```
app/
├── agents/                    # Multi-agent system components
│   ├── chat_agent/           # Supervisor agent coordinating other agents
│   │   ├── __init__.py
│   │   └── agent.py          # LangGraph supervisor implementation
│   ├── db_agent/             # Database operations agent
│   │   ├── __init__.py
│   │   ├── agent.py          # ReAct agent for database queries
│   │   └── tools/            # Database tools
│   │       ├── fetchSchema.py   # Schema inspection tool
│   │       └── runFetchQuery.py # Query execution tool
│   └── graph_agent/          # Data visualization agent
│       ├── __init__.py
│       └── agent.py          # Chart/graph generation agent
├── constants/                # Configuration and prompts
│   ├── __init__.py
│   ├── config.py            # Environment variable handling
│   └── prompt.py            # Agent prompts and instructions
├── controllers/             # FastAPI route controllers
│   ├── chat/                # Chat endpoint handling
│   ├── session/             # Session management
│   └── user/                # User management
├── db/                      # Database configuration
│   ├── __init__.py
│   └── connection.py        # SQLModel database connection
├── helper/                  # Utility modules
│   ├── __init__.py
│   ├── logger.py           # Logging configuration
│   └── model.py            # LLM model setup
└── models/                  # Database models
    ├── base.py             # Base model with common fields
    ├── user.py             # User model
    ├── session.py          # Session model
    └── session_chat.py     # Chat history model
alembic/                     # Database migrations
├── env.py
├── script.py.mako
└── versions/               # Migration files
main.py                     # FastAPI application entry point
requirements.txt            # Python dependencies
docker-compose.yaml         # PostgreSQL containers setup
alembic.ini                # Alembic configuration
.env                       # Environment variables (not tracked)
```

## 🛠️ Setup
1. **Clone the repository**

```zsh
git clone <repo-url>
cd db-ai-agent
```

2. **Set up PostgreSQL databases using Docker**

```zsh
docker-compose up -d
```

This will create two PostgreSQL containers:
- `postgres` (port 5432): General database
- `db_agent` (port 5433): Application database

3. **Create and activate a virtual environment**

```zsh
python3 -m venv venv
source venv/bin/activate
```

4. **Install dependencies**

```zsh
pip install -r requirements.txt
```

> **Note:** The requirements.txt file uses unpinned versions to avoid dependency conflicts. Pip will automatically resolve compatible versions for all packages.

5. **Configure environment variables**

Create a `.env` file in the project root with the following variables:

```
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5433
DB_NAME=db_agent
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_ID=gpt-4o-mini
GEMINI_API_KEY=your_gemini_api_key (optional)
GEMINI_MODEL_ID=gemini-2.0-flash (optional)
```

> **Note:** You need to obtain an OpenAI API key from [OpenAI](https://platform.openai.com/api-keys). Gemini API key is optional and can be obtained from [Google AI Studio](https://makersuite.google.com/app/apikey).

6. **Run database migrations**

```zsh
alembic upgrade head
```

7. **Start the FastAPI server**

```zsh
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` with automatic documentation at `http://localhost:8000/docs`.

## 🚀 Usage

### API Endpoints

Once the server is running, you can interact with the following endpoints:

#### 1. User Management
- `POST /api/v1/user/create` - Create a new user
- `GET /api/v1/user/{user_id}` - Get user information

#### 2. Session Management
- `POST /api/v1/session/create` - Create a new chat session
- `GET /api/v1/session/{session_id}` - Get session details

#### 3. Chat Interface
- `GET /api/v1/chat?session_id={uuid}&query={your_query}` - Send a natural language query

### Example Usage

1. **Create a user and session first:**
```bash
# Create user
curl -X POST "http://localhost:8000/api/v1/user/create" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "name": "John Doe"}'

# Create session
curl -X POST "http://localhost:8000/api/v1/session/create" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "your-user-id"}'
```

2. **Send chat queries:**
```bash
curl "http://localhost:8000/api/v1/chat?session_id=your-session-id&query=What%20tables%20are%20in%20the%20database?"
```

### Example Queries
- "What tables are in the database?"
- "Show me all users who have admin privileges"
- "How many orders were placed in the last month?"
- "Find products with inventory less than 10"
- "Create a chart showing sales by month"
- "Generate a bar graph of user registrations by date"

## 🧠 How It Works

### Multi-Agent Architecture
The system uses a sophisticated multi-agent architecture built with LangGraph:

1. **Supervisor Agent** (`chat_agent`):
   - Coordinates between specialized agents
   - Manages conversation flow and context
   - Determines which agent to use based on user queries

2. **Database Agent** (`db_agent`):
   - Fetches database schema using `fetch_schema` tool
   - Executes SQL queries using `run_query` tool
   - Returns structured data with query results

3. **Graph Agent** (`graph_agent`):
   - Generates data visualizations from database results
   - Creates HTML/JavaScript charts using D3.js, Chart.js, or Plotly
   - Handles requests for graphs, charts, and visual analytics

### Request Flow
1. User sends a natural language query via REST API
2. Supervisor agent analyzes the query and determines the appropriate agent
3. For data queries: DB agent fetches schema and executes SQL
4. For visualization requests: Graph agent creates charts from data
5. Conversation history is maintained in the database
6. Structured response is returned with data, query, and explanation

### Security Features
- Only SELECT queries are allowed for data retrieval
- SQL injection prevention through parameterized queries
- Session-based access control
- Schema inspection prevents unauthorized table access

### Architecture
The project follows a modern microservices-inspired architecture:
- **FastAPI**: RESTful API with automatic OpenAPI documentation
- **LangGraph**: Multi-agent coordination and workflow management
- **LangChain**: ReAct agents with tool integration
- **SQLModel**: Type-safe database ORM with Pydantic integration
- **Alembic**: Database migration management
- **PostgreSQL**: Robust relational database with JSON support
- **Docker**: Containerized database deployment

## 📦 Dependencies
Key dependencies include:
- **fastapi**: Modern, fast web framework for building APIs
- **langchain**: Framework for building applications with LLMs
- **langgraph**: Multi-agent workflow orchestration
- **langgraph-supervisor**: Supervisor agent implementation
- **langchain-openai**: OpenAI integration for LangChain
- **sqlmodel**: SQLAlchemy-based ORM with Pydantic validation
- **alembic**: Database migration tool
- **psycopg2-binary**: PostgreSQL adapter for Python
- **python-dotenv**: Environment variable management

> **Note:** All package versions are unpinned in requirements.txt to allow pip to automatically resolve compatible versions and avoid dependency conflicts.

See `requirements.txt` for the full list.

## 🔧 Troubleshooting

### Dependency Conflicts
If you encounter dependency conflicts during installation:

1. **Use unpinned versions**: The requirements.txt file has been configured with unpinned package versions to allow pip to resolve compatible versions automatically.

2. **Create a fresh virtual environment**:
   ```zsh
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Alternative installation methods**:
   - Use `pip install --force-reinstall -r requirements.txt` to force reinstallation
   - Try installing packages one by one to identify specific conflicts
   - Consider using `pip-tools` for dependency resolution

### Common Issues
- **OpenAI API errors**: Ensure your `OPENAI_API_KEY` is valid and has sufficient credits
- **Database connection errors**: Verify PostgreSQL containers are running (`docker-compose ps`)
- **Migration errors**: Run `alembic upgrade head` to apply latest database schema
- **Port conflicts**: Ensure ports 5432 and 5433 are available for PostgreSQL containers
- **Import errors**: Make sure all dependencies are installed in the virtual environment
- **CORS issues**: Frontend requests should include proper headers for cross-origin requests

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
- [FastAPI](https://fastapi.tiangolo.com/) for the modern web framework
- [LangChain](https://www.langchain.com/) for the agent framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for multi-agent orchestration
- [OpenAI](https://openai.com/) for the GPT models
- [SQLModel](https://sqlmodel.tiangolo.com/) for the database ORM
- [PostgreSQL](https://www.postgresql.org/) for the robust database system
