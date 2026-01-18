import argparse
import requests
from flask import Flask, request, Response

app = Flask(__name__)

cache = {}
def fetch_from_origin(path):
    url = f"{app.config['ORIGIN']}/{path}"

    headers = {
        k: v
        for k, v in request.headers
        if k.lower() not in ("host", "accept-encoding")
    }
    # print(headers)
    headers["Accept-Encoding"] = "identity"
    print(headers)
    print(f"method - {request.method}")
    print(f"params - {request.args}")
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
    url = f"{app.config['ORIGIN']}/{path}"
    if url in cache:
        cached_resp = cache[url]

        return Response(
            cached_resp["body"],
            mimetype="application/json",
            status=200
        )

    else:
        origin_resp = fetch_from_origin(path)
        cache[url] = {
            "body": origin_resp.content,
            "status": origin_resp.status_code,
            # headers optional for now
        }

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

    app.run(host="127.0.0.1", port=args.port, debug=True, use_reloader=False)

if __name__ == "__main__":
    start_server()
