from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import logging
from config import settings
from database.models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database connection manager with connection pooling
    """
    
    def __init__(self):
        """
        Initialize database connection with pooling
        """
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """
        Create database engine with connection pooling
        """
        try:
            # Create engine with connection pooling
            self.engine = create_engine(
                settings.database_url,
                poolclass=QueuePool,
                pool_size=5,  # Number of connections to keep open
                max_overflow=10,  # Max connections that can be created beyond pool_size
                pool_timeout=30,  # Timeout for getting connection from pool
                pool_recycle=3600,  # Recycle connections after 1 hour
                pool_pre_ping=True,  # Verify connections before using them
                echo=False  # Set to True for SQL query logging
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("Database engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {str(e)}")
            raise
    
    def create_tables(self):
        """
        Create all tables defined in models
        """
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {str(e)}")
            raise
    
    def drop_tables(self):
        """
        Drop all tables (use with caution!)
        """
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.warning("All database tables dropped")
        except Exception as e:
            logger.error(f"Failed to drop tables: {str(e)}")
            raise
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions
        
        Usage:
            with db_manager.get_session() as session:
                # Use session here
                pass
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_db(self) -> Generator[Session, None, None]:
        """
        Dependency for FastAPI to get database sessions
        
        Usage in FastAPI:
            @app.get("/items")
            def get_items(db: Session = Depends(get_db)):
                # Use db here
                pass
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """
        Test database connection
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                # Test pgvector extension
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
                
                # Test pgvector is installed
                result = conn.execute(
                    text("SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector'")
                )
                vector_installed = result.fetchone()[0] > 0
                
                if not vector_installed:
                    logger.warning("pgvector extension is not installed")
                    return False
                
                logger.info("Database connection test successful")
                return True
                
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False
    
    def execute_sql_file(self, file_path: str):
        """
        Execute SQL commands from a file
        
        Args:
            file_path: Path to SQL file
        """
        try:
            with open(file_path, 'r') as f:
                sql_content = f.read()
            
            with self.engine.connect() as conn:
                # Split by semicolon and execute each statement
                statements = sql_content.split(';')
                for statement in statements:
                    statement = statement.strip()
                    if statement:
                        conn.execute(text(statement))
                conn.commit()
            
            logger.info(f"Successfully executed SQL file: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to execute SQL file: {str(e)}")
            raise
    
    def get_table_count(self, table_name: str) -> int:
        """
        Get row count for a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Number of rows in the table
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table_name}")
                )
                count = result.fetchone()[0]
                return count
        except Exception as e:
            logger.error(f"Failed to get table count: {str(e)}")
            return 0
    
    def close(self):
        """
        Close database connection and dispose of engine
        """
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


# Create global database manager instance
db_manager = DatabaseManager()


# Dependency for FastAPI
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get database session
    """
    session = db_manager.SessionLocal()
    try:
        yield session
    finally:
        session.close()