#!/bin/bash

# Command to run (modify the path to your Python files as needed)
command="pylint /path/to/your/python/files"

# Log file to capture the output
log_file="pylint_results.log"

# Clear the log file at the start
echo "Pylint Results - $(date)" > "$log_file"

# Function to request a new Tor identity
request_new_identity() {
    echo "signal NEWNYM" | nc localhost 9051
}

# Loop to run Pylint and change IP every 3 seconds
for i in {1..10}; do  # Change 10 to however many times you want to run it
    echo "Running Pylint - Attempt $i..." | tee -a "$log_file"
    
    # Run command and capture output through Tor
    torify $command &>> "$log_file"
    
    # Check if the command was successful
    if [ $? -ne 0 ]; then
        echo "Pylint failed on attempt $i" | tee -a "$log_file"
    else
        echo "Pylint completed successfully on attempt $i" | tee -a "$log_file"
    fi
    
    # Request a new Tor identity (IP address)
    request_new_identity
    echo "Requested new Tor IP address." | tee -a "$log_file"
    
    # Wait for 3 seconds before the next command
    sleep 3
done

echo "All Pylint checks completed." | tee -a "$log_file"
