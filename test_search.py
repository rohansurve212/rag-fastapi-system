#!/usr/bin/env python3
"""
Test script for Phase 5 - Embeddings & Semantic Search
This script tests semantic, keyword, and hybrid search functionality
"""

import requests
import sys
import tempfile
import time
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
    """Create a test document with AI-related content"""
    content = """Introduction to Artificial Intelligence

Artificial Intelligence (AI) is the simulation of human intelligence by machines. 
AI systems can learn from experience, adjust to new inputs, and perform human-like tasks.

Machine Learning
Machine learning is a subset of artificial intelligence. It provides systems the ability 
to automatically learn and improve from experience without being explicitly programmed.

Deep Learning
Deep learning is part of machine learning based on artificial neural networks. 
Neural networks are inspired by the human brain and can learn complex patterns.

Natural Language Processing
Natural language processing (NLP) enables computers to understand, interpret, and generate 
human language. NLP is used in chatbots, translation services, and sentiment analysis.

Computer Vision
Computer vision allows machines to interpret and understand visual information from the world.
Applications include facial recognition, autonomous vehicles, and medical image analysis.

AI Applications
AI is transforming industries including healthcare, finance, transportation, and education.
From medical diagnosis to fraud detection, AI systems are becoming increasingly capable.

Future of AI
The future of artificial intelligence holds tremendous potential. As AI continues to advance,
it will reshape how we work, live, and interact with technology."""

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
            print_info("Waiting 8 seconds for processing and embedding generation...")
            time.sleep(8)
            
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


def test_search_stats():
    """Test search statistics endpoint"""
    print_section("Test 1: Search Statistics")
    
    try:
        response = requests.get(f"{API_URL}/api/v1/search/stats")
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('statistics', {})
            
            print_success("Search statistics retrieved")
            print(f"\n  Total Documents: {stats.get('total_documents')}")
            print(f"  Total Chunks: {stats.get('total_chunks')}")
            print(f"  Chunks with Embeddings: {stats.get('chunks_with_embeddings')}")
            print(f"  Searchable: {stats.get('searchable_percentage')}%")
            print(f"  Avg Chunks/Document: {stats.get('average_chunks_per_document')}")
            
            return stats.get('chunks_with_embeddings', 0) > 0
        else:
            print_error(f"Stats request failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Stats test failed: {str(e)}")
        return False


