from dotenv import load_dotenv
from app.agents import supervisor
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# Load environment variables from .env file
load_dotenv()

def main(debug_mode=False):
    """
    Interactive chat session with the supervisor agent.
    Maintains conversation history and allows continuous interaction.
    
    Args:
        debug_mode (bool): If True, shows detailed message information
    """
    print("🤖 Database Assistant Chat")
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'debug' to toggle debug mode")
    if debug_mode:
        print("🔍 Debug mode: ON")
    print("=" * 50)
    
    # Initialize conversation state
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Goodbye! Thanks for using the Database Assistant.")
                break
            
            # Toggle debug mode
            if user_input.lower() == 'debug':
                debug_mode = not debug_mode
                status = "ON" if debug_mode else "OFF"
                print(f"\n🔍 Debug mode: {status}")
                continue
            
            if not user_input:
                print("Please enter a message or type 'quit' to exit.")
                continue
            
            # Add user message to history
            conversation_history.append(HumanMessage(content=user_input))
            
            print("\n🤖 Assistant: ", end="", flush=True)
            
            # Invoke supervisor with conversation history
            result = supervisor.invoke(
                {"messages": conversation_history}, 
                config=config
            )
            
            # Extract and display the latest response
            if result and "messages" in result:
                # Get all new messages from this interaction
                new_messages = result["messages"][len(conversation_history):]
                
                for i, message in enumerate(new_messages):
                    if debug_mode:
                        print(f"\n🔍 Message {i+1} Type: {type(message).__name__}")
                        if hasattr(message, 'name'):
                            print(f"🔍 Message Name: {message.name}")
                    
                    if hasattr(message, 'content') and message.content:
                        # Display the message content
                        if hasattr(message, 'name') and message.name:
                            print(f"\n🔧 {message.name}: {message.content}")
                        else:
                            print(f"\n{message.content}")
                    
                    # Display tool calls if present
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        for tool_call in message.tool_calls:
                            tool_name = tool_call.get('name', 'Unknown')
                            tool_args = tool_call.get('args', {})
                            print(f"\n🛠️  Tool Call: {tool_name}")
                            if debug_mode:
                                print(f"   Args: {tool_args}")
                    
                    # Display tool responses if present
                    if hasattr(message, 'tool_call_id') and hasattr(message, 'content'):
                        print(f"\n📊 Tool Response: {message.content}")
                    
                    # Show additional message attributes in debug mode
                    if debug_mode:
                        attrs_to_show = ['id', 'role', 'tool_call_id', 'additional_kwargs']
                        for attr in attrs_to_show:
                            if hasattr(message, attr) and getattr(message, attr):
                                print(f"🔍 {attr}: {getattr(message, attr)}")
                
                # Update conversation history with ALL new messages (including intermediate steps)
                conversation_history.extend(new_messages)
                
                # Show conversation statistics in debug mode
                if debug_mode:
                    print(f"\n🔍 Total messages in history: {len(conversation_history)}")
                    print(f"🔍 New messages this turn: {len(new_messages)}")
                
                # Display a separator for clarity
                print("\n" + "=" * 50)
                
            else:
                print("I apologize, but there was an issue processing your request.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or type 'quit' to exit.")

def run_single_query():
    """
    Alternative function to run a single query (for testing)
    """
    user_input = "Give me order statistics for the last 2 months. I want graph of it."
    result = supervisor.invoke({
        "messages": [HumanMessage(content=user_input)]
    })
    
    print("Response:")
    for message in result["messages"]:
        print(message.content)
        print("+" + "-" * 40)

if __name__ == "__main__":
    # Use interactive chat by default
    main()

