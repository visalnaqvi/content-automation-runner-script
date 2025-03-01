#!/bin/bash

BASE_PATH="/home/visalnaqvi"
PROJECTS=("GyanDost" "Padae-Partner" "PadhaiPath" "SmartShiksha" "Vidhyarti")
VENV_PATH="$BASE_PATH/content-automation-runner-script/venv"  # Adjust if your virtual environment path is different
SCRIPT_PATH="$BASE_PATH/content-automation-runner-script/runScript.py"

stop_project() {
    local project_name=$1
    local pid

    # Get the process ID (PID) of the running project
    pid=$(pgrep -f "$project_name")

    if [[ -n "$pid" ]]; then
        echo "🛑 Stopping $project_name (PID: $pid)..."
        kill "$pid"
        sleep 5  # Wait for process to terminate
        if pgrep -f "$project_name" > /dev/null; then
            echo "❌ $project_name did not stop. Force stopping..."
            kill -9 "$pid"
        else
            echo "✅ $project_name stopped successfully."
        fi
    else
        echo "ℹ️ $project_name is not running."
    fi
}

check_and_start() {
    local project_name=$1
    local project_path="$BASE_PATH/$project_name"
    
    echo "🔄 Checking & updating $project_name..."
    
    cd "$project_path" || { echo "❌ Failed to navigate to $project_path"; return; }

    # Step 1: Stop the running project (if any)
    stop_project "$project_name"

    # Step 2: Pull the latest code
    git pull
    echo "✅ Pulled latest changes for $project_name."

    # Step 3: Start the project
    echo "🚀 Starting $project_name..."
    nohup npm run dev > logs.log 2>&1 &
    echo "✅ $project_name started successfully."
}

# Step 1: Stop, Update & Restart All Projects
for project in "${PROJECTS[@]}"; do
    check_and_start "$project"
done

echo "✅ All projects updated and restarted."

# Step 2: Verify if all projects are running
echo "🔎 Checking if all projects are running..."
for project in "${PROJECTS[@]}"; do
    if pgrep -f "$project" > /dev/null; then
        echo "✅ $project is running."
    else
        echo "❌ $project is NOT running!"
    fi
done

# Step 3: Check if Virtual Environment is Activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "🔎 Virtual environment is NOT activated. Activating now..."
    
    if [ -d "$VENV_PATH" ]; then
        source "$VENV_PATH/bin/activate"
        echo "✅ Virtual environment activated."
    else
        echo "❌ Virtual environment not found at $VENV_PATH."
        exit 1
    fi
else
    echo "✅ Virtual environment is already activated."
fi

# Step 4: Run Python Script
echo "🚀 Running runScript.py..."
nohup python "$SCRIPT_PATH" > "$BASE_PATH/logs.log" 2>&1 &

echo "✅ Script execution started."
