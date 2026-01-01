#!/usr/bin/env python3
import http.server
import socketserver
import argparse
import os

def start_server(port, origin):
    print(f"Proxy starting on port {port}")
    print(f"Origin: {origin}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="caching-proxy")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--origin", default=".", help="Directory to serve")
    args = parser.parse_args()

    start_server(args.port, args.origin)
