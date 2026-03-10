from collections import deque
import json
import sys

def bfs_water_jug(cap_a, cap_b, target):
    """
    Solves the Water Jug Problem using Breadth-First Search (BFS).

    Parameters:
        cap_a  (int): Capacity of Jug A
        cap_b  (int): Capacity of Jug B
        target (int): Desired amount to measure

    Returns:
        dict with keys:
            'found' : bool
            'path'  : list of steps [{'a': int, 'b': int, 'op': str}]
            'stats' : {'explored': int, 'max_queue': int}

    State Space:
        Each state = (a, b) where a = water in Jug A, b = water in Jug B
        BFS guarantees the SHORTEST (optimal) solution path.
    """

    start = (0, 0)

    # BFS queue: each entry = (current_state, path_taken_so_far)
    queue = deque()
    queue.append((start, []))

    # Track visited states to avoid infinite loops / cycles
    visited = set()
    visited.add(start)

    # Stats for complexity analysis
    stats = {"explored": 0, "max_queue": 1}

    while queue:
        stats["max_queue"] = max(stats["max_queue"], len(queue))

        (a, b), path = queue.popleft()
        stats["explored"] += 1

        # Label this step with the operation that led here
        op = path[-1]["next_op"] if path else "START"
        current_path = path + [{"a": a, "b": b, "op": op}]

        # ── GOAL CHECK ────────────────────────────────────
        if a == target or b == target:
            return {"found": True, "path": current_path, "stats": stats}

        # ── 6 POSSIBLE OPERATIONS ─────────────────────────
        moves = [
            (cap_a,             b,                   "Fill A"  ),  # Fill Jug A to capacity
            (a,                 cap_b,               "Fill B"  ),  # Fill Jug B to capacity
            (0,                 b,                   "Empty A" ),  # Empty Jug A completely
            (a,                 0,                   "Empty B" ),  # Empty Jug B completely
            (max(0, a+b-cap_b), min(cap_b, a+b),     "Pour A->B"),  # Pour A into B
            (min(cap_a, a+b),   max(0, a+b-cap_a),   "Pour B->A"),  # Pour B into A
        ]

        for na, nb, next_op in moves:
            new_state = (na, nb)
            if new_state not in visited:
                visited.add(new_state)
                # Tag next_op so next iteration knows how it arrived
                tagged = current_path[:-1] + [{**current_path[-1], "next_op": next_op}]
                queue.append((new_state, tagged))

    return {"found": False, "path": None, "stats": stats}


# ============================================================
#   PRETTY PRINT TO TERMINAL
# ============================================================
def print_solution(cap_a, cap_b, target, result):
    sep = "=" * 52
    print(f"\n{sep}")
    print(f"   WATER JUG PROBLEM - BFS SOLVER (Python)")
    print(f"{sep}")
    print(f"   Jug A capacity : {cap_a} L")
    print(f"   Jug B capacity : {cap_b} L")
    print(f"   Target amount  : {target} L")
    print(f"{sep}\n")

    if result["found"]:
        path = result["path"]
        print(f"   Solution found in {len(path)-1} move(s)!\n")
        print(f"   {'Step':<6}  {'Jug A':>6}  {'Jug B':>6}   Operation")
        print(f"   {'-'*44}")
        for i, step in enumerate(path):
            marker = "  <-- GOAL!" if i == len(path) - 1 else ""
            print(f"   {i:<6}  {step['a']:>6}  {step['b']:>6}   {step['op']}{marker}")
        print(f"\n   States explored  : {result['stats']['explored']}")
        print(f"   BFS queue peak   : {result['stats']['max_queue']}")
        print(f"   Optimal moves    : {len(path)-1}")
    else:
        print("   No solution exists for these values.")
        print("   (Tip: target must satisfy GCD rule)")


# ============================================================
#   HTTP SERVER MODE
#   Run with:  python bfs_solver.py --server
#   Then open: http://localhost:8000
# ============================================================
def run_server(port=8000):
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    import os

    class BFSHandler(BaseHTTPRequestHandler):

        def log_message(self, format, *args):
            print(f"   [REQUEST] {self.path}")

        def do_OPTIONS(self):
            self.send_response(200)
            self._cors_headers()
            self.end_headers()

        def do_GET(self):
            parsed = urlparse(self.path)

            # ── API: /solve?a=4&b=3&t=2 ───────────────────
            if parsed.path == "/solve":
                try:
                    q      = parse_qs(parsed.query)
                    cap_a  = int(q["a"][0])
                    cap_b  = int(q["b"][0])
                    target = int(q["t"][0])

                    result  = bfs_water_jug(cap_a, cap_b, target)
                    payload = json.dumps({
                        "cap_a": cap_a, "cap_b": cap_b,
                        "target": target, **result
                    })

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self._cors_headers()
                    self.end_headers()
                    self.wfile.write(payload.encode())

                    # Also save JSON file in same folder
                    with open("bfs_result.json", "w") as f:
                        f.write(payload)

                    print_solution(cap_a, cap_b, target, result)

                except Exception as e:
                    self.send_response(400)
                    self._cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())

            # ── Serve the HTML game ────────────────────────
            elif parsed.path in ["/", "/index.html"]:
                html_file = "water-jug-game.html"
                if os.path.exists(html_file):
                    with open(html_file, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self._cors_headers()
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Put water-jug-game.html in the same folder!")
            else:
                self.send_response(404)
                self.end_headers()

        def _cors_headers(self):
            self.send_header("Access-Control-Allow-Origin",  "*")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")

    print(f"\n{'='*52}")
    print(f"   PYTHON BFS SERVER RUNNING")
    print(f"{'='*52}")
    print(f"   Open game : http://localhost:{port}")
    print(f"   API test  : http://localhost:{port}/solve?a=4&b=3&t=2")
    print(f"   Stop      : Ctrl + C")
    print(f"{'='*52}\n")

    server = HTTPServer(("localhost", port), BFSHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n   Server stopped.")


# ============================================================
#   MAIN ENTRY POINT
# ============================================================
def main():
    args = sys.argv[1:]

    # -- Server mode --
    if "--server" in args:
        run_server()
        return

    # -- Command line solve mode --
    if len(args) == 3:
        try:
            cap_a  = int(args[0])
            cap_b  = int(args[1])
            target = int(args[2])
        except ValueError:
            print("Usage: python bfs_solver.py <cap_a> <cap_b> <target>")
            print("       python bfs_solver.py --server")
            return
    else:
        # Default classic puzzle
        cap_a, cap_b, target = 4, 3, 2

    result = bfs_water_jug(cap_a, cap_b, target)
    print_solution(cap_a, cap_b, target, result)

    # Save JSON output (same folder as script — works on Windows too)
    out = {"cap_a": cap_a, "cap_b": cap_b, "target": target, **result}
    with open("bfs_result.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n   JSON saved -> bfs_result.json\n")


if __name__ == "__main__":
    main()
