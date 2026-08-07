"""
Root Entry Point for Disease Prediction System.
Launches the FastAPI production backend server.
"""

import sys
import os
import uvicorn

# Add root folder to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from backend.app.config.settings import settings
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Server documentation available at: http://localhost:{settings.PORT}/docs")
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)