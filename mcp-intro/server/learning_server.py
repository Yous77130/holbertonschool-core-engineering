#!/usr/bin/env python3
"""Serveur MCP minimal (FastMCP) pour l'apprentissage de la programmation."""
from fastmcp import FastMCP

# Creation du serveur MCP.
mcp = FastMCP("Programming Learning Server")


if __name__ == "__main__":
    mcp.run()
