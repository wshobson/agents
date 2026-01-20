"""
CrewAI Crew Template

Production-ready template for building CrewAI Crews with:
- Proper error handling
- Rate limiting
- Memory configuration
- Structured outputs
- Monitoring hooks

Usage:
    from crew_template import build_research_crew

    crew = build_research_crew()
    result = crew.kickoff(inputs={"topic": "AI Agents"})
"""

import os
from typing import List, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai.memory import LongTermMemory
from crewai.memory.storage import RAGStorage


# ============================================================================
# Configuration
# ============================================================================

def get_llm(model: str = "anthropic/claude-sonnet-4-5") -> LLM:
    """Get configured LLM instance."""
    return LLM(model=model)


def get_embedder_config() -> dict:
    """Get embedding configuration."""
    return {
        "provider": "openai",
        "config": {"model": "text-embedding-3-large"}
    }


def get_memory_storage() -> RAGStorage:
    """Get memory storage configuration."""
    return RAGStorage(
        type="chroma",
        persist_directory="./crew_memory",
        embedder=get_embedder_config()
    )


# ============================================================================
# Output Schemas
# ============================================================================

class ResearchOutput(BaseModel):
    """Structured output for research task."""
    findings: List[str] = Field(description="Key research findings")
    sources: List[str] = Field(description="Source URLs or references")
    confidence: float = Field(description="Confidence score 0-1")
    summary: str = Field(description="Brief summary of findings")


class AnalysisOutput(BaseModel):
    """Structured output for analysis task."""
    insights: List[str] = Field(description="Key insights from analysis")
    recommendations: List[str] = Field(description="Actionable recommendations")
    risks: List[str] = Field(description="Identified risks or concerns")
    score: float = Field(description="Overall assessment score 0-100")


class ContentOutput(BaseModel):
    """Structured output for content creation."""
    title: str = Field(description="Content title")
    body: str = Field(description="Main content body")
    sections: List[str] = Field(description="Section headings")
    word_count: int = Field(description="Total word count")


# ============================================================================
# Agents
# ============================================================================

def create_researcher(llm: Optional[LLM] = None) -> Agent:
    """Create a research specialist agent."""
    return Agent(
        role="Senior Research Analyst",
        goal="Discover comprehensive, accurate information on {topic}",
        backstory="""You are a meticulous researcher with 15 years of experience
        in investigative journalism. You excel at finding credible sources,
        cross-referencing information, and synthesizing complex data.
        You always cite your sources and indicate confidence levels.""",
        llm=llm or get_llm(),
        verbose=True,
        memory=True,
        max_iter=5,
        max_rpm=10,
        allow_delegation=False
    )


def create_analyst(llm: Optional[LLM] = None) -> Agent:
    """Create a data analyst agent."""
    return Agent(
        role="Senior Data Analyst",
        goal="Analyze data and provide actionable insights on {topic}",
        backstory="""You are an expert data analyst with a background in
        statistics and business intelligence. You identify patterns,
        trends, and anomalies that others miss. You present findings
        clearly with supporting evidence.""",
        llm=llm or get_llm(),
        verbose=True,
        memory=True,
        max_iter=5,
        allow_delegation=False
    )


def create_writer(llm: Optional[LLM] = None) -> Agent:
    """Create a content writer agent."""
    return Agent(
        role="Senior Technical Writer",
        goal="Create clear, engaging, well-structured content",
        backstory="""You are an expert technical writer who transforms
        complex information into accessible, well-organized content.
        You have a talent for explaining difficult concepts in simple
        terms while maintaining technical accuracy.""",
        llm=llm or get_llm(),
        verbose=True,
        memory=True,
        max_iter=5,
        allow_delegation=False
    )


def create_editor(llm: Optional[LLM] = None) -> Agent:
    """Create a content editor agent."""
    return Agent(
        role="Senior Editor",
        goal="Ensure content accuracy, clarity, and professional quality",
        backstory="""You are a seasoned editor with extensive experience
        in technical publishing. You have a keen eye for detail and
        maintain the highest editorial standards. You improve clarity
        without changing the author's voice.""",
        llm=llm or get_llm(),
        verbose=True,
        memory=True,
        max_iter=3,
        allow_delegation=False
    )


# ============================================================================
# Tasks
# ============================================================================

def create_research_task(agent: Agent) -> Task:
    """Create a research task with structured output."""
    return Task(
        description="""Research the following topic thoroughly: {topic}

        Requirements:
        1. Find at least 5 credible sources
        2. Extract key facts and insights
        3. Identify any conflicting information
        4. Provide confidence scores for findings
        5. Cite all sources""",
        expected_output="Comprehensive research report with cited sources",
        agent=agent,
        output_pydantic=ResearchOutput
    )


def create_analysis_task(agent: Agent, context: List[Task]) -> Task:
    """Create an analysis task with context from research."""
    return Task(
        description="""Analyze the research findings and provide insights.

        Requirements:
        1. Identify key patterns and trends
        2. Provide actionable recommendations
        3. Highlight potential risks or concerns
        4. Give an overall assessment score""",
        expected_output="Detailed analysis with insights and recommendations",
        agent=agent,
        context=context,
        output_pydantic=AnalysisOutput
    )


