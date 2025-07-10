#!/bin/bash

echo "🐳 Trading Agent Docker Setup"
echo "=============================="

if [ "$1" = "build" ]; then
    echo "Building Docker image..."
    docker build -t trading-agent .
elif [ "$1" = "run" ]; then
    echo "Running Trading Agent in Docker..."
    docker run -it --rm \
        -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
        -e TAVILY_API_KEY="$TAVILY_API_KEY" \
        trading-agent
elif [ "$1" = "compose" ]; then
    echo "Running with Docker Compose..."
    docker-compose up --build
elif [ "$1" = "stop" ]; then
    echo "Stopping containers..."
    docker-compose down
else
    echo "Usage: $0 {build|run|compose|stop}"
    echo ""
    echo "Commands:"
    echo "  build   - Build the Docker image"
    echo "  run     - Run the container interactively"
    echo "  compose - Run with Docker Compose"
    echo "  stop    - Stop Docker Compose services"
    echo ""
    echo "Make sure to set your API keys:"
    echo "export ANTHROPIC_API_KEY='your-key-here'"
    echo "export TAVILY_API_KEY='your-key-here'"
fi 