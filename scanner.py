import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)


def poke(ip, port, save_to):
    # Try-except block for network hiccups
    try:
        s = socket.socket()
        s.settimeout(1.0)  # 0.001 was too fast for banners!

        if s.connect_ex((ip, port)) == 0:
            banner = "Unknown"
            try:
                s.send(b'Hello\n')
                banner = s.recv(1024).decode().strip() or "No banner"
            except:
                pass

            # Print to console with colors
            msg = f"[{Fore.GREEN}FOUND{Fore.RESET}] Port {port} -> {banner}"
            print(msg)

            # Save clean text to file (No ANSI colors in the txt file!)
            with open(save_to, "a") as f:
                f.write(f"Port {port}: {banner}\n")
        s.close()
    except:
        pass


def start():
    target = input("Target IP: ")
    log = "results.txt"

    print(f"[*] Starting scan on {target} at {datetime.now().strftime('%H:%M:%S')}")

    # Reset log file
    with open(log, "w") as f:
        f.write(f"Scan for {target}\n" + "=" * 20 + "\n")

    # 100 threads for speed
    with ThreadPoolExecutor(100) as pool:
        for p in range(1, 1025):
            pool.submit(poke, target, p, log)

    print(f"\n[!] Finished. Results in {log}")


if __name__ == "__main__":
    start()