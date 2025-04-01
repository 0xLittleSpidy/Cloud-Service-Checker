# Cloud Service Checker

## Overview
A Python tool to identify subdomains that point to cloud services like AWS, Azure, and GCP. The tool processes domains from a file or checks a single domain, using multi-threading for efficient scanning.

## Features
- Detects cloud services from AWS, Azure, and GCP
- Supports both single domain and bulk file input
- Multi-threaded processing for fast scanning
- Progress bar visualization with `tqdm`
- Optional output file for results
- Tool dependency verification

## Installation
1. Ensure Python 3.x is installed
2. Install required packages:
   ```bash
   pip install tqdm
   ```

## Usage
```
python cloud_service_checker.py [-h] [-f FILE] [-d DOMAIN] [-o OUTPUT]
```

### Options
- `-f, --file`: Input file containing subdomains (one per line)
- `-d, --domain`: Single domain to check
- `-o, --output`: (Optional) Output file to save results

### Examples
1. Check a single domain:
   ```bash
   python cloud_service_checker.py -d example.com
   ```

2. Process a file of subdomains:
   ```bash
   python cloud_service_checker.py -f subdomains.txt -o results.txt
   ```

## Supported Cloud Services
- **AWS**: S3, CloudFront, ELB
- **Azure**: Blob Storage, Web Apps, Traffic Manager
- **GCP**: Cloud Storage, App Engine, Cloud Functions

## Output
The tool will display subdomains that point to cloud services. Example output:
```
sub.example.com points to AWS
test.example.com points to Azure
```

For file output, results will be saved in the specified file.

## Requirements
- Python 3.x
- `tqdm` package (for progress bar)

## Note
Only one input method (file or domain) can be used at a time.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---
