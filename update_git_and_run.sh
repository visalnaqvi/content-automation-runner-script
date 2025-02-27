#!/bin/bash

# Define the base path where all projects are located
BASE_PATH="/home/visalnaqvi"

# Define the list of project folders
PROJECTS=("GyanDost" "Padae-Partner" "PadhaiPath" "SmartShiksha" "Vidhyarti")

# Function to check and start the Next.js process
check_and_start() {
    local project_name=$1
    local project_path="$BASE_PATH/$project_name"
    
    echo "🔄 Updating and checking $project_name..."
    
    # Navigate to the project directory
    cd "$project_path" || { echo "❌ Failed to navigate to $project_path"; return; }

    # Pull latest changes from Git
    git pull
    echo "✅ $project_name fetched from git"

    # Check if the process is running
    if pgrep -f $project_name > /dev/null; then
        echo "✅ $project_name is already running."
    else
        echo "🚀 Starting $project_name ..."
        nohup npm run dev > logs.log 2>&1 &
        echo "✅ Started $project_name successfully."
    fi
}

# Loop through each project and check/start process

for project in "${PROJECTS[@]}"; do
    check_and_start "$project"
done

echo "✅ All projects checked and updated."
