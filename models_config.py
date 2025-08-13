"""
Free AI Models Configuration for GP Medical Assistant
Supporting multiple free model providers
"""

import os
from typing import Optional

# Hugging Face Models Configuration
HUGGINGFACE_MODELS = {
    "medical_llama": {
        "model_id": "microsoft/DialoGPT-medium",
        "description": "General conversation model",
        "max_tokens": 1000,
        "temperature": 0.7
    },
    "medical_mistral": {
        "model_id": "mistralai/Mistral-7B-Instruct-v0.1",
        "description": "Instruction-following model",
        "max_tokens": 1000,
        "temperature": 0.3
    },
    "medical_llama2": {
        "model_id": "meta-llama/Llama-2-7b-chat-hf",
        "description": "Meta's Llama 2 chat model",
        "max_tokens": 1000,
        "temperature": 0.3
    },
    "medical_zephyr": {
        "model_id": "HuggingFaceH4/zephyr-7b-beta",
        "description": "High-quality instruction model",
        "max_tokens": 1000,
        "temperature": 0.3
    },
    "medical_openchat": {
        "model_id": "openchat/openchat-3.5-1210",
        "description": "OpenChat conversation model",
        "max_tokens": 1000,
        "temperature": 0.3
    }
}

# Ollama Local Models (Free, runs locally)
OLLAMA_MODELS = {
    "llama2": {
        "model_name": "llama2:7b",
        "description": "Meta Llama 2 7B",
        "temperature": 0.3
    },
    "mistral": {
        "model_name": "mistral:7b",
        "description": "Mistral 7B",
        "temperature": 0.3
    },
    "codellama": {
        "model_name": "codellama:7b",
        "description": "Code Llama 7B",
        "temperature": 0.3
    },
    "medllama": {
        "model_name": "medllama2:7b",
        "description": "Medical Llama 2",
        "temperature": 0.3
    }
}

# OpenAI-Compatible Free APIs
FREE_APIS = {
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "description": "Together AI (Free tier available)"
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama2-70b-4096",
        "description": "Groq (Free tier available)"
    },
    "perplexity": {
        "base_url": "https://api.perplexity.ai",
        "model": "llama-2-7b-chat",
        "description": "Perplexity AI (Free tier)"
    }
}

def get_model_config(model_type: str = "huggingface", model_name: str = "medical_zephyr") -> dict:
    """Get configuration for specified model"""
    if model_type == "huggingface":
        return HUGGINGFACE_MODELS.get(model_name, HUGGINGFACE_MODELS["medical_zephyr"])
    elif model_type == "ollama":
        return OLLAMA_MODELS.get(model_name, OLLAMA_MODELS["llama2"])
    elif model_type == "free_api":
        return FREE_APIS.get(model_name, FREE_APIS["together"])
    else:
        return HUGGINGFACE_MODELS["medical_zephyr"]

def get_available_models() -> dict:
    """Get all available free models"""
    return {
        "huggingface": HUGGINGFACE_MODELS,
        "ollama": OLLAMA_MODELS,
        "free_apis": FREE_APIS
    }