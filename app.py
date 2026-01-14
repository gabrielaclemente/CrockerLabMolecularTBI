import os
import webbrowser
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# Route for the home page
@app.route("/")
def home():
    timestamp = datetime.now().isoformat()
    return render_template("index.html", timestamp=timestamp)


if __name__ == "__main__":
    # Only open the browser if we're in the main process (avoids multiple tabs in debug mode)
    if os.environ.get("WERKZEUG_RUN_MAIN") is None:
        webbrowser.open("http://127.0.0.1:5000")
    
    # Start Flask dev server with auto-reload
    app.run(debug=True)