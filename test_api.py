#!/usr/bin/env python3
"""
Test script to verify Google Gemini API connection
"""

from dotenv import load_dotenv
load_dotenv()

import os
from langchain_google_genai import ChatGoogleGenerativeAI

def test_api():
    """Test the Google Gemini API connection"""
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ No API key found in environment")
            return False
        
        print(f"✅ API key found: {api_key[:10]}...")
        
        # Test the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            max_output_tokens=100
        )
        
        response = llm.invoke("Hello, can you help with medical questions?")
        print(f"✅ API connection successful!")
        print(f"Response: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == '__main__':
    test_api()