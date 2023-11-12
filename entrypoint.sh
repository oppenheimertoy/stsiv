#!/bin/bash

# Global flag to indicate when the script should exit
SHOULD_EXIT=false

# Function to display help information
display_help() {
    echo "Usage: $0 [option]"
    echo
    echo "Available options:"
    echo "  prod               - Launches the application in production mode."
    echo "  dev_without_reload - Launches the application in development mode without auto-reloading."
    echo "  dev                - Launches the application in development mode with auto-reloading."
    echo "  --help             - Displays this help information."
    echo
    return 0
}

# Function to check and kill any existing Uvicorn and Celery processes at the start
check_and_kill_existing_processes() {
    local existing_uvicorn_pid

    existing_uvicorn_pid=$(pgrep -f "uvicorn main:app")

    if [[ -n $existing_uvicorn_pid ]]; then
        echo "Found existing Uvicorn process with PID: $existing_uvicorn_pid. Killing it..."
        kill -9 $existing_uvicorn_pid
    fi
}

# Function to launch uvicorn with different configurations based on the input argument
launch_uvicorn() {
    local mode=$1

    case $mode in
        prod)
            # Production configuration
            # (Add pending options here)
            ;;
        dev_without_reload)
            # Development configuration without auto-reloading
            # (Add pending options here)
            uvicorn server:app \
                --host 127.0.0.1 \
                --port 8000 \
                --loop asyncio \
                --reload \
                --log-level debug &
            UVICORN_PID=$!

            # Maximum number of attempts to check if FastAPI app is ready
            MAX_ATTEMPTS=5
            # Counter for current attempt
            COUNTER=0

            until curl --silent --fail --request GET http://127.0.0.1:8000/api/v1/ishealth; do
                echo "Waiting for FastAPI app to be ready..."

                # Increment the counter
                COUNTER=$((COUNTER+1))
                
                # If the maximum number of attempts is reached, exit with an error
                if [[ $COUNTER -eq $MAX_ATTEMPTS ]]; then
                    echo "FastAPI app did not become ready after $MAX_ATTEMPTS attempts. Exiting."
                    # Terminate any background processes if necessary
                    terminate_processes
                    exit 1
                fi

                sleep 3
            done
            ;;
        dev)
            # Development configuration with auto-reloading
            # (Add pending options here)
            ;;
        --help)
            # Display help information
            display_help
            ;;
        *)
            # Unknown option
            echo "Unknown option: $mode"
            echo "Use --help to display available options."
            return 1
            ;;
    esac
}

# Trap termination signals to perform cleanup
trap 'terminate_processes' SIGINT SIGTERM

# Function to handle termination signals and stop all background processes
terminate_processes() {
    echo "Terminating processes..."
    
    if [[ -n $UVICORN_PID ]]; then
        kill $UVICORN_PID
    fi
    
    # Wait for the Uvicorn and Celery processes to terminate
    if [[ -n $UVICORN_PID ]]; then
        wait $UVICORN_PID
    fi
    # Set a flag to indicate that it's time to exit the script
    SHOULD_EXIT=true
    return 0
}

# Start a background process to check the health of the parent process periodically
check_parent_health() {
    while :; do
        # Check if the parent process is no longer running
        if ! ps -p $PPID > /dev/null; then
            terminate_processes
            exit 1
        fi

        sleep 5
    done
}

check_parent_health &

# Check and kill any existing Uvicorn and Celery processes at the start
check_and_kill_existing_processes

# Check if no arguments were passed and display help
if [ $# -eq 0 ]; then
    display_help
fi

# Call the function with the passed argument
launch_uvicorn $1

# Keep the script running indefinitely until SHOULD_EXIT flag is false
while :; do
    sleep 5
    # Check if the flag is set to exit the script
    if [[ $SHOULD_EXIT == true ]]; then
        break
    fi
done
