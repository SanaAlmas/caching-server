import argparse
import requests
from flask import Flask, request, Response

app = Flask(__name__)

def fetch_from_origin(path):
    url = f"{app.config['ORIGIN']}/{path}"

    headers = {
        k: v
        for k, v in request.headers
        if k.lower() not in ("host", "accept-encoding")
    }

    headers["Accept-Encoding"] = "identity"

    return requests.request(
        method=request.method,
        url=url,
        headers=headers,
        params=request.args,
        data=request.get_data(),
    )

@app.route("/")
def home():
    return {"message": "Caching proxy is running"}

@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    origin_resp = fetch_from_origin(path)

    excluded_headers = {
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    }

    headers = [
        (name, value)
        for name, value in origin_resp.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(origin_resp.content, origin_resp.status_code, headers)

def start_server():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--origin", required=True)
    args = parser.parse_args()

    app.config["ORIGIN"] = args.origin.rstrip("/")

    print(f"Proxy running on port {args.port}")
    print(f"Forwarding to {app.config['ORIGIN']}")

    app.run(host="127.0.0.1", port=args.port)

if __name__ == "__main__":
    start_server()
