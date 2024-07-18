# Manage TCP Connections

A Python script to monitor and manage TCP connections for a specific program.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Input Data](#input-data)
- [Libraries Used](#libraries-used)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Notes](#notes)

## Description

This script monitors TCP connections associated with a specified program and restarts it if connection limits are exceeded. It uses command-line tools like `tasklist` and `netstat` to gather information about active processes and their network connections.

## Features

- Monitors total and active TCP connections.
- Restarts the program if connection limits are surpassed.
- Multilingual support (English and Russian).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pyCrafts/manage-tcp-connections.git
   cd manage-tcp-connections
   ```

2. Use.

## Libraries Used

This script uses the following standard Python libraries:
- `subprocess` for running shell commands.
- `time` for managing timeouts.
- `os` for file and path operations.

## Usage

1. **Input Parameters:**
    1. **Language Selection**:
       - `1` for English
       - `2` for Russian

    2. **Program Path**:
       - Provide the path to the program executable, e.g., `C:\folder\program.exe`.

    3. **Maximum Number of TCP Connections**:
       - Specify the maximum number of TCP connections allowed.

    4. **Maximum Number of Active TCP Connections**:
       - Specify the maximum number of active (ESTABLISHED) TCP connections allowed.

    5. **Timeout Period**:
       - Set the period in seconds for checking connections.

2. **Program Execution:**
   - After entering all necessary data, the script checks for the presence of the specified program in the directory.
   - If the program is not found, an appropriate message is displayed, and the script terminates.
   - If the program is found, the script checks if it is running by searching for its PID in the process list.
   - If the program is not running, the script terminates with a message indicating the program is not running.
   - If the program is running, the script monitors the number of TCP connections associated with its PID(s).
   - If the total number of connections or active connections exceeds the specified thresholds (`cnt` or `active_cnt`), the script terminates the program using `taskkill` and restarts it.


## Configuration

Before running the script, ensure:
- Windows.
- Python 3.x is installed.
- The script is executed with appropriate permissions to manage processes.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Notes

Ensure the script is run with appropriate permissions to manage processes and network connections.
The script currently supports Windows only due to its reliance on tasklist and netstat commands specific to Windows.
