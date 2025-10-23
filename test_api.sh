#!/bin/bash

# API Testing Script for Phase 1
# This script tests all endpoints created in Phase 1

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  RAG System API - Phase 1 Tests${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Function to test an endpoint
test_endpoint() {
    local endpoint=$1
    local description=$2
    
    echo -e "${BLUE}Testing: ${description}${NC}"
    echo -e "Endpoint: ${endpoint}\n"
    
    response=$(curl -s -w "\n%{http_code}" "${API_URL}${endpoint}")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✓ Success (HTTP ${http_code})${NC}"
        echo -e "Response:\n${body}\n"
    else
        echo -e "${RED}✗ Failed (HTTP ${http_code})${NC}"
        echo -e "Response:\n${body}\n"
    fi
    
    echo -e "----------------------------------------\n"
}

# Wait for API to be ready
echo -e "${BLUE}Waiting for API to be ready...${NC}\n"
sleep 2

# Test 1: Root endpoint
test_endpoint "/" "Root Endpoint - Welcome Message"

# Test 2: Health check
test_endpoint "/health" "Health Check Endpoint"

# Test 3: API status
test_endpoint "/api/v1/status" "API Status Endpoint"

# Test 4: OpenAPI docs (just check if accessible)
echo -e "${BLUE}Testing: OpenAPI Documentation${NC}"
echo -e "Endpoint: /docs\n"

docs_response=$(curl -s -o /dev/null -w "%{http_code}" "${API_URL}/docs")

if [ "$docs_response" -eq 200 ]; then
    echo -e "${GREEN}✓ API Documentation is accessible${NC}"
    echo -e "Visit: ${API_URL}/docs\n"
else
    echo -e "${RED}✗ API Documentation is not accessible (HTTP ${docs_response})${NC}\n"
fi

echo -e "----------------------------------------\n"

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "API URL: ${API_URL}"
echo -e "Documentation: ${API_URL}/docs"
echo -e "Alternative Docs: ${API_URL}/redoc"
echo -e "\n${GREEN}Phase 1 testing complete!${NC}\n"