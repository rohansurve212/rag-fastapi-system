#!/usr/bin/env python3
"""
Test script for Phase 4 - Database Integration & Management
This script tests database operations, CRUD, and background processing
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


def create_test_text_file():
    """Create a temporary test text file"""
    content = """Artificial Intelligence and Machine Learning

Artificial Intelligence (AI) is revolutionizing technology. Machine learning enables computers to learn from data.

Deep learning uses neural networks to process complex patterns. These technologies are transforming industries worldwide.

Applications range from healthcare diagnostics to autonomous vehicles. The future of AI holds immense potential."""

    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write(content)
    temp_file.close()
    
    return Path(temp_file.name)


def test_database_connection():
    """Test database connection via health check"""
    print_section("Test 1: Database Connection")
    
    try:
        response = requests.get(f"{API_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Health check successful")
            print(f"  Status: {data.get('status')}")
            print(f"  Service: {data.get('service')}")
            print(f"  OpenAI Configured: {data.get('openai_configured')}")
            return data.get('status') == 'healthy'
        else:
            print_error(f"Health check failed (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False


def test_document_upload_with_db(test_file_path):
    """Test document upload with database storage"""
    print_section("Test 2: Document Upload with Database")
    
    try:
        print_info(f"Uploading file: {test_file_path.name}")
        
        with open(test_file_path, 'rb') as f:
            files = {'file': (test_file_path.name, f, 'text/plain')}
            response = requests.post(
                f"{API_URL}/api/v1/documents/upload",
                files=files
            )
        
        if response.status_code == 201:
            data = response.json()
            print_success("Document upload successful")
            print(f"\n  Document ID: {data.get('document_id')}")
            print(f"  Filename: {data.get('filename')}")
            print(f"  File Size: {data.get('file_size')} bytes")
            print(f"  File Hash: {data.get('file_hash')}")
            print(f"  Message: {data.get('message')}")
            
            return data.get('document_id')
        else:
            print_error(f"Upload failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Upload test failed: {str(e)}")
        return None


def test_document_retrieval(document_id):
    """Test retrieving document details"""
    print_section("Test 3: Document Retrieval")
    
    if not document_id:
        print_error("No document ID provided")
        return False
    
    try:
        print_info(f"Retrieving document: {document_id}")
        
        # Wait a bit for background processing
        print_info("Waiting 3 seconds for background processing...")
        time.sleep(3)
        
        response = requests.get(f"{API_URL}/api/v1/documents/{document_id}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Document retrieval successful")
            print(f"\n  Document ID: {data.get('document_id')}")
            print(f"  Filename: {data.get('filename')}")
            print(f"  Chunks Created: {data.get('chunks_created')}")
            print(f"  Message: {data.get('message')}")
            
            if data.get('metadata'):
                meta = data['metadata']
                print("\n  Metadata:")
                print(f"    Processing Status: {data.get('message')}")
                print(f"    Word Count: {meta.get('word_count')}")
                print(f"    Chunk Count: {meta.get('chunk_count')}")
            
            return True
        else:
            print_error(f"Retrieval failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Retrieval test failed: {str(e)}")
        return False


def test_document_chunks(document_id):
    """Test retrieving document chunks"""
    print_section("Test 4: Document Chunks Retrieval")
    
    if not document_id:
        print_error("No document ID provided")
        return False
    
    try:
        print_info(f"Retrieving chunks for document: {document_id}")
        
        # Wait a bit more for background processing to complete
        print_info("Waiting 5 seconds for chunk processing...")
        time.sleep(5)
        
        response = requests.get(f"{API_URL}/api/v1/documents/{document_id}/chunks")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Chunks retrieval successful")
            print(f"\n  Document ID: {data.get('document_id')}")
            print(f"  Chunk Count: {data.get('chunk_count')}")
            
            if data.get('chunks') and len(data['chunks']) > 0:
                print("\n  First Chunk:")
                first_chunk = data['chunks'][0]
                print(f"    Chunk ID: {first_chunk.get('chunk_id')}")
                print(f"    Index: {first_chunk.get('chunk_index')}")
                print(f"    Text Preview: {first_chunk.get('text')[:100]}...")
                
                if first_chunk.get('metadata'):
                    print(f"    Has Embedding: {first_chunk['metadata'].get('has_embedding')}")
            
            return data.get('chunk_count', 0) > 0
        else:
            print_error(f"Chunks retrieval failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Chunks test failed: {str(e)}")
        return False


def test_list_documents():
    """Test listing all documents"""
    print_section("Test 5: List Documents")
    
    try:
        print_info("Retrieving document list")
        
        response = requests.get(f"{API_URL}/api/v1/documents/")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Document list retrieval successful")
            print(f"\n  Total Documents: {data.get('total_count')}")
            
            if data.get('documents'):
                print(f"  Documents Retrieved: {len(data['documents'])}")
                
                if len(data['documents']) > 0:
                    print("\n  First Document:")
                    first_doc = data['documents'][0]
                    print(f"    Filename: {first_doc.get('filename')}")
                    print(f"    File Type: {first_doc.get('file_type')}")
                    print(f"    File Size: {first_doc.get('file_size')} bytes")
                    print(f"    Chunk Count: {first_doc.get('chunk_count')}")
            
            return True
        else:
            print_error(f"List failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"List test failed: {str(e)}")
        return False


def test_document_deletion(document_id):
    """Test document deletion"""
    print_section("Test 6: Document Deletion")
    
    if not document_id:
        print_error("No document ID provided")
        return False
    
    try:
        print_info(f"Deleting document: {document_id}")
        
        response = requests.delete(f"{API_URL}/api/v1/documents/{document_id}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Document deletion successful")
            print(f"  Message: {data.get('message')}")
            print(f"  Document ID: {data.get('document_id')}")
            
            # Verify deletion
            print_info("Verifying deletion...")
            verify_response = requests.get(f"{API_URL}/api/v1/documents/{document_id}")
            
            if verify_response.status_code == 404:
                print_success("Deletion verified (document not found)")
                return True
            else:
                print_error("Document still exists after deletion")
                return False
        else:
            print_error(f"Deletion failed (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Deletion test failed: {str(e)}")
        return False


def test_duplicate_detection():
    """Test duplicate document detection"""
    print_section("Test 7: Duplicate Detection")
    
    test_file_path = None
    try:
        # Create test file
        test_file_path = create_test_text_file()
        print_info("Uploading document first time...")
        
        # First upload
        with open(test_file_path, 'rb') as f:
            files = {'file': (test_file_path.name, f, 'text/plain')}
            response1 = requests.post(
                f"{API_URL}/api/v1/documents/upload",
                files=files
            )
        
        if response1.status_code != 201:
            print_error("First upload failed")
            return False
        
        doc1_id = response1.json().get('document_id')
        print_success(f"First upload successful: {doc1_id}")
        
        # Second upload (duplicate)
        print_info("Uploading same document again (should detect duplicate)...")
        with open(test_file_path, 'rb') as f:
            files = {'file': (test_file_path.name, f, 'text/plain')}
            response2 = requests.post(
                f"{API_URL}/api/v1/documents/upload",
                files=files
            )
        
        if response2.status_code == 201:
            data = response2.json()
            doc2_id = data.get('document_id')
            
            if doc1_id == doc2_id:
                print_success("Duplicate detected correctly")
                print(f"  Message: {data.get('message')}")
                print(f"  Same Document ID: {doc2_id}")
                
                # Cleanup
                requests.delete(f"{API_URL}/api/v1/documents/{doc1_id}")
                
                return True
            else:
                print_error("Duplicate not detected (different IDs)")
                # Cleanup both
                requests.delete(f"{API_URL}/api/v1/documents/{doc1_id}")
                requests.delete(f"{API_URL}/api/v1/documents/{doc2_id}")
                return False
        else:
            print_error(f"Second upload failed (HTTP {response2.status_code})")
            return False
            
    except Exception as e:
        print_error(f"Duplicate detection test failed: {str(e)}")
        return False
    finally:
        if test_file_path and test_file_path.exists():
            test_file_path.unlink()


def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}RAG System API - Phase 4 Tests{Colors.END}")
    print(f"Testing at: {API_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print_info("These tests include background processing and may take 10-15 seconds")
    
    # Create test file
    test_file_path = create_test_text_file()
    document_id = None
    
    try:
        # Run tests
        results = {}
        
        # Test 1: Database Connection
        results["Database Connection"] = test_database_connection()
        
        if not results["Database Connection"]:
            print_error("\n⚠ Database connection failed. Cannot proceed with other tests.")
            print_info("Make sure PostgreSQL container is running and healthy.")
            sys.exit(1)
        
        # Test 2: Upload with Database
        document_id = test_document_upload_with_db(test_file_path)
        results["Document Upload"] = document_id is not None
        
        # Test 3: Retrieval
        results["Document Retrieval"] = test_document_retrieval(document_id)
        
        # Test 4: Chunks
        results["Document Chunks"] = test_document_chunks(document_id)
        
        # Test 5: List
        results["List Documents"] = test_list_documents()
        
        # Test 6: Deletion
        results["Document Deletion"] = test_document_deletion(document_id)
        
        # Test 7: Duplicate Detection
        results["Duplicate Detection"] = test_duplicate_detection()
        
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
            print(f"\n{Colors.BLUE}Phase 4 is complete and working correctly!{Colors.END}\n")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed. Please check the output above.{Colors.END}\n")
            sys.exit(1)
            
    except Exception as e:
        print_error(f"Test suite error: {str(e)}")
        sys.exit(1)
    finally:
        # Cleanup
        if test_file_path and test_file_path.exists():
            test_file_path.unlink()


if __name__ == "__main__":
    main()