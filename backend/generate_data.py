print("PYTHON IS RUNNING")

import json
from datetime import datetime

data = {
    "message": "Hello from Python",
    "timestamp": datetime.now().isoformat()
}

with open("data/output.json", "w") as f:
    json.dump(data, f, indent=2)

print("Data generated")