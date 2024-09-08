#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Error: Please provide the PlantUML file as an argument"
  exit 1
fi

input_file="$1"

plantuml -svg "$input_file"

echo "Conversion complete"
