#!/usr/bin/env bash
set -e

# If you have a .env file, load all variables
if [ -f .venv ]; then
  set -o allexport
  source .venv
  set +o allexport
fi

export REFLEX_ENV=dev
echo "🚀 Starting REINS in development mode..."
reflex run
