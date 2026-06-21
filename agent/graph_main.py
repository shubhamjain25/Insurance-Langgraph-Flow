from langgraph.graph import StateGraph, START, END
from agent.graph_agents.input import input_agent
from agent.graph_agents.parser import parser_agent
from agent.graph_agents.processor import processor_agent
from agent.graph_agents.aggregator import aggregator_agent
from agent.router import *
from agent.schema_structures.Schema import *


def get_graph():
    builder = StateGraph(DocumentValidator)

    builder.add_node("input_node",input_agent)
    builder.add_node("parser_node",parser_agent)
    builder.add_node("processor_node",processor_agent)
    builder.add_node("aggregator_node",aggregator_agent)

    # intake_builder.add_node("hitl_node",hitl_agent)


    builder.add_edge(START,"input_node")
    builder.add_edge("input_node","parser_node")
    builder.add_conditional_edges(
        "parser_node",
        parser_router,{
            "APPROVED": "processor_node",
            "FAILED": "parser_node",
            "RETRY_EXHAUSTED": "aggregator_node",
        }
    )
    builder.add_edge("processor_node","aggregator_node")
    builder.add_edge("aggregator_node",END)

    graph = builder.compile()
    return graph