"""A simple LangGraph agent with tools."""

import os
from typing import Annotated, Literal

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict


# Define the state
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Define tools
@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    # Mock weather data
    weather_data = {
        "new york": "72°F, Sunny",
        "london": "58°F, Cloudy",
        "tokyo": "68°F, Partly Cloudy",
        "paris": "65°F, Rainy",
        "sydney": "80°F, Clear",
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression. Example: '2 + 2' or '10 * 5'"""
    try:
        # Only allow safe mathematical operations
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"


# Create the tools list
tools = [get_weather, calculate]

# Create the model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0).bind_tools(tools)


# Define the agent node
def agent(state: State) -> dict:
    """The agent node that calls the LLM."""
    system_message = SystemMessage(
        content="You are a helpful assistant. You can help with weather queries and calculations."
    )
    messages = [system_message] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


# Define the routing function
def should_continue(state: State) -> Literal["tools", END]:
    """Determine whether to continue to tools or end."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return END


# Build the graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("agent", agent)
workflow.add_node("tools", ToolNode(tools))

# Add edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# Compile the graph
graph = workflow.compile()

