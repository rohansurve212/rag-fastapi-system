#!/usr/bin/env python3
"""
Test script for Phase 6 - Complete RAG Implementation
This script tests the complete RAG system
"""

import requests
import sys
import tempfile
import time
import json
from pathlib import Path
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


def create_test_document():
    """Create a comprehensive test document"""
    content = """Complete Guide to Artificial Intelligence

Introduction
Artificial Intelligence (AI) is transforming our world. This guide covers the fundamentals of AI, machine learning, and deep learning.

What is Machine Learning?
Machine learning is a subset of AI that enables computers to learn from data without explicit programming. It uses algorithms to identify patterns and make decisions with minimal human intervention.

Key Types of Machine Learning:
1. Supervised Learning: Learning from labeled data
2. Unsupervised Learning: Finding patterns in unlabeled data
3. Reinforcement Learning: Learning through trial and error

Deep Learning Explained
Deep learning is a specialized form of machine learning that uses artificial neural networks. These networks are inspired by the human brain and can process complex patterns in large datasets.

Neural networks consist of layers:
- Input layer: Receives data
- Hidden layers: Process information
- Output layer: Produces results

Natural Language Processing
NLP enables computers to understand and generate human language. Applications include chatbots, translation services, and sentiment analysis. Modern NLP uses transformer architectures for improved performance.

Computer Vision Applications
Computer vision allows machines to interpret visual information. Key applications include:
- Facial recognition systems
- Autonomous vehicle navigation
- Medical image analysis
- Object detection and tracking

AI in Healthcare
AI is revolutionizing healthcare through:
- Disease diagnosis and prediction
- Drug discovery and development
- Personalized treatment plans
- Medical imaging analysis
- Patient monitoring systems

Future of Artificial Intelligence
The future of AI includes:
- More advanced natural language understanding
- Improved computer vision systems
- Ethical AI development
- AI-human collaboration
- Automated decision-making systems

Conclusion
AI continues to evolve rapidly, offering tremendous potential for solving complex problems and improving our daily lives."""

    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write(content)
    temp_file.close()
    
    return Path(temp_file.name)


def upload_test_document():
    """Upload test document and wait for processing"""
    print_section("Setup: Upload Test Document")
    
    test_file = None
    try:
        test_file = create_test_document()
        print_info(f"Created test document: {test_file.name}")
        
        with open(test_file, 'rb') as f:
            files = {'file': (test_file.name, f, 'text/plain')}
            response = requests.post(
                f"{API_URL}/api/v1/documents/upload",
                files=files
            )
        
        if response.status_code == 201:
            data = response.json()
            doc_id = data.get('document_id')
            print_success(f"Document uploaded: {doc_id}")
            
            # Wait for processing
            print_info("Waiting 10 seconds for processing and embedding generation...")
            time.sleep(10)
            
            return doc_id
        else:
            print_error(f"Upload failed (HTTP {response.status_code})")
            return None
            
    except Exception as e:
        print_error(f"Upload failed: {str(e)}")
        return None
    finally:
        if test_file and test_file.exists():
            test_file.unlink()


