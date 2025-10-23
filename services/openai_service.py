from openai import OpenAI, OpenAIError
from typing import List, Dict
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIService:
    """
    Service class for interacting with OpenAI API
    """
    
    def __init__(self):
        """
        Initialize OpenAI client with API key from settings
        """
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY in .env file")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.embedding_model = settings.openai_embedding_model
        logger.info(f"OpenAI service initialized with model: {self.model}")
    
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Dict:
        """
        Generate a chat completion using OpenAI's API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0 to 2.0)
            max_tokens: Maximum tokens in the response
            
        Returns:
            Dictionary containing response text and metadata
            
        Raises:
            OpenAIError: If the API request fails
        """
        try:
            logger.info(f"Generating chat completion with {len(messages)} messages")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract response data
            result = {
                "response": response.choices[0].message.content,
                "model": response.model,
                "tokens_used": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason
            }
            
            logger.info(f"Chat completion successful. Tokens used: {result['tokens_used']}")
            return result
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in chat completion: {str(e)}")
            raise
    
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding vector for the given text
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
            
        Raises:
            OpenAIError: If the API request fails
        """
        try:
            logger.info(f"Creating embedding for text of length {len(text)}")
            
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            embedding = response.data[0].embedding
            logger.info(f"Embedding created successfully. Dimension: {len(embedding)}")
            
            return embedding
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error while creating embedding: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in create_embedding: {str(e)}")
            raise
    
    
    def create_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Create embeddings for multiple texts with automatic batching

        OpenAI's embedding API has limits:
        - Max 300,000 tokens per request
        - We use conservative batch_size to avoid hitting limits

        Args:
            texts: List of texts to embed
            batch_size: Number of texts per API call (default: 100)

        Returns:
            List of embedding vectors

        Raises:
            OpenAIError: If the API request fails
        """
        try:
            logger.info(f"Creating embeddings for {len(texts)} texts in batches of {batch_size}")

            all_embeddings = []

            # Process in batches
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (len(texts) + batch_size - 1) // batch_size

                logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} texts)")

                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch
                )

                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

            logger.info(f"Batch embeddings created successfully: {len(all_embeddings)} total")
            return all_embeddings

        except OpenAIError as e:
            logger.error(f"OpenAI API error while creating batch embeddings: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in create_embeddings_batch: {str(e)}")
            raise
    
    
    def test_connection(self) -> bool:
        """
        Test if the OpenAI API connection is working
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try a simple completion with minimal tokens
            test_messages = [
                {"role": "user", "content": "Hi"}
            ]
            
            _ = self.client.chat.completions.create(
                model=self.model,
                messages=test_messages,
                max_tokens=5
            )
            
            logger.info("OpenAI connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {str(e)}")
            return False


# Create a singleton instance
openai_service = OpenAIService()