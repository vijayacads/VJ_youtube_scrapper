"""
Launcher script for VJ Youtube Amaze
This is the entry point when running as an EXE file.
"""
import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

def get_app_path():
    """Get the application path - works for both EXE and script mode"""
    if getattr(sys, 'frozen', False):
        # Running as compiled EXE
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent

def start_server():
    """Start the FastAPI server"""
    app_path = get_app_path()
    os.chdir(app_path)
    
    # Add current directory to Python path
    if str(app_path) not in sys.path:
        sys.path.insert(0, str(app_path))
    
    try:
        import uvicorn
        from main import app
        print("=" * 60)
        print("VJ Youtube Amaze - Starting Server...")
        print("=" * 60)
        print("Server will be available at: http://localhost:8000")
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        print()
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(f"Error starting server: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to be ready
    print("Starting VJ Youtube Amaze...")
    time.sleep(4)
    
    # Open browser
    try:
        webbrowser.open('http://localhost:8000')
        print("\nBrowser opened automatically!")
        print("If browser didn't open, go to: http://localhost:8000")
    except:
        print("Could not open browser automatically.")
        print("Please open your browser and go to: http://localhost:8000")
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
