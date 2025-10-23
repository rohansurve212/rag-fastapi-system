#!/usr/bin/env python3
"""
Test script for Phase 2 - Chat Endpoint
This script tests the OpenAI integration and chat functionality
"""

import requests
import sys
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}\n")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")


def test_openai_connection():
    """Test OpenAI API connection"""
    print_section("Test 1: OpenAI Connection Test")
    
    try:
        response = requests.get(f"{API_URL}/api/v1/chat/test")
        
        if response.status_code == 200:
            data = response.json()
            print_success("OpenAI connection successful")
            print(f"  Model: {data.get('model')}")
            print(f"  Embedding Model: {data.get('embedding_model')}")
            print(f"  Status: {data.get('status')}")
            return True
        else:
            print_error(f"Connection test failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Connection test failed: {str(e)}")
        return False


def test_simple_chat():
    """Test simple chat without conversation history"""
    print_section("Test 2: Simple Chat Request")
    
    payload = {
        "message": "What is FastAPI in one sentence?",
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        print_info(f"Sending message: {payload['message']}")
        response = requests.post(
            f"{API_URL}/api/v1/chat/",
            json=payload,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Chat request successful")
            print(f"\n  Response: {data['response']}")
            print(f"  Model: {data['model']}")
            print(f"  Tokens Used: {data['tokens_used']}")
            print(f"  Message Count: {data['message_count']}")
            return True
        else:
            print_error(f"Chat request failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Chat request failed: {str(e)}")
        return False


def test_chat_with_history():
    """Test chat with conversation history"""
    print_section("Test 3: Chat with Conversation History")
    
    payload = {
        "message": "What did I just ask you about?",
        "conversation_history": [
            {
                "role": "user",
                "content": "Tell me about Python"
            },
            {
                "role": "assistant",
                "content": "Python is a high-level programming language known for its simplicity and readability."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        print_info("Sending message with conversation history")
        response = requests.post(
            f"{API_URL}/api/v1/chat/",
            json=payload,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Chat with history successful")
            print(f"\n  Response: {data['response']}")
            print(f"  Message Count: {data['message_count']}")
            print(f"  Tokens Used: {data['tokens_used']}")
            return True
        else:
            print_error(f"Chat with history failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Chat with history failed: {str(e)}")
        return False


def test_temperature_variation():
    """Test different temperature settings"""
    print_section("Test 4: Temperature Variation")
    
    temperatures = [0.0, 0.5, 1.0]
    question = "Say hello in a creative way"
    
    all_passed = True
    for temp in temperatures:
        payload = {
            "message": question,
            "temperature": temp,
            "max_tokens": 50
        }
        
        try:
            print_info(f"Testing with temperature={temp}")
            response = requests.post(
                f"{API_URL}/api/v1/chat/",
                json=payload,
                headers=HEADERS
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Temperature {temp} successful")
                print(f"  Response: {data['response'][:80]}...")
            else:
                print_error(f"Temperature {temp} failed (HTTP {response.status_code})")
                all_passed = False
                
        except Exception as e:
            print_error(f"Temperature {temp} failed: {str(e)}")
            all_passed = False
    
    return all_passed


def test_error_handling():
    """Test error handling with invalid requests"""
    print_section("Test 5: Error Handling")
    
    # Test with empty message
    payload = {
        "message": "",
        "temperature": 0.7
    }
    
    try:
        print_info("Testing with empty message (should fail)")
        response = requests.post(
            f"{API_URL}/api/v1/chat/",
            json=payload,
            headers=HEADERS
        )
        
        if response.status_code in [400, 422]:
            print_success("Error handling works correctly (rejected empty message)")
            return True
        else:
            print_error(f"Expected error but got HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error handling test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}RAG System API - Phase 2 Tests{Colors.END}")
    print(f"Testing at: {API_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Wait for API to be ready
    print_info("Waiting for API to be ready...")
    
    # Run tests
    results = {
        "OpenAI Connection": test_openai_connection(),
        "Simple Chat": test_simple_chat(),
        "Chat with History": test_chat_with_history(),
        "Temperature Variation": test_temperature_variation(),
        "Error Handling": test_error_handling()
    }
    
    # Print summary
    print_section("Test Summary")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    for test_name, passed_test in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.END}" if passed_test else f"{Colors.RED}FAILED{Colors.END}"
        print(f"{test_name}: {status}")
    
    print(f"\n{Colors.BOLD}Total: {total} | Passed: {Colors.GREEN}{passed}{Colors.END} | Failed: {Colors.RED}{failed}{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed!{Colors.END}")
        print(f"\n{Colors.BLUE}Phase 2 is complete and working correctly!{Colors.END}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed. Please check the output above.{Colors.END}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()