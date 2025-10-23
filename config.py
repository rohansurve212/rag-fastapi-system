from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Union


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Application Settings
    app_name: str = Field(default="RAG System API", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_reload: bool = Field(default=False, env="API_RELOAD")
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small", 
        env="OPENAI_EMBEDDING_MODEL"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://raguser:ragpassword@db:5432/ragdb",
        env="DATABASE_URL"
    )
    db_host: str = Field(default="db", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="ragdb", env="DB_NAME")
    db_user: str = Field(default="raguser", env="DB_USER")
    db_password: str = Field(default="ragpassword", env="DB_PASSWORD")
    
    # Upload Configuration
    max_upload_size: int = Field(default=10485760, env="MAX_UPLOAD_SIZE")  # 10MB
    allowed_extensions: Union[List[str], str] = Field(
        default=[".txt", ".pdf"],
        env="ALLOWED_EXTENSIONS"
    )
    upload_dir: str = Field(default="/app/uploads", env="UPLOAD_DIR")

    @field_validator('allowed_extensions', mode='before')
    @classmethod
    def parse_allowed_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(',')]
        return v
    
    # Vector Search Configuration
    embedding_dimension: int = Field(default=1536, env="EMBEDDING_DIMENSION")
    top_k_results: int = Field(default=5, env="TOP_K_RESULTS")
    
    # Chunking Configuration
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, env="CHUNK_OVERLAP")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()