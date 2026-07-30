import os
import sys
import time
import socket
import threading
import subprocess
import webbrowser


def resource_path(relative_path):
    """Get absolute path to bundled resource."""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def wait_for_server(host="127.0.0.1", port=8501, timeout=60):
    start = time.time()

    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)

    return False


def start_streamlit():
    app = resource_path("app.py")

    subprocess.Popen(
        [
            "streamlit",
            "run",
            app,
            "--server.headless=true",
            "--server.port=8501",
            "--browser.gatherUsageStats=false",
        ],
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


if __name__ == "__main__":
    threading.Thread(target=start_streamlit, daemon=True).start()

    if wait_for_server():
        webbrowser.open("http://127.0.0.1:8501")

    while True:
        time.sleep(1)