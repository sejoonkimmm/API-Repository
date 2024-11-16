import os
from app.database import Base, engine
from app.models import Todo, HealthCheck
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        logger.info("Check and Creating the tables.")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables are ready.")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

def main():
    init_db()
    
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()