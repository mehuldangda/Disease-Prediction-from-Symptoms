"""
Entry script to launch the FastAPI backend server.
"""

import sys
import os
import uvicorn

# Add root folder to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.app.config.settings import settings

if __name__ == "__main__":
    print(f"Launching {settings.APP_NAME} on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
