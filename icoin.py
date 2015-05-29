#!/usr/bin/env python3

from waitress import serve

from icoin import app


HOST = "0.0.0.0"
PORT = "8080"
THREADS = "1"

if __name__ == "__main__":
    serve(app, host=HOST, port=PORT, threads=THREADS)
