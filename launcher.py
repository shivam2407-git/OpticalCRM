import subprocess
import threading
import time
import webbrowser
import socket
import sys
import os


def wait_for_server(host="127.0.0.1", port=8501, timeout=30):
    start = time.time()

    while time.time() - start < timeout:
        try:
            socket.create_connection((host, port), timeout=1).close()
            return True
        except OSError:
            time.sleep(0.5)

    return False


def run_streamlit():
    app = os.path.join(os.path.dirname(__file__), "app.py")

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            app,
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


threading.Thread(target=run_streamlit, daemon=True).start()

if wait_for_server():
    webbrowser.open("http://127.0.0.1:8501")

while True:
    time.sleep(1)