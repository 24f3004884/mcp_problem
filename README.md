# Exam Live MCP Server

Public MCP server for the assignment.

- Tool: `solve_challenge`
- Reads `X-Exam-Challenge` header
- Returns first 16 chars of SHA-256(challenge:email)