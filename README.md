https://roadmap.sh/projects/caching-server
# Caching Proxy Server
A simple HTTP caching proxy built to understand **request forwarding, caching, and CLI tooling** from first principles.
This project focuses on **systems thinking**, not frameworks.

## 1. Objective

Build a local HTTP proxy server that:

* Receives HTTP requests
* Forwards them to an origin server
* Caches responses
* Returns cached responses for repeated requests

---

## 2. Requirements

The system must provide a **CLI command** that:

* Starts a local server
* Forwards incoming HTTP requests to another server
* Saves the response
* Returns the saved response if the same request occurs again

In short:

> “Don’t forward the same GET request twice.”

---

## 3. How to Run the Project

### Prerequisites

* Python 3.9+
* Virtual environment (recommended)

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the proxy server

```bash
python main.py --port 8000 --origin https://dummyjson.com
```

You should see output like:

```
Proxy starting on port 8000
Origin: https://dummyjson.com
```

### Example request

```bash
curl http://localhost:8000/products?limit=1
```

* First request → forwarded to origin (**cache MISS**)
* Second request → served from cache (**cache HIT**)

---

## 4. CLI Options

| Option          | Description                          |
| --------------- | ------------------------------------ |
| `--port`        | Port to run the proxy server         |
| `--origin`      | Origin server to forward requests to |
| `--clear-cache` | Clears the in-memory cache and exits |

Example:

```bash
python main.py --clear-cache
```

Output:

```
Cache cleared
```

---

## 5. The 4 Small Problems This Project Solves

### Problem 1: CLI

**Question:**
“How do I start something from the terminal?”

**Responsibilities:**

* Read `--port`
* Read `--origin`
* Read `--clear-cache`

---

### Problem 2: HTTP Server

**Question:**
“How do I listen on a port and receive requests?”

**Responsibilities:**

* Listen on `localhost:<port>`
* Receive:

  * path (`/products`)
  * method (`GET`)
  * headers

At this stage, the server can simply return:

```
Hello from proxy
```

---

### Problem 3: Forwarding Requests

**Question:**
“How do I send the same request to another server?”

**Responsibilities:**

* Take incoming request
* Reconstruct request using:

  * origin + path
  * method
  * query params
* Send request to origin
* Return response to client

👉 At this stage, the proxy works **without caching**.

---

### Problem 4: Caching

**Question:**
“How do I avoid forwarding the same request twice?”

**Responsibilities:**

* Create a cache
* Store responses
* Look up cached responses
* Return cached data if available

That’s it.

---

## 6. Correct Order to Build (Very Important)

### Step 1: CLI only

* Command runs
* Prints:

```
Proxy starting on port 3000
Origin: http://dummyjson.com
```

(No server yet.)

---

### Step 2: Server only

* Start server
* Always return:

```
Hello from proxy
```

(No forwarding.)

---

### Step 3: Forwarding only

* Request comes in
* Forward to origin
* Return response
* No caching

✅ At this point, you already have a working proxy.

---

### Step 4: Add cache

* Cache GET responses
* Key by full URL
* Return cached response if it exists

---

### Step 5: Add polish

* `X-Cache: HIT / MISS`
* `--clear-cache`
* Logs

---

## 7. Think in “Flow”, Not Code

Every request follows this flow:

```
Request arrives
↓
Is method GET?
↓
Generate cache key
↓
Is key in cache?
   ↓
   Yes → return cached response (X-Cache: HIT)
   No  → forward → cache → return (X-Cache: MISS)
```

---

## 8. Cache Design (Keep It Simple)

### Version 1 design

* Cache: in-memory dictionary
* Key: full URL (`/products?limit=10`)
* Value:

  * status code
  * headers
  * body
  * timestamp

TTL can be added later.

---

## 9. About `--clear-cache`

Simple interpretation:

* Cache is global
* `--clear-cache` empties it
* Program prints:

```
Cache cleared
```

---

## 10. What to Write Before Coding (Do This!)

Before writing code, define:

### 1. CLI Contract

```
caching-proxy --port <number> --origin <url>
caching-proxy --clear-cache
```

---

### 2. Cache Rules

* Cache GET requests only
* Key = path + query string
* In-memory storage

---

### 3. Known Limitations

* No HTTPS interception
* No cache-control headers
* No persistence across restarts

---

## 11. If You Feel Stuck, Ask This Question

> “What is the smallest thing I can build that moves me forward?”

Not:

> “How do I finish everything?”

But:

> “Can I forward **one** request?”

That mindset changes everything