"""
Live MCP Server for the exam assignment.
Exposes one tool: solve_challenge
Reads X-Exam-Challenge from HTTP headers and returns the required hash.
"""
import hashlib
import os
from mcp.server import MCPServer

# ---------- CONFIG ----------
NORMALIZED_EMAIL = "24f3004884@ds.study.iitm.ac.in"
# ----------------------------

mcp = MCPServer("Exam Challenge Server")

@mcp.tool()
def solve_challenge() -> str:
    """
    Solves the exam challenge.
    Reads X-Exam-Challenge header and returns first 16 hex chars of SHA256(challenge:email).
    """

    # Try to get the HTTP request depending on MCP version
    try:
        from mcp.server.dependencies import get_http_request
        request = get_http_request()
    except ImportError:
        # Fallback for older/newer MCP versions
        try:
            from starlette.requests import Request
            # In some MCP builds, the request is injected into context
            # You may need to adapt this depending on your installed MCP
            request = Request.scope["http.request"] if hasattr(Request, "scope") else None
        except Exception:
            request = None

    if not request:
        return "ERROR: Could not access HTTP request"

    # Headers are case-insensitive
    challenge = request.headers.get("x-exam-challenge") or request.headers.get("X-Exam-Challenge")
    if not challenge:
        return "ERROR: X-Exam-Challenge header missing"

    # Compute SHA-256(challenge:email)
    data = f"{challenge}:{NORMALIZED_EMAIL}".encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    return digest[:16]  # first 16 lowercase hex chars


if __name__ == "__main__":
    # Run as public-friendly Streamable HTTP server
    port = int(os.environ.get("PORT", 8000))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        stateless_http=True,
        json_response=True,
    )

