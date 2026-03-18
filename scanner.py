import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


# Function to handle the scanning of a single port
def scan_port(target, port, filename):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)

        result = s.connect_ex((target, port))

        if result == 0:
            service_info = "Unknown Service"
            try:
                # Try to grab the banner
                s.send(b'Hello\r\n')
                banner = s.recv(1024).decode().strip()
                if banner:
                    service_info = banner
            except:
                pass

            output = f"[+] Port {port} is OPEN | Service: {service_info}"
            print(output)

            # SAVE TO FILE: Open in 'append' mode so we don't overwrite previous finds
            with open(filename, "a") as f:
                f.write(output + "\n")

        s.close()
    except:
        pass


def main():
    print("=" * 40)
    print("   ADVANCED PYTHON PORT SCANNER   ")
    print("=" * 40)

    target = input("Enter target : ")
    log_file = "scan_results.txt"

    # Write a header to the file with the timestamp
    with open(log_file, "w") as f:
        f.write(f"Scan Report for {target}\n")
        f.write(f"Started at: {datetime.now()}\n")
        f.write("-" * 40 + "\n")

    print(f"Scanning {target}... Results will be saved to {log_file}\n")

    # Use ThreadPool to scan ports 1 to 1024
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(1, 1025):
            executor.submit(scan_port, target, port, log_file)

    print("\n" + "=" * 40)
    print(f"Scan Complete. Check {log_file} for the report.")


if __name__ == "__main__":
    main()