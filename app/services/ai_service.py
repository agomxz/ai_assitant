from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    BaseMessage,
    AIMessage,
    ToolMessage,
)
from langchain_core.tools import tool
from app.config import settings
from app.logger import setup_logger
from app.services.prompt import TOOL_SYSTEM_PROMPT
from app.core.event_bus import get_history
from app.tools.get_weather import get_weather
from datetime import datetime


logger = setup_logger(__name__)


@tool
def tool_get_weather(latitude: float, longitude: float) -> str:
    """Get current weather with latitude and longitude"""
    logger.info('Getting current weather from API')
    return get_weather(latitude, longitude)


@tool
def tool_current_date_time() -> str:
    """Get current date and time"""
    logger.info('Getting toll current datetime')
    return datetime.now().isoformat()


llm = ChatOpenAI(
    base_url=settings.ollama_host,
    api_key="ollama",
    model="gpt-oss",
    temperature=0.2,
)

tools = [tool_get_weather, tool_current_date_time]

llm = llm.bind_tools(tools)


def build_messages_from_history(
    session_id: str,
    prompt: str,
)->list:
    """
    Create context of the chat conversation with the history of redis messages
    """

    logger.info(f"Build messages from history for session_id [{session_id}]")

    history = get_history(session_id)

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
    """
    Build reponse to user
    Exists two tools:
        - tool_get_weather
        - tool_current_date_time
    """
    logger.info(f"Generating for session_id [{session_id}]")

    messages = build_messages_from_history(session_id, content)

    try:
        response = await llm.ainvoke(messages)
        
        if hasattr(response, "tool_calls") and response.tool_calls:
            logger.info("Response with tool calls")

            for tool_call in response.tool_calls:
                logger.info(f"Tool to call: {tool_call}")

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                tool_func = next((t for t in tools if t.name == tool_name), None)

                if tool_func:
                    tool_result = await tool_func.ainvoke(tool_args)

                    messages.append(
                        ToolMessage(
                            tool_call_id=tool_call["id"],
                            content=str(tool_result),
                        )
                    )


            # Get a new response with the tool results
            response = await llm.ainvoke(messages)

        return response.content

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "I'm sorry, I encountered an error."
