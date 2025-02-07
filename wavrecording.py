from flask import Flask, request, jsonify
import subprocess
import os
import time
import datetime
import signal

app = Flask(__name__)

RECORDING_DIR = "recorded_conversation"
CHUNK_DURATION = 300  # 5 minutes in seconds
RECORDING_PROCESS = None

# Create the recording directory if it doesn't exist
if not os.path.exists(RECORDING_DIR):
    os.makedirs(RECORDING_DIR)

def start_recording():
    global RECORDING_PROCESS
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(RECORDING_DIR, f"recording_{timestamp}.wav")

    # Use `rec` command for recording on macOS.  Ensure SoX is installed: `brew install sox`
    command = [
        "rec",
        "-r", "16000",  # Sample rate 16kHz
        "-c", "1",       # Mono channel
        filename,
        "silence", "1", "0.1", "1", "1", "0.1", "1" # Stop recording if silence is detected
    ]

    try:
      RECORDING_PROCESS = subprocess.Popen(command, preexec_fn=os.setsid) # setsid is used to kill the child process correctly
      print(f"Recording started to {filename} (PID: {RECORDING_PROCESS.pid})")
      return True, "Recording started"
    except Exception as e:
      print(f"Error starting recording: {e}")
      return False, f"Error starting recording: {e}"


def stop_recording():
    global RECORDING_PROCESS
    if RECORDING_PROCESS:
      try:
        os.killpg(os.getpgid(RECORDING_PROCESS.pid), signal.SIGTERM) # kill the process group
        RECORDING_PROCESS = None
        print("Recording stopped.")
        return True, "Recording stopped"
      except ProcessLookupError:
        print("No recording process to stop.")
        RECORDING_PROCESS = None # Reset in case the process already ended
        return True, "No recording process to stop"  # or False, "No recording process to stop" depending on error handling
      except Exception as e:
        print(f"Error stopping recording: {e}")
        return False, f"Error stopping recording: {e}"
    else:
      return True, "No recording in progress"


@app.route('/start_recording', methods=['POST'])
def start_recording_api():
    success, message = start_recording()
    return jsonify({"status": "success" if success else "error", "message": message})


@app.route('/stop_recording', methods=['POST'])
def stop_recording_api():
    success, message = stop_recording()
    return jsonify({"status": "success" if success else "error", "message": message})

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production
