#!/usr/bin/env python
"""Test semantic search API endpoint directly"""
import asyncio
import json
from pydantic import BaseModel, EmailStr
from routes_comprehensive import analyze_question
from database import SessionLocal

class AnalyzerQuestionRequest(BaseModel):
    email: str
    question: str

async def test_endpoint():
    """Test the analyzer endpoint directly without HTTP"""
    request = AnalyzerQuestionRequest(
        email="test@example.com",
        question="I am very angry at my family"
    )
    
    db = SessionLocal()
    
    try:
        result = await analyze_question(request, db=db)
        print("✓ TEST PASSED")
        print(f"Result: {json.dumps(result, indent=2, default=str)}")
    except Exception as e:
        print(f"✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_endpoint())
