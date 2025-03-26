"""
Utility functions for the Efiko application
"""
import os
from typing import List
from datetime import datetime

def get_file_extension(filename: str) -> str:
    """Get the file extension from a filename."""
    return os.path.splitext(filename)[1].lower().lstrip('.')

def format_file_size(size_in_bytes: int) -> str:
    """Format file size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks of approximately equal size."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1  # +1 for space

        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks