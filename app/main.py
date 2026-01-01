import argparse

def start_server():
    parser = argparse.ArgumentParser(description="caching-proxy")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--origin", default=".", help="Directory to serve")
    args = parser.parse_args()
    print(f"Proxy starting on port {args.port}")
    print(f"Origin: {args.origin}")