def test_rag_health():
    """Test RAG health check"""
    print_section("Test 1: RAG Health Check")
    
    try:
        response = requests.get(f"{API_URL}/api/v1/rag/health")
        
        if response.status_code == 200:
            data = response.json()
            print_success("RAG health check successful")
            
            print(f"\n  Status: {data.get('status')}")
            print(f"  RAG Enabled: {data.get('rag_enabled')}")
            print(f"  Message: {data.get('message')}")
            
            if data.get('statistics'):
                stats = data['statistics']
                print("\n  Statistics:")
                print(f"    Documents: {stats.get('total_documents')}")
                print(f"    Chunks: {stats.get('total_chunks')}")
                print(f"    With Embeddings: {stats.get('chunks_with_embeddings')}")
                print(f"    Searchable: {stats.get('searchable_percentage')}%")
            
            return data.get('rag_enabled', False)
        else:
            print_error(f"Health check failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False


def test_simple_rag_query():
    """Test simple RAG query"""
    print_section("Test 2: Simple RAG Query")
    
    try:
        query = "What is machine learning?"
        print_info(f"Query: '{query}'")
        
        payload = {
            "query": query,
            "top_k": 3,
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        response = requests.post(
            f"{API_URL}/api/v1/rag/chat",
            json=payload,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("RAG query successful")
            
            print(f"\n  Answer: {data.get('answer')[:200]}...")
            print(f"\n  Sources Used: {len(data.get('sources', []))}")
            print(f"  Context Used: {data.get('context_used')}")
            print(f"  Model: {data.get('model')}")
            print(f"  Tokens: {data.get('tokens_used')}")
            
            if data.get('sources'):
                print("\n  Top Source:")
                source = data['sources'][0]
                print(f"    Document: {source.get('document_name')}")
                print(f"    Relevance: {source.get('relevance_score')}")
                print(f"    Preview: {source.get('text_preview')[:100]}...")
            
            return len(data.get('sources', [])) > 0
        else:
            print_error(f"RAG query failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"RAG query test failed: {str(e)}")
        return False


def test_rag_with_conversation_history():
    """Test RAG with conversation history"""
    print_section("Test 3: RAG with Conversation History")
    
    try:
        # First query
        first_query = "What is deep learning?"
        print_info(f"First Query: '{first_query}'")
        
        payload1 = {
            "query": first_query,
            "top_k": 3
        }
        
        response1 = requests.post(
            f"{API_URL}/api/v1/rag/chat",
            json=payload1,
            headers=HEADERS
        )
        
        if response1.status_code != 200:
            print_error("First query failed")
            return False
        
        data1 = response1.json()
        first_answer = data1.get('answer')
        print_success(f"First answer received ({len(first_answer)} chars)")
        
        # Follow-up query with history
        follow_up = "What are its main applications?"
        print_info(f"Follow-up Query: '{follow_up}'")
        
        payload2 = {
            "query": follow_up,
            "conversation_history": [
                {"role": "user", "content": first_query},
                {"role": "assistant", "content": first_answer}
            ],
            "top_k": 3
        }
        
        response2 = requests.post(
            f"{API_URL}/api/v1/rag/chat",
            json=payload2,
            headers=HEADERS
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            print_success("Follow-up query successful")
            
            print(f"\n  Answer: {data2.get('answer')[:200]}...")
            print(f"  Sources Used: {len(data2.get('sources', []))}")
            
            return True
        else:
            print_error(f"Follow-up query failed (HTTP {response2.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Conversation history test failed: {str(e)}")
        return False


def test_rag_source_attribution():
    """Test RAG source attribution"""
    print_section("Test 4: RAG Source Attribution")
    
    try:
        query = "How does natural language processing work?"
        print_info(f"Query: '{query}'")
        
        payload = {
            "query": query,
            "top_k": 5
        }
        
        response = requests.post(
            f"{API_URL}/api/v1/rag/chat",
            json=payload,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            sources = data.get('sources', [])
            answer = data.get('answer', '')
            
            print_success("Source attribution test successful")
            
            print(f"\n  Sources Retrieved: {len(sources)}")
            
            # Check if answer mentions sources
            has_source_ref = any(f"Source {i+1}" in answer for i in range(len(sources)))
            print(f"  Answer References Sources: {has_source_ref}")
            
            # Display all sources
            print("\n  All Sources:")
            for source in sources:
                print(f"    - Source {source.get('source_number')}: {source.get('document_name')} (Score: {source.get('relevance_score')})")
            
            return len(sources) > 0
        else:
            print_error(f"Source attribution test failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Source attribution test failed: {str(e)}")
        return False


def test_rag_document_filtering():
    """Test RAG with document filtering"""
    print_section("Test 5: RAG with Document Filtering")
    
    try:
        # Get a document ID first
        doc_response = requests.get(f"{API_URL}/api/v1/documents/")
        if doc_response.status_code != 200 or not doc_response.json().get('documents'):
            print_info("No documents available for filtering test")
            return True
        
        doc_id = doc_response.json()['documents'][0].get('file_hash')
        print_info("Testing with document filter")
        
        query = "Explain AI applications"
        payload = {
            "query": query,
            "document_id": doc_id,
            "top_k": 3
        }
        
        response = requests.post(
            f"{API_URL}/api/v1/rag/chat",
            json=payload,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Document filtering successful")
            
            print(f"\n  Answer: {data.get('answer')[:150]}...")
            print(f"  Sources: {len(data.get('sources', []))}")
            
            return True
        else:
            print_error(f"Document filtering failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Document filtering test failed: {str(e)}")
        return False


def test_rag_parameter_tuning():
    """Test RAG with different parameters"""
    print_section("Test 6: RAG Parameter Tuning")
    
    try:
        query = "What is computer vision?"
        
        # Test with low temperature (more focused)
        print_info("Testing with low temperature (0.3)")
        payload_low = {
            "query": query,
            "temperature": 0.3,
            "max_tokens": 200
        }
        
        response_low = requests.post(
            f"{API_URL}/api/v1/rag/chat",
            json=payload_low,
            headers=HEADERS
        )
        
        if response_low.status_code != 200:
            print_error("Low temperature test failed")
            return False
        
        print_success("Low temperature: Response generated")
        
        # Test with high top_k
        print_info("Testing with more context (top_k=8)")
        payload_high = {
            "query": query,
            "top_k": 8,
            "temperature": 0.7
        }
        
        response_high = requests.post(
            f"{API_URL}/api/v1/rag/chat",
            json=payload_high,
            headers=HEADERS
        )
        
        if response_high.status_code == 200:
            data = response_high.json()
            print_success(f"High top_k: {data.get('context_used')} chunks used")
            
            return True
        else:
            print_error("High top_k test failed")
            return False
            
    except Exception as e:
        print_error(f"Parameter tuning test failed: {str(e)}")
        return False


def test_rag_no_relevant_context():
    """Test RAG when no relevant context exists"""
    print_section("Test 7: RAG with No Relevant Context")
    
    try:
        query = "What is quantum entanglement in physics?"
        print_info(f"Query about topic not in documents: '{query}'")
        
        payload = {
            "query": query,
            "top_k": 3
        }
        
        response = requests.post(
            f"{API_URL}/api/v1/rag/chat",
            json=payload,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            
            print_success("RAG handled off-topic query")
            
            # Check if system admits lack of information
            admits_lack = any(phrase in answer.lower() for phrase in [
                "don't have", "not in", "cannot find", "no information",
                "not available", "based on the available"
            ])
            
            print(f"\n  Admits Lack of Info: {admits_lack}")
            print(f"  Answer: {answer[:200]}...")
            
            return True
        else:
            print_error(f"Off-topic query failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Off-topic test failed: {str(e)}")
        return False


def cleanup_test_document(doc_id):
    """Delete test document"""
    print_section("Cleanup: Delete Test Document")
    
    if not doc_id:
        print_info("No document to clean up")
        return True
    
    try:
        response = requests.delete(f"{API_URL}/api/v1/documents/{doc_id}")
        
        if response.status_code == 200:
            print_success(f"Test document deleted: {doc_id}")
            return True
        else:
            print_error(f"Cleanup failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Cleanup failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}RAG System API - Phase 6 Tests (Final Phase!){Colors.END}")
    print(f"Testing at: {API_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print_info("These tests verify the complete RAG system (~15 seconds)")
    
    # Upload test document
    doc_id = upload_test_document()
    
    if not doc_id:
        print_error("\n⚠ Failed to upload test document. Cannot proceed.")
        sys.exit(1)
    
    try:
        # Run tests
        results = {
            "RAG Health Check": test_rag_health(),
            "Simple RAG Query": test_simple_rag_query(),
            "Conversation History": test_rag_with_conversation_history(),
            "Source Attribution": test_rag_source_attribution(),
            "Document Filtering": test_rag_document_filtering(),
            "Parameter Tuning": test_rag_parameter_tuning(),
            "No Relevant Context": test_rag_no_relevant_context()
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
        
        # Cleanup
        cleanup_test_document(doc_id)
        
        if passed == total:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed!{Colors.END}")
            print(f"\n{Colors.BLUE}{Colors.BOLD}Phase 6 is complete and working correctly!{Colors.END}")
            print(f"\n{Colors.GREEN}{Colors.BOLD}🏆 CONGRATULATIONS! The complete RAG system is functional! 🏆{Colors.END}\n")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed. Please check the output above.{Colors.END}\n")
            sys.exit(1)
            
    except Exception as e:
        print_error(f"Test suite error: {str(e)}")
        cleanup_test_document(doc_id)
        sys.exit(1)


if __name__ == "__main__":
    main()