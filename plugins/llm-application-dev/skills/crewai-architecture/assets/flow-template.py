"""
CrewAI Flow Template

Production-ready template for building CrewAI Flows with:
- Structured state management
- Error handling and recovery
- Conditional routing
- State persistence
- Monitoring hooks

Usage:
    from flow_template import ResearchFlow

    flow = ResearchFlow()
    result = flow.kickoff(inputs={"query": "AI agent architectures"})
    print(flow.state.final_output)
"""

import time
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

from crewai import Agent, Task, Crew, LLM
from crewai.flow.flow import Flow, listen, start, router


# ============================================================================
# State Models
# ============================================================================

class FlowState(BaseModel):
    """
    Structured state for the flow.

    Using Pydantic provides:
    - Type safety
    - Validation
    - IDE autocomplete
    - Serialization
    """
    # Input
    query: str = ""

    # Processing state
    status: Literal["pending", "researching", "analyzing", "writing", "complete", "failed"] = "pending"
    iteration: int = 0
    max_iterations: int = 10

    # Results
    research_results: List[str] = Field(default_factory=list)
    analysis: str = ""
    final_output: str = ""

    # Error tracking
    errors: List[str] = Field(default_factory=list)
    last_error: Optional[str] = None

    # Metadata
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def record_error(self, error: str):
        """Record an error in state."""
        self.errors.append(error)
        self.last_error = error

    def get_duration(self) -> Optional[float]:
        """Get flow duration in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


# ============================================================================
# LLM Configuration
# ============================================================================

def get_llm(model: str = "anthropic/claude-sonnet-4-5") -> LLM:
    """Get configured LLM instance."""
    return LLM(model=model)


# ============================================================================
# Agent Factories
# ============================================================================

def create_researcher() -> Agent:
    """Create research agent."""
    return Agent(
        role="Research Specialist",
        goal="Find comprehensive, accurate information",
        backstory="Expert researcher with attention to detail",
        llm=get_llm(),
        verbose=True,
        memory=True,
        max_iter=5
    )


def create_analyst() -> Agent:
    """Create analysis agent."""
    return Agent(
        role="Data Analyst",
        goal="Analyze data and provide actionable insights",
        backstory="Expert analyst who finds patterns in data",
        llm=get_llm(),
        verbose=True,
        memory=True,
        max_iter=5
    )


def create_writer() -> Agent:
    """Create content writer agent."""
    return Agent(
        role="Technical Writer",
        goal="Create clear, well-structured content",
        backstory="Expert writer who explains complex topics simply",
        llm=get_llm(),
        verbose=True,
        memory=True,
        max_iter=5
    )


# ============================================================================
# Flow Implementation
# ============================================================================

class ResearchFlow(Flow[FlowState]):
    """
    Production-ready research flow.

    Flow pattern:
    1. Initialize -> Research -> Route
    2. If research successful -> Analyze -> Write -> Complete
    3. If research failed -> Retry or Fail

    Usage:
        flow = ResearchFlow()
        result = flow.kickoff(inputs={"query": "AI agents"})
        print(flow.state.final_output)
    """

    def __init__(self):
        super().__init__()
        # Create agents once (reused across steps)
        self._researcher = create_researcher()
        self._analyst = create_analyst()
        self._writer = create_writer()

    # ========================================================================
    # Flow Steps
    # ========================================================================

    @start()
    def initialize(self):
        """Entry point: Initialize flow state."""
        self.state.status = "pending"
        self.state.started_at = datetime.now()
        self.state.iteration = 1

        print("\n" + "=" * 60)
        print("FLOW STARTING")
        print(f"Query: {self.state.query}")
        print("=" * 60 + "\n")

        return {"status": "initialized", "query": self.state.query}

    @listen(initialize)
    def research(self, init_result):
        """Execute research crew."""
        print(f"\n--- RESEARCH PHASE (Iteration {self.state.iteration}) ---")
        self.state.status = "researching"

        try:
            crew = Crew(
                agents=[self._researcher],
                tasks=[Task(
                    description=f"Research the following query thoroughly: {self.state.query}",
                    expected_output="Comprehensive research findings with sources",
                    agent=self._researcher
                )],
                verbose=True
            )

            result = crew.kickoff()
            self.state.research_results = [result.raw]

            print(f"Research complete: {len(result.raw)} characters")
            return {"success": True, "result": result.raw}

        except Exception as e:
            error_msg = f"Research failed: {str(e)}"
            self.state.record_error(error_msg)
            print(f"ERROR: {error_msg}")
            return {"success": False, "error": error_msg}

    @router(research)
    def route_after_research(self) -> Literal["analyze", "retry_research", "fail"]:
        """Route based on research results."""
        # Check if research was successful
        if self.state.research_results and len(self.state.research_results[0]) > 100:
            return "analyze"

        # Check iteration limit
        if self.state.iteration >= self.state.max_iterations:
            return "fail"

        # Retry
        self.state.iteration += 1
        return "retry_research"

    @listen("retry_research")
    def retry_research(self):
        """Retry research with backoff."""
        print(f"\n--- RETRYING RESEARCH (Iteration {self.state.iteration}) ---")

        # Exponential backoff
        delay = 2 ** (self.state.iteration - 1)
        print(f"Waiting {delay} seconds before retry...")
        time.sleep(delay)

        # Clear previous errors for this attempt
        self.state.research_results = []

        # Re-run research
        return self.research({"retry": True})

    @listen("analyze")
    def analyze(self):
        """Analyze research results."""
        print("\n--- ANALYSIS PHASE ---")
        self.state.status = "analyzing"

        try:
            crew = Crew(
                agents=[self._analyst],
                tasks=[Task(
                    description=f"""Analyze these research findings and provide insights:

                    {self.state.research_results[0][:5000]}

                    Provide:
                    1. Key insights
                    2. Patterns identified
                    3. Recommendations""",
                    expected_output="Detailed analysis with insights",
                    agent=self._analyst
                )],
                verbose=True
            )

            result = crew.kickoff()
            self.state.analysis = result.raw

            print(f"Analysis complete: {len(result.raw)} characters")
            return {"success": True, "result": result.raw}

        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}"
            self.state.record_error(error_msg)
            return {"success": False, "error": error_msg}

    @listen(analyze)
    def write(self, analysis_result):
        """Write final output."""
        print("\n--- WRITING PHASE ---")
        self.state.status = "writing"

        try:
            crew = Crew(
                agents=[self._writer],
                tasks=[Task(
                    description=f"""Create a comprehensive report based on:

                    RESEARCH:
                    {self.state.research_results[0][:3000]}

                    ANALYSIS:
                    {self.state.analysis[:3000]}

                    Create a well-structured report with clear sections.""",
                    expected_output="Professional report",
                    agent=self._writer
                )],
                verbose=True
            )

            result = crew.kickoff()
            self.state.final_output = result.raw

            return {"success": True, "result": result.raw}

        except Exception as e:
            error_msg = f"Writing failed: {str(e)}"
            self.state.record_error(error_msg)
            return {"success": False, "error": error_msg}

    @listen(write)
    def complete(self, write_result):
        """Mark flow as complete."""
        self.state.status = "complete"
        self.state.completed_at = datetime.now()

        duration = self.state.get_duration()

        print("\n" + "=" * 60)
        print("FLOW COMPLETE")
        print(f"Iterations: {self.state.iteration}")
        print(f"Duration: {duration:.1f}s" if duration else "")
        print(f"Output length: {len(self.state.final_output)} characters")
        print("=" * 60 + "\n")

        return {
            "status": "complete",
            "output": self.state.final_output,
            "duration": duration
        }

    @listen("fail")
    def handle_failure(self):
        """Handle flow failure."""
        self.state.status = "failed"
        self.state.completed_at = datetime.now()

        print("\n" + "=" * 60)
        print("FLOW FAILED")
        print(f"Iterations: {self.state.iteration}")
        print(f"Errors: {self.state.errors}")
        print("=" * 60 + "\n")

        return {
            "status": "failed",
            "errors": self.state.errors,
            "iterations": self.state.iteration
        }


# ============================================================================
# Alternative Flow Patterns
# ============================================================================

class ConditionalFlow(Flow[FlowState]):
    """
    Flow with conditional routing based on input classification.
    """

    @start()
    def classify(self):
        """Classify input to determine routing."""
        query = self.state.query.lower()

        if any(word in query for word in ["code", "programming", "api"]):
            self.state.classification = "technical"
        elif any(word in query for word in ["write", "article", "blog"]):
            self.state.classification = "creative"
        else:
            self.state.classification = "research"

        return self.state.classification

    @router(classify)
    def route(self) -> Literal["technical", "creative", "research"]:
        return self.state.classification

    @listen("technical")
    def handle_technical(self):
        return f"Technical handler for: {self.state.query}"

    @listen("creative")
    def handle_creative(self):
        return f"Creative handler for: {self.state.query}"

    @listen("research")
    def handle_research(self):
        return f"Research handler for: {self.state.query}"


class ParallelFlow(Flow[FlowState]):
    """
    Flow with parallel execution paths.
    """

    @start()
    def begin(self):
        return "started"

    @listen(begin)
    def path_a(self, data):
        """Runs in parallel."""
        time.sleep(1)
        return {"path": "a", "result": "done"}

    @listen(begin)
    def path_b(self, data):
        """Runs in parallel with path_a."""
        time.sleep(1)
        return {"path": "b", "result": "done"}

    @listen(path_a)
    @listen(path_b)
    def merge(self, result):
        """Called when either path completes."""
        return f"Received: {result}"


# ============================================================================
# Execution Helpers
# ============================================================================

def run_flow(
    flow_class,
    inputs: dict,
    max_retries: int = 3
) -> dict:
    """
    Execute a flow with error handling.

    Args:
        flow_class: Flow class to instantiate
        inputs: Input dictionary
        max_retries: Maximum retry attempts

    Returns:
        Result dictionary
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            flow = flow_class()
            result = flow.kickoff(inputs=inputs)
            return {
                "success": True,
                "result": result,
                "state": flow.state.model_dump(),
                "attempts": attempt + 1
            }
        except Exception as e:
            last_error = e
            error_msg = str(e).lower()

            retryable = any(err in error_msg for err in [
                "rate limit", "timeout", "connection"
            ])

            if retryable and attempt < max_retries - 1:
                delay = 2 ** attempt
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
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("Starting Research Flow...")

    result = run_flow(
        flow_class=ResearchFlow,
        inputs={"query": "Best practices for building production AI agents"},
        max_retries=3
    )

    if result["success"]:
        print(f"\n[SUCCESS] Completed in {result['attempts']} attempt(s)")
        print(f"\nFinal State:")
        print(f"  Status: {result['state']['status']}")
        print(f"  Output length: {len(result['state']['final_output'])} chars")
    else:
        print(f"\n[FAILED] Error: {result['error']}")
