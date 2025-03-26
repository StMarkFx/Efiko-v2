import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# API Configuration
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "Efiko"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Vector Search Configuration
VECTOR_SIMILARITY_THRESHOLD = 0.7
MAX_SEARCH_RESULTS = 5

# Document Processing
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_DOCUMENT_TYPES = ["pdf", "txt", "doc", "docx"]