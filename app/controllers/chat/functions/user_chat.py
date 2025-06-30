from uuid import UUID
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from sqlmodel import Session, select
from sqlalchemy import desc


from app.db import engine
from app.models import SessionChat, Session as UserSession, MessageRole
from app.agents import supervisor

def user_chat_controller(session_id: UUID, query: str):
    """
    Run a database query within the context of a session.

    Args:
        session_id (UUID): The ID of the session.
        query (str): The SQL query to execute.

    Returns:
        The result of the query execution.
    """
    
    # fetch last 16 messages from session chat
    with Session(engine) as session:
        # fetch last 16 messages from session chat
        messages = session.exec(
            select(SessionChat).where(SessionChat.session_id == session_id).order_by(desc(SessionChat.created_at)).limit(16)
        ).all()
        
        chat_session = session.exec(
            select(UserSession).where(UserSession.id == session_id)
        ).first()
        
        if not chat_session:
            # close the session
            session.close()
            
            raise ValueError(f"Session with ID {session_id} not found.")
            
        # close the session
        session.close()
        
    # define conversation history
    old_conversation_history = []
    conversation_history = []
    
    # convert messages to conversation history
    for message in messages:
        if message.role == "user":
            old_conversation_history.append(HumanMessage(content=message.message))
        elif message.role == "assistant":
            old_conversation_history.append(AIMessage(content=message.message))
        elif message.role == "system":
            old_conversation_history.append(SystemMessage(content=message.message))
        elif message.role in ["tool", "tool_response", "tool_call"]:
            continue
            
    # add system message with DB connection URL
    old_conversation_history.append(SystemMessage(content=f"""
        Use this DB Connection URL to connect to the database:
        {chat_session.db_connection_url}
    """))
    
    # add user query to conversation history
    conversation_history = old_conversation_history + [HumanMessage(content=query)]
    
    # generate a unique thread ID for the conversation
    config = {"configurable": {"thread_id": session_id}}
    
    # Invoke supervisor with conversation history
    result = supervisor.invoke(
        {"messages": conversation_history}, 
        config=config
    )
    
    # update conversation history with the result
    if result and "messages" in result:
        # Get all new messages from this interaction
        new_messages = result["messages"][len(old_conversation_history):]
        
        for message in new_messages:
            if hasattr(message, 'type') and message.type == 'human':
                conversation_history.append(HumanMessage(content=message.content))
            elif hasattr(message, 'type') and message.type == 'ai':
                conversation_history.append(AIMessage(content=message.content))
            elif hasattr(message, 'type') and message.type == 'system':
                conversation_history.append(SystemMessage(content=message.content))
            elif hasattr(message, 'type') and message.type == 'tool':
                conversation_history.append(ToolMessage(content=message.content, tool_call_id=getattr(message, 'tool_call_id', '')))
            elif type(message).__name__ == 'HumanMessage':
                conversation_history.append(HumanMessage(content=message.content))
            elif type(message).__name__ == 'AIMessage':
                conversation_history.append(AIMessage(content=message.content))
            elif type(message).__name__ == 'SystemMessage':
                conversation_history.append(SystemMessage(content=message.content))
            elif type(message).__name__ == 'ToolMessage':
                conversation_history.append(ToolMessage(content=message.content, tool_call_id=getattr(message, 'tool_call_id', '')))
    
    # extract the latest message content from conversation history
    latest_message = conversation_history[len(old_conversation_history)+1:]
    
    # insert the new messages into the session chat
    with Session(engine) as session:
        conversation_history_trs = []
        for index, message in enumerate(latest_message):
            role = None
            message_content = ""
            
            # Determine role and content based on message type
            if hasattr(message, 'type'):
                if message.type == 'human':
                    role = MessageRole.USER
                elif message.type == 'ai':
                    role = MessageRole.ASSISTANT
                elif message.type == 'system':
                    role = MessageRole.SYSTEM
                elif message.type == 'tool':
                    role = MessageRole.TOOL
            elif type(message).__name__ == 'HumanMessage':
                role = MessageRole.USER
            elif type(message).__name__ == 'AIMessage':
                role = MessageRole.ASSISTANT
            elif type(message).__name__ == 'SystemMessage':
                role = MessageRole.SYSTEM
            elif type(message).__name__ == 'ToolMessage':
                role = MessageRole.TOOL

            # Get message content
            if hasattr(message, 'content') and message.content:
                message_content = message.content
            elif hasattr(message, 'name') and message.name:
                message_content = message.name
            else:
                message_content = str(message)
            
            # Skip if we couldn't determine the role
            if not role:
                continue
            
            # create a new session chat entry
            conversation_history_trs.append(SessionChat(
                session_id=session_id,
                message=message_content,
                role=role,
                is_final_message= (index == (len(latest_message) - 1) or index == 0 )
            ))

        # add to the session
        session.add_all(conversation_history_trs)

        # commit the changes
        session.commit()
    
    # return the latest message content
    return latest_message[-1].content if latest_message else "No response generated."
