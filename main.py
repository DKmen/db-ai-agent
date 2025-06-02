from dotenv import load_dotenv

from app.agent import executor

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    result = executor.invoke({
        "input": "Normal User is able to create new user if not why ?",
    })
    print(result)
