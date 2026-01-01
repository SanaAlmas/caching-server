1. Objective

request forwarding, caching, and CLI tooling.

2. Requirement
I need a terminal command that starts a local server.
That server receives HTTP requests, forwards them to another server, saves the response, and 
if the same request happens again, returns the saved response instead of forwarding it.”

3. 4 small problems
Problem 1: CLI

“How do I start something from the terminal?”

Read --port
Read --origin
Read --clear-cache

Problem 2: HTTP Server

“How do I listen on a port and receive requests?”

Listen on localhost:<port>
Receive:
path (/products)
method (GET)
headers

Problem 3: Forwarding Requests

“How do I send the same request to another server?”

Take incoming request
Reconstruct it for origin + path
Send request
Return response to client

👉 At this stage, your proxy works without cache.

Problem 4: Caching

“How do I avoid forwarding the same request twice?”

Create a cache
Store response
Look it up next time
That’s it.

4. The correct order to build (very important)
Step 1: CLI only
Command runs
Prints:
Proxy starting on port 3000
Origin: http://dummyjson.com
No server yet.

Step 2: Server only
Start server
Always return:
Hello from proxy
No forwarding.

Step 3: Forwarding only
Request comes in
Forward to origin
Return response
No caching.

✅ At this point, you already have a working proxy.

Step 4: Add cache
Cache GET responses
Key by URL
Return cached response if exists

Step 5: Add polish
X-Cache: HIT / MISS
--clear-cache
Logs

5. Think in “flow”, not code

Every request follows this flow:
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

6. Cache design (keep it simple)
For version 1:
Cache = in-memory map
Key = full URL (/products?limit=10)
Value =
status code
headers
body
timestamp
TTL can be optional at first.

7. About --clear-cache
Simple interpretation:
Cache is global
--clear-cache empties it
Print:
Cache cleared

8. What to write before coding (do this!)

Create a small document or notes with:

1. CLI contract
caching-proxy --port <number> --origin <url>
caching-proxy --clear-cache

2. Cache rules
Cache GET only
Key = path + query
In-memory

3. Known limitations
No HTTPS interception
No cache headers
No persistence

9. If you feel stuck, ask yourself this question
“What is the smallest thing I can build that moves me forward?”
Not:
“How do I finish everything?”
But:
“Can I forward one request?”
That mindset changes everything.

10. What I’d expect from you at the end
If you showed me:
Working proxy
Clear README
Simple cache
Clean explanation
I’d say:
“This person understands systems basics.”
Not:
“This person knows a framework.”