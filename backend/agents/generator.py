"""
Generator Agent Module

Responsibility: Generate educational content for a given grade and topic.

The Generator Agent creates age-appropriate explanations and multiple-choice
questions (MCQs) based on the specified grade level and subject topic.
"""

import json
import re
from typing import Optional
from pydantic import BaseModel, Field

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import generate_completion


# ============================================================================
# Data Models (Structured Input/Output)
# ============================================================================

class GeneratorInput(BaseModel):
    """Structured input for the Generator Agent."""
    grade: int = Field(..., ge=1, le=12, description="Student grade level (1-12)")
    topic: str = Field(..., min_length=1, description="Educational topic to cover")


class MCQ(BaseModel):
    """Multiple Choice Question structure."""
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    answer: str = Field(..., pattern=r"^[ABCD]$")


class GeneratorOutput(BaseModel):
    """Structured output from the Generator Agent."""
    explanation: str
    mcqs: list[MCQ]


# ============================================================================
# Generator Agent Implementation
# ============================================================================

class GeneratorAgent:
    """
    Agent responsible for generating educational content.
    
    This agent uses GROQ's Llama model to create grade-appropriate explanations
    and multiple-choice questions for any given topic.
    """
    
    def __init__(self):
        """Initialize the Generator Agent."""
        pass
    
    def _build_prompt(
        self, 
        grade: int, 
        topic: str, 
        feedback: Optional[list[str]] = None
    ) -> str:
        """
        Build the generation prompt for the LLM.
        
        Args:
            grade: Student grade level
            topic: Topic to generate content for
            feedback: Optional reviewer feedback for refinement
            
        Returns:
            Formatted prompt string
        """
        grade_guidelines = {
            (1, 3): "Use very simple words and short sentences. Be playful and fun.",
            (4, 6): "Use clear, straightforward language. Include relatable examples.",
            (7, 9): "Use standard academic language. Include more detailed explanations.",
            (10, 12): "Use sophisticated vocabulary. Include technical terms with context.",
        }
        
        language_guide = ""
        for (low, high), guide in grade_guidelines.items():
            if low <= grade <= high:
                language_guide = guide
                break
        
        prompt = f"""Generate educational content for:

**Grade Level:** {grade}
**Topic:** {topic}

**Language Guidelines:** {language_guide}

**Instructions:**
1. Create a clear, age-appropriate explanation of the topic (2-4 paragraphs)
2. Generate exactly 3 multiple-choice questions (MCQs)
3. Each MCQ must have exactly 4 options labeled A, B, C, D
4. Ensure concepts are accurate and appropriate for the grade level

"""
        
        if feedback:
            feedback_text = "\n".join(f"- {fb}" for fb in feedback)
            prompt += f"""
**IMPORTANT - Address this feedback from the reviewer:**
{feedback_text}

Please regenerate the content addressing ALL feedback points above.

"""
        
        prompt += """**Output Format:**
Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks, no extra text):
{
    "explanation": "<detailed explanation appropriate for the grade>",
    "mcqs": [
        {
            "question": "<question text>",
            "options": ["A. <option>", "B. <option>", "C. <option>", "D. <option>"],
            "answer": "<A, B, C, or D>"
        },
        {
            "question": "<question text>",
            "options": ["A. <option>", "B. <option>", "C. <option>", "D. <option>"],
            "answer": "<A, B, C, or D>"
        },
        {
            "question": "<question text>",
            "options": ["A. <option>", "B. <option>", "C. <option>", "D. <option>"],
            "answer": "<A, B, C, or D>"
        }
    ]
}
"""
        return prompt
    
    def _parse_response(self, response_text: str) -> GeneratorOutput:
        """Parse the LLM response into structured output."""
        cleaned = response_text.strip()
        
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        json_match = re.search(r'\{[\s\S]*\}', cleaned)
        if json_match:
            cleaned = json_match.group()
        
        try:
            data = json.loads(cleaned)
            return GeneratorOutput(**data)
        except (json.JSONDecodeError, Exception) as e:
            raise ValueError(f"Failed to parse LLM response: {e}")
    
    def generate(
        self, 
        input_data: GeneratorInput, 
        feedback: Optional[list[str]] = None
    ) -> GeneratorOutput:
        """Generate educational content for the given input."""
        prompt = self._build_prompt(
            grade=input_data.grade,
            topic=input_data.topic,
            feedback=feedback
        )
        
        system_prompt = "You are an expert educational content creator. Always respond with valid JSON only."
        response = generate_completion(prompt, system_prompt)
        
        return self._parse_response(response)
    
    def generate_from_dict(
        self, 
        data: dict, 
        feedback: Optional[list[str]] = None
    ) -> dict:
        """Convenience method to generate from dict and return dict."""
        input_data = GeneratorInput(**data)
        output = self.generate(input_data, feedback=feedback)
        return output.model_dump()
