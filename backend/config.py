"""
Configuration module for the Educational Content Generation System.

This module handles:
- Environment variable loading
- GROQ LLM (Llama) initialization
- Model configuration settings
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Validate API key exists
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please set it in your .env file.\n"
        "Get your key from: https://console.groq.com/keys"
    )

# Model configuration
MODEL_NAME = "llama-3.3-70b-versatile"  # Powerful Llama 3.3 model on GROQ
TEMPERATURE = 0.7  # Balanced creativity
MAX_TOKENS = 2048


def get_client() -> Groq:
    """
    Initialize and return the GROQ client.
    
    Returns:
        Groq: Configured GROQ client instance
    """
    return Groq(api_key=GROQ_API_KEY)


def generate_completion(prompt: str, system_prompt: str = None) -> str:
    """
    Generate a completion using GROQ Llama model.
    
    Args:
        prompt: The user prompt
        system_prompt: Optional system prompt for context
        
    Returns:
        str: Generated text response
    """
    client = get_client()
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    
    return response.choices[0].message.content
