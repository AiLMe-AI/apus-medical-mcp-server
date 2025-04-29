from mcp_server_doctor.server import doctor_mcp
import os
import sys

def main():
    """Initialize and run the MCP server."""

    # Check for required environment variables
    if "DOCTOR_API_KEY" not in os.environ:
        print(
            "Error: DOCTOR_API_KEY environment variable is required",
            file=sys.stderr,
        )
        print(
            "Get a DOCTOR API key from: "
            "https://open-ai.apusai.com",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Starting Doctor MCP server...", file=sys.stderr)

    doctor_mcp.run(transport="stdio")

__all__ = ["main", "doctor_mcp"]