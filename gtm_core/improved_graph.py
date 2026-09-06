"""
LangGraph orchestration for the Improved GTM multi-agent workflow (Week 4).
Connects the improved nodes with explicit revision feedback injection and safety guardrails.
"""

from typing import Any
from langgraph.graph import StateGraph, START, END
from .state import GTMState
from .agents import get_llm
from .improved_agents import (
    improved_strategy_node,
    improved_linkedin_node,
    improved_email_node,
    improved_ad_copy_node,
    improved_blog_node,
    improved_critic_node
)

def build_improved_gtm_graph(provider: str = "mock", model_name: str = None, api_key: str = None):
    """Builds and compiles the improved LangGraph pipeline."""
    llm = get_llm(provider=provider, model_name=model_name, api_key=api_key)
    
    workflow = StateGraph(GTMState)
    
    # Node wrappers injecting LLM
    def run_strategist(state: GTMState) -> GTMState:
        return improved_strategy_node(state, llm)
        
    def run_linkedin(state: GTMState) -> GTMState:
        return improved_linkedin_node(state, llm)
        
    def run_email(state: GTMState) -> GTMState:
        return improved_email_node(state, llm)
        
    def run_ads(state: GTMState) -> GTMState:
        return improved_ad_copy_node(state, llm)
        
    def run_blog(state: GTMState) -> GTMState:
        return improved_blog_node(state, llm)
        
    def run_critic(state: GTMState) -> GTMState:
        return improved_critic_node(state, llm)
        
    # Register Nodes
    workflow.add_node("strategist", run_strategist)
    workflow.add_node("linkedin_writer", run_linkedin)
    workflow.add_node("email_writer", run_email)
    workflow.add_node("ad_writer", run_ads)
    workflow.add_node("blog_writer", run_blog)
    workflow.add_node("critic", run_critic)
    
    # Sequential Pipeline Edges
    workflow.add_edge(START, "strategist")
    workflow.add_edge("strategist", "linkedin_writer")
    workflow.add_edge("linkedin_writer", "email_writer")
    workflow.add_edge("email_writer", "ad_writer")
    workflow.add_edge("ad_writer", "blog_writer")
    workflow.add_edge("blog_writer", "critic")
    
    # QA Revision Loop
    def should_revise(state: GTMState) -> str:
        passed = state.get("review_passed", True)
        revisions = state.get("revision_count", 0)
        max_revisions = state.get("max_revisions", 1)
        
        if not passed and revisions < max_revisions:
            return "linkedin_writer"
        return END

    workflow.add_conditional_edges(
        "critic",
        should_revise,
        {
            "linkedin_writer": "linkedin_writer",
            END: END
        }
    )
    
    return workflow.compile()
