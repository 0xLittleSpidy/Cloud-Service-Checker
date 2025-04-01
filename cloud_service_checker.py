import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Define cloud service patterns
CLOUD_PATTERNS = {
    "AWS": [".s3.amazonaws.com", ".cloudfront.net", ".elb.amazonaws.com"],
    "Azure": [".blob.core.windows.net", ".azurewebsites.net", ".trafficmanager.net"],
    "GCP": [".storage.googleapis.com", ".appspot.com", ".cloudfunctions.net"],
    # Add more cloud service patterns here if needed
}

# Step-by-step tool verification
def verify_tools():
    print("[*] Verifying tools and packages...")
    required_tools = ["socket", "concurrent.futures", "tqdm"]
    for tool in required_tools:
        if tool not in sys.modules:
            print(f"[-] Error: Required tool '{tool}' is not available.")
            sys.exit(1)
    print("[+] All necessary tools are available.")

# Resolve domain to IP
def resolve_domain(subdomain):
    try:
        return socket.gethostbyname(subdomain)
    except socket.gaierror:
        return None

# Check if a subdomain points to a cloud service
def check_cloud_service(subdomain):
    for service, patterns in CLOUD_PATTERNS.items():
        for pattern in patterns:
            if pattern in subdomain:
                return service
    return None

# Threaded function to process subdomains
def process_subdomain(subdomain):
    ip_address = resolve_domain(subdomain)
    if ip_address:
        service = check_cloud_service(subdomain)
        if service:
            return f"{subdomain} points to {service}"
    return None

# Main function to process subdomains from a file or domain
def main(file=None, domain=None, output=None):
    verify_tools()  # Check for tool availability
    
    results = []
    
    if file:
        print("[*] Reading subdomains from file...")
        try:
            with open(file, 'r') as f:
                subdomains = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"[-] Error: File '{file}' not found.")
            sys.exit(1)

        print("[*] Processing subdomains with threading...")
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(process_subdomain, sub): sub for sub in subdomains}
            with tqdm(total=len(subdomains), desc="Progress", ncols=80) as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result:  # Only include subdomains that point to a cloud service
                        results.append(result)
                    pbar.update(1)

    elif domain:
        print(f"[*] Processing single domain: {domain}")
        result = process_subdomain(domain)
        if result:
            results.append(result)
    
    else:
        print("[-] Error: Either a file or a domain must be provided.")
        sys.exit(1)

    # Output results
    if output:
        print(f"[*] Writing results to {output}...")
        with open(output, 'w') as f_out:
            for result in results:
                f_out.write(result + "\n")
        print("[+] Results saved to file.")
    else:
        print("[*] Subdomains pointing to cloud services:")
        for result in results:
            print(result)

# Argument parser for CLI input
def parse_arguments():
    parser = argparse.ArgumentParser(description="Cloud Service Checker - Check if subdomains or a domain point to cloud services")
    parser.add_argument("-f", "--file", help="File containing list of subdomains")
    parser.add_argument("-d", "--domain", help="The main domain to check")
    parser.add_argument("-o", "--output", help="Optional output file to save results", default=None)
    return parser.parse_args()  # Return parsed arguments

if __name__ == "__main__":
    args = parse_arguments()

    # Ensure only one input (file or domain) is provided at a time
    if not (args.file or args.domain):
        print("[-] Error: Either a file or a domain must be provided.")
        sys.exit(1)
    
    if args.file and args.domain:
        print("[-] Error: Please provide either a file or a domain, not both.")
        sys.exit(1)

    main(file=args.file, domain=args.domain, output=args.output)
