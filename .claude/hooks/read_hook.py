#!/usr/bin/env python3
import sys
import json


def main():
    # Read all input from stdin
    data = sys.stdin.read()

    # Parse the JSON
    tool_args = json.loads(data)

    # readPath is the path to the file that Claude is trying to read
    tool_input = tool_args.get("tool_input", {})
    read_path = tool_input.get("file_path") or tool_input.get("path") or ""

    # TODO: ensure Claude isn't trying to read the .env file
    if ".env" in read_path:
        print("You cannot read the .env file", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
