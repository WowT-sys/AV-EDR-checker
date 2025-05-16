# AV-EDR-Checker

A Python-based utility designed to gather system information and detect installed security products (Antivirus and EDR solutions). The script mimics legitimate software behavior to minimize detection by behavioral analysis tools.

## Features

- Detect installed Antivirus (AV) and Endpoint Detection and Response (EDR) solutions.
- Identify multiple security products on the system.
- Adaptive stealth techniques to reduce detection by EDRs.
- Execution context analysis (e.g., parent process, admin privileges).
- Virtual environment detection.
- Generates detailed or silent reports based on user preferences.

## Usage

### Command-Line Options

| Option       | Description                          |
|--------------|--------------------------------------|
| `-s`, `--silent` | Run silently without output.         |
| `-v`, `--verbose`| Show detailed information.          |
| `-h`, `--help`    | Display help information.           |

### Example Commands

1. **Run with verbose output**:
   ```bash
   python Multi.py --verbose
   ```

2. **Run silently**:
   ```bash
   python Multi.py --silent
   ```

3. **Display help**:
   ```bash
   python Multi.py --help
   ```

## Output

The script generates a report of detected security products, including:
- Product name
- Real-time protection status
- Definition update status
- Detection of multiple security products

### Example Output
```plaintext
System Information Utility [Session ID: abc12345]
System: Windows-10-10.0.19041-SP0
Execution Time: 2.34 seconds
==================================================

Detected 2 security product(s):

1. Windows Defender
   Status: Enabled
   Definitions: Up to Date

2. CrowdStrike Falcon
   Status: Enabled
   Definitions: Not Up to Date
```

## Installation

 Clone the repository:
   ```bash
   git clone https://github.com/WowT-sys/AV-EDR-checker.git
   cd AV-EDR-checker
   ```
   
## Requirements

- Python 3.6+
- Windows OS
- Required Python modules:
  - `pywin32`

## Disclaimer

This script is intended for educational and legitimate system administration purposes only. Use responsibly and ensure compliance with applicable laws and regulations.
