from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from app.config import settings
from app.logger import setup_logger
from app.services.prompt import AGENT_PROMPT, TOOL_SYSTEM_PROMPT
from app.core.event_bus import get_history
from app.tools.get_weather import get_weather
from app.tools.get_time import get_current_time


from langchain_core.prompts import ChatPromptTemplate

logger = setup_logger(__name__)


@tool
def weather(latitude: float, longitude: float) -> str:
    """Get current weather with latitude and longitude"""
    return get_weather(latitude, longitude)


@tool
def obtener_fecha_actual() -> str:
    """Devuelve la fecha y hora actual en formato ISO"""
    from datetime import datetime
    return datetime.now().isoformat()

llm = ChatOpenAI(
    base_url=settings.ollama_host,
    api_key="ollama",
    model='gpt-oss',
    temperature=0.2,
)

tools = [weather, obtener_fecha_actual]

llm = llm.bind_tools(tools)


def build_messages_from_history(
    session_id: str,
    prompt: str,
):

    """
    Create context of the chat conversation with the history of redis messages
    """

    logger.info(f"Building messages from history for session_id [{session_id}] and prompt [{prompt}]")

    history = get_history(session_id)


    # for i in history:
    #     logger.info(i)

    messages: list[BaseMessage] = [
        SystemMessage(content=TOOL_SYSTEM_PROMPT),
    ]

    for msg in history:
        content = msg.get("content", "")
        if msg.get("sender") == "user":
            messages.append(HumanMessage(content=str(content)))
        elif msg.get("sender") == "assistant":
            messages.append(AIMessage(content=str(content)))

    messages.append(HumanMessage(content=str(prompt)))
    
    return messages



async def generate_response(session_id: str | None, content: str) -> str:
    logger.info(f"Generating response for session_id [{session_id}] and content [{content}]")
    
    messages = build_messages_from_history(session_id, content)
    
    try:
        response = await llm.ainvoke(messages)

        print(response)
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            logger.info("Response with tool calls")

            for tool_call in response.tool_calls:
                logger.info(f"Tool call type: {type(tool_call)}")
                logger.info(f"Tool call: {tool_call}")


                tool_name = tool_call['name']
                tool_args = tool_call['args']
                
                # Find the tool function
                tool_func = next((t for t in tools if t.name == tool_name), None)

                if tool_func:
                    tool_result = await tool_func.ainvoke(tool_args)
                    
                    messages.append(
                        ToolMessage(
                            tool_call_id=tool_call['id'],
                            content=str(tool_result),
                        )
                    )
            
            # Get a new response with the tool results
            response = await llm.ainvoke(messages)
            
        return response.content
        
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request."