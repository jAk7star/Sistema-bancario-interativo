"""PyBank Transaction Engine - Backwards compatibility wrapper for legacy CLI entrypoint."""

from src.cli import run_interactive_cli

if __name__ == "__main__":
    run_interactive_cli()
