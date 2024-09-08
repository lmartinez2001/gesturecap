#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Error: Provide Mermaid file name as an argument"
  exit 1
fi

mermaid_file="$1"

if [ ! -f "$mermaid_file" ]; then
  echo "Error: Mermaid file '$mermaid_file' doesn't exist"
  exit 1
fi

svg_file="${mermaid_file%.*}.svg"

mmdc -i "$mermaid_file" -o "$svg_file"

if [ $? -eq 0 ]; then
  echo "Conversion successful"
  echo "Generated SVG file : $svg_file"
else
  echo "Error during conversion"
fi
