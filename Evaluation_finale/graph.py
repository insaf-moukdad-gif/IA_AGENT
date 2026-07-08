"""
graph.py
--------
Construction du graphe LangGraph 
"""

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage
from langchain.messages import ToolMessage
from langchain_ollama import ChatOllama  # remplacer par ChatOpenAI/ChatAnthropic si besoin

from etat import HelpDeskAgentState
from prompt import SYSTEM_PROMPT
from tool import all_tools, tools_by_name
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

# --- Modele LLM avec tools ---------------------------------------------
model = ChatOllama(model="llama3.2:3b", temperature=0)
model_with_tools = model.bind_tools(all_tools)


# -------------------------------------------------------------------
# Agent
# -------------------------------------------------------------------

def agent(state: HelpDeskAgentState):

    response = model_with_tools.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] +
        state["messages"]
    )

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# -------------------------------------------------------------------
# Tools
# -------------------------------------------------------------------

def tools(state: HelpDeskAgentState):

    last_message = state["messages"][-1]

    messages = []

    for call in last_message.tool_calls:

        tool = tools_by_name[call["name"]]

        result = tool.invoke(call["args"])

        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )
        )

    return {
        "messages": messages,
        "tool_calls_count":
            state.get("tool_calls_count", 0)
            + len(last_message.tool_calls),
    }


# -------------------------------------------------------------------
# Condition
# -------------------------------------------------------------------

def should_continue(state: HelpDeskAgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


# -------------------------------------------------------------------
# Graphe
# -------------------------------------------------------------------

def build_graph():

    builder = StateGraph(HelpDeskAgentState)

    builder.add_node("agent", agent)

    builder.add_node("tools", tools)

    builder.add_edge(START, "agent")

    builder.add_conditional_edges(
        "agent",
        should_continue,
        ["tools", END],
    )

    builder.add_edge("tools", "agent")

    graph = builder.compile(
        checkpointer=memory
    )

    return graph


# -------------------------------------------------------------------
# Visualisation
# -------------------------------------------------------------------

def save_graph_image(graph, path="graph.png"):

    png = graph.get_graph().draw_mermaid_png()

    with open(path, "wb") as f:
        f.write(png)

    print("Graphe sauvegardé :", path)
