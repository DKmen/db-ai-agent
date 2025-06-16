from app.agents import db_agent_executor

if __name__ == "__main__":
    result = db_agent_executor.invoke({
        "input": "Give me information about this id e0604fd2-2888-4488-a827-81acdb7c98cc",
    })
    print(result)
