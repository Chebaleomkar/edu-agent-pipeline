"""
Pipeline Module - Orchestrates the Agent Flow

Flow:
┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐
│  Generator  │────▶│  Reviewer   │────▶│  Pass? Done!        │
│   Agent     │     │   Agent     │     │  Fail? Refine once  │
└─────────────┘     └─────────────┘     └─────────────────────┘
"""

from dataclasses import dataclass
from typing import Optional
from agents import GeneratorAgent, ReviewerAgent


@dataclass
class PipelineResult:
    """Complete result from running the educational content pipeline."""
    grade: int
    topic: str
    initial_content: dict
    review_result: dict
    refined_content: Optional[dict] = None
    was_refined: bool = False


class EducationalContentPipeline:
    """
    Main pipeline orchestrating the Generator → Reviewer → Refinement flow.
    
    This pipeline:
    1. Generates initial content using the Generator Agent
    2. Reviews the content using the Reviewer Agent
    3. If review fails, refines content once with feedback
    """
    
    def __init__(self):
        """Initialize both agents."""
        self.generator = GeneratorAgent()
        self.reviewer = ReviewerAgent()
    
    def run(self, grade: int, topic: str) -> PipelineResult:
        """Execute the full pipeline."""
        # Step 1: Generate initial content
        initial_content = self.generator.generate_from_dict({
            "grade": grade,
            "topic": topic
        })
        
        # Step 2: Review the generated content
        review_result = self.reviewer.review_from_dict(
            generator_output=initial_content,
            grade=grade,
            topic=topic
        )
        
        # Step 3: Refinement (if needed - exactly ONE pass)
        refined_content = None
        was_refined = False
        
        if review_result["status"] == "fail" and review_result["feedback"]:
            refined_content = self.generator.generate_from_dict(
                data={"grade": grade, "topic": topic},
                feedback=review_result["feedback"]
            )
            was_refined = True
        
        return PipelineResult(
            grade=grade,
            topic=topic,
            initial_content=initial_content,
            review_result=review_result,
            refined_content=refined_content,
            was_refined=was_refined
        )


def generate_educational_content(grade: int, topic: str) -> PipelineResult:
    """Generate educational content for a given grade and topic."""
    pipeline = EducationalContentPipeline()
    return pipeline.run(grade, topic)