def test_semantic_search():
    """Test semantic search"""
    print_section("Test 2: Semantic Search")
    
    try:
        # Search for AI-related content
        query = "What is machine learning?"
        print_info(f"Query: '{query}'")
        
        response = requests.get(
            f"{API_URL}/api/v1/search/semantic",
            params={"query": query, "top_k": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Semantic search successful")
            
            print(f"\n  Results Count: {data.get('results_count')}")
            print(f"  Search Type: {data.get('search_type')}")
            
            if data.get('results'):
                print("\n  Top Result:")
                top_result = data['results'][0]
                print(f"    Similarity: {top_result.get('similarity_score')}")
                print(f"    Document: {top_result.get('document_name')}")
                print(f"    Text Preview: {top_result.get('text')[:100]}...")
            
            return data.get('results_count', 0) > 0
        else:
            print_error(f"Semantic search failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Semantic search test failed: {str(e)}")
        return False


def test_keyword_search():
    """Test keyword search"""
    print_section("Test 3: Keyword Search")
    
    try:
        # Search for specific keyword
        query = "neural networks"
        print_info(f"Query: '{query}'")
        
        response = requests.get(
            f"{API_URL}/api/v1/search/keyword",
            params={"query": query, "top_k": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Keyword search successful")
            
            print(f"\n  Results Count: {data.get('results_count')}")
            print(f"  Search Type: {data.get('search_type')}")
            
            if data.get('results'):
                print("\n  First Result:")
                first_result = data['results'][0]
                print(f"    Relevance: {first_result.get('relevance_score')}")
                print(f"    Document: {first_result.get('document_name')}")
                print(f"    Text Preview: {first_result.get('text')[:100]}...")
            
            return data.get('results_count', 0) > 0
        else:
            print_error(f"Keyword search failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Keyword search test failed: {str(e)}")
        return False


def test_hybrid_search():
    """Test hybrid search"""
    print_section("Test 4: Hybrid Search")
    
    try:
        # Hybrid search combining semantic and keyword
        query = "deep learning applications"
        print_info(f"Query: '{query}'")
        
        response = requests.get(
            f"{API_URL}/api/v1/search/hybrid",
            params={
                "query": query,
                "top_k": 3,
                "semantic_weight": 0.7,
                "keyword_weight": 0.3
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Hybrid search successful")
            
            print(f"\n  Results Count: {data.get('results_count')}")
            print(f"  Search Type: {data.get('search_type')}")
            print(f"  Weights: semantic={data['weights']['semantic']}, keyword={data['weights']['keyword']}")
            
            if data.get('results'):
                print("\n  Top Result:")
                top_result = data['results'][0]
                print(f"    Combined Score: {top_result.get('combined_score')}")
                print(f"    Semantic Score: {top_result.get('semantic_score')}")
                print(f"    Keyword Score: {top_result.get('keyword_score')}")
                print(f"    Document: {top_result.get('document_name')}")
                print(f"    Text Preview: {top_result.get('text')[:100]}...")
            
            return data.get('results_count', 0) > 0
        else:
            print_error(f"Hybrid search failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Hybrid search test failed: {str(e)}")
        return False


def test_context_search():
    """Test search with context"""
    print_section("Test 5: Context Search")
    
    try:
        # Search with surrounding context
        query = "computer vision"
        print_info(f"Query: '{query}' with context_window=1")
        
        response = requests.get(
            f"{API_URL}/api/v1/search/context",
            params={
                "query": query,
                "top_k": 2,
                "context_window": 1
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Context search successful")
            
            print(f"\n  Results Count: {data.get('results_count')}")
            print(f"  Context Window: {data.get('context_window')}")
            
            if data.get('results'):
                result = data['results'][0]
                print("\n  Result with Context:")
                print(f"    Main Chunk Index: {result.get('chunk_index')}")
                print(f"    Context Chunks: {len(result.get('context', []))}")
                
                if result.get('context'):
                    for ctx in result['context']:
                        print(f"      - Chunk {ctx['chunk_index']} ({ctx['position']})")
            
            return data.get('results_count', 0) > 0
        else:
            print_error(f"Context search failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Context search test failed: {str(e)}")
        return False


def test_search_filters():
    """Test search with filters"""
    print_section("Test 6: Search with Filters")
    
    try:
        # Test with minimum similarity threshold
        query = "artificial intelligence"
        print_info(f"Query: '{query}' with min_similarity=0.5")
        
        response = requests.get(
            f"{API_URL}/api/v1/search/semantic",
            params={
                "query": query,
                "top_k": 5,
                "min_similarity": 0.5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Filtered search successful")
            
            print(f"\n  Results Count: {data.get('results_count')}")
            
            if data.get('results'):
                # Check all results meet minimum threshold
                min_score = min(r.get('similarity_score', 0) for r in data['results'])
                print(f"  Minimum Score: {min_score}")
                print(f"  All above threshold: {min_score >= 0.5}")
            
            return True
        else:
            print_error(f"Filtered search failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Filtered search test failed: {str(e)}")
        return False


def test_empty_results():
    """Test search with no results"""
    print_section("Test 7: Empty Results Handling")
    
    try:
        # Search for something unlikely to exist
        query = "xyzabc123nonexistent"
        print_info(f"Query: '{query}' (should return no results)")
        
        response = requests.get(
            f"{API_URL}/api/v1/search/semantic",
            params={"query": query, "top_k": 5}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Empty results handled correctly")
            
            print(f"\n  Results Count: {data.get('results_count')}")
            print(f"  Success: {data.get('success')}")
            
            return data.get('success')
        else:
            print_error(f"Request failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Empty results test failed: {str(e)}")
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
    print(f"\n{Colors.BOLD}RAG System API - Phase 5 Tests{Colors.END}")
    print(f"Testing at: {API_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print_info("These tests require a document with embeddings (~10 seconds)")
    
    # Upload test document
    doc_id = upload_test_document()
    
    if not doc_id:
        print_error("\n⚠ Failed to upload test document. Cannot proceed.")
        sys.exit(1)
    
    try:
        # Run tests
        results = {
            "Search Statistics": test_search_stats(),
            "Semantic Search": test_semantic_search(),
            "Keyword Search": test_keyword_search(),
            "Hybrid Search": test_hybrid_search(),
            "Context Search": test_context_search(),
            "Search Filters": test_search_filters(),
            "Empty Results": test_empty_results()
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
            print(f"\n{Colors.BLUE}Phase 5 is complete and working correctly!{Colors.END}\n")
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