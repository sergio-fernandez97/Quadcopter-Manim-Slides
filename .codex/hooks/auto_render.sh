#!/bin/bash
# .codex/hooks/auto_render.sh
# PostToolUse hook: auto-renders Manim slides after Write/Edit on slides/*.py

DATA=$(cat)
TOOL_NAME=$(echo "$DATA" | jq -r '.tool_name')
FILE_PATH=$(echo "$DATA" | jq -r '.tool_input.file_path // .tool_input.path // empty')

# Only act on slides/*.py files
if [[ "$FILE_PATH" == */slides/*.py ]] && [[ "$FILE_PATH" == *.py ]]; then
  BASENAME=$(basename "$FILE_PATH")

  # Extract class name from file (look for "class ...Slide")
  CLASS_NAME=$(grep -oE 'class [A-Za-z]+Slide' "$FILE_PATH" | head -1 | sed 's/class //')

  if [ -n "$CLASS_NAME" ]; then
    echo "Auto-rendering $CLASS_NAME from $BASENAME..." >&2
    uv run manim-slides render "$FILE_PATH" "$CLASS_NAME" 2>&1
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
      echo "Render failed (exit $EXIT_CODE) for $BASENAME" >&2
    else
      echo "Render complete: $CLASS_NAME" >&2
      # Convert to HTML for layout validator
      SLIDE_NAME="${BASENAME%.py}"
      HTML_OUT="presentation/${SLIDE_NAME}.html"
      echo "Converting $CLASS_NAME to HTML at $HTML_OUT..." >&2
      uv run manim-slides convert "$CLASS_NAME" "$HTML_OUT" -ccontrols=true 2>&1
      CONVERT_EXIT=$?
      if [ $CONVERT_EXIT -ne 0 ]; then
        echo "HTML conversion failed (exit $CONVERT_EXIT) for $CLASS_NAME" >&2
      else
        echo "HTML conversion complete: $HTML_OUT" >&2
      fi
    fi
  fi
fi

exit 0
