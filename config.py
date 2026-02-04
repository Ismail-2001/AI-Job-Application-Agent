import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration for the AI Job Agent."""
    
    # Flask & Security
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///local_agent.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Search & Generation
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    EMBEDDING_MODEL = "models/text-embedding-004"
    
    # App Settings
    OUTPUT_DIR = os.path.join(os.getcwd(), "output")
    MAX_WORKERS = 4

    @classmethod
    def validate(cls):
        """Ensure critical environment variables are present."""
        missing = []
        if not cls.DEEPSEEK_API_KEY:
            missing.append("DEEPSEEK_API_KEY")
        if not cls.GOOGLE_API_KEY:
            missing.append("GOOGLE_API_KEY")
        
        if missing:
            raise ValueError(f"❌ Missing critical environment variables: {', '.join(missing)}")