def create_writing_task(agent: Agent, context: List[Task]) -> Task:
    """Create a writing task with context from analysis."""
    return Task(
        description="""Create a well-structured article based on the analysis.

        Requirements:
        1. Clear introduction explaining the topic
        2. Well-organized sections with headers
        3. Technical accuracy with source citations
        4. Actionable conclusions
        5. Target: 1000-1500 words""",
        expected_output="A polished technical article",
        agent=agent,
        context=context,
        output_pydantic=ContentOutput
    )


def create_editing_task(agent: Agent, context: List[Task]) -> Task:
    """Create an editing task with context from writing."""
    return Task(
        description="""Review and polish the article for publication.

        Requirements:
        1. Check for factual accuracy
        2. Improve clarity and flow
        3. Fix any grammatical issues
        4. Ensure consistent formatting
        5. Verify all citations""",
        expected_output="Publication-ready article with edit notes",
        agent=agent,
        context=context
    )


# ============================================================================
# Crews
# ============================================================================

def build_research_crew(
    enable_memory: bool = True,
    enable_long_term_memory: bool = False,
    verbose: bool = True
) -> Crew:
    """
    Build a complete research crew with configurable options.

    Args:
        enable_memory: Enable short-term memory
        enable_long_term_memory: Enable persistent long-term memory
        verbose: Enable verbose logging

    Returns:
        Configured Crew instance
    """
    llm = get_llm()

    # Create agents
    researcher = create_researcher(llm)
    analyst = create_analyst(llm)
    writer = create_writer(llm)
    editor = create_editor(llm)

    # Create tasks with dependencies
    research_task = create_research_task(researcher)
    analysis_task = create_analysis_task(analyst, [research_task])
    writing_task = create_writing_task(writer, [analysis_task])
    editing_task = create_editing_task(editor, [writing_task])

    # Configure memory
    long_term_memory = None
    if enable_long_term_memory:
        long_term_memory = LongTermMemory(storage=get_memory_storage())

    # Build crew
    crew = Crew(
        agents=[researcher, analyst, writer, editor],
        tasks=[research_task, analysis_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=verbose,
        memory=enable_memory,
        long_term_memory=long_term_memory,
        embedder=get_embedder_config() if enable_memory else None
    )

    return crew


def build_analysis_crew(
    enable_memory: bool = True,
    verbose: bool = True
) -> Crew:
    """
    Build a focused analysis crew (research + analysis only).

    Args:
        enable_memory: Enable short-term memory
        verbose: Enable verbose logging

    Returns:
        Configured Crew instance
    """
    llm = get_llm()

    researcher = create_researcher(llm)
    analyst = create_analyst(llm)

    research_task = create_research_task(researcher)
    analysis_task = create_analysis_task(analyst, [research_task])

    return Crew(
        agents=[researcher, analyst],
        tasks=[research_task, analysis_task],
        process=Process.sequential,
        verbose=verbose,
        memory=enable_memory
    )


# ============================================================================
# Execution with Error Handling
# ============================================================================

def execute_crew(
    crew: Crew,
    inputs: dict,
    max_retries: int = 3
) -> dict:
    """
    Execute crew with error handling and retries.

    Args:
        crew: Crew instance to execute
        inputs: Input dictionary for kickoff
        max_retries: Maximum retry attempts

    Returns:
        Result dictionary with output and metadata
    """
    import time

    last_error = None

    for attempt in range(max_retries):
        try:
            result = crew.kickoff(inputs=inputs)
            return {
                "success": True,
                "output": result.raw,
                "pydantic": result.pydantic if hasattr(result, 'pydantic') else None,
                "attempts": attempt + 1
            }
        except Exception as e:
            last_error = e
            error_msg = str(e).lower()

            # Check if retryable
            retryable = any(err in error_msg for err in [
                "rate limit", "timeout", "connection", "502", "503", "504"
            ])

            if retryable and attempt < max_retries - 1:
                delay = 2 ** attempt  # Exponential backoff
                print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                time.sleep(delay)
            else:
                break

    return {
        "success": False,
        "error": str(last_error),
        "attempts": max_retries
    }


# ============================================================================
# Callbacks for Monitoring
# ============================================================================

def on_task_complete(task, output):
    """Callback for task completion monitoring."""
    print(f"[TASK COMPLETE] {task.description[:50]}...")
    print(f"[OUTPUT] {str(output)[:200]}...")
    # Add your monitoring/logging here
    # e.g., send to DataDog, CloudWatch, etc.


def setup_monitoring(crew: Crew):
    """Setup monitoring callbacks on crew."""
    crew.on_task_complete = on_task_complete
    return crew


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Example usage
    print("Building research crew...")
    crew = build_research_crew(
        enable_memory=True,
        enable_long_term_memory=False,
        verbose=True
    )

    # Setup monitoring
    crew = setup_monitoring(crew)

    # Execute with error handling
    print("\nExecuting crew...")
    result = execute_crew(
        crew=crew,
        inputs={"topic": "Best practices for AI agent development"},
        max_retries=3
    )

    if result["success"]:
        print(f"\n[SUCCESS] Completed in {result['attempts']} attempt(s)")
        print(f"\nOutput:\n{result['output']}")
    else:
        print(f"\n[FAILED] Error: {result['error']}")
