import argparse
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def start_server():
    parser = argparse.ArgumentParser(description="caching-proxy")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--origin", default="localhost/products", help="Directory to serve")
    args = parser.parse_args()
    app.run(host="127.0.0.1", port= args.port)
    print(f"Proxy starting on port {args.port}")
    print(f"Origin: {args.origin}")
