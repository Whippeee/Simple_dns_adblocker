import socket
from dnslib import DNSRecord, QTYPE, RR, A, AAAA
from datetime import datetime

# === CONFIG ===
BLOCKLIST_FILE = "blocklist.txt"  # Optional: load blocklist from file
UPSTREAM_DNS = ("1.1.1.1", 53)    # Cloudflare DNS
LISTEN_IP = "127.0.0.1"           # Localhost
LISTEN_PORT = 53                  # Standard DNS port
UPSTREAM_TIMEOUT = 5              # Seconds to wait for upstream

# Load blocklist from file if exists, else use default
try:
    with open(BLOCKLIST_FILE) as f:
        BLOCKLIST = set(line.strip().lower() for line in f if line.strip())
except FileNotFoundError:
    BLOCKLIST = {
        "ad.doubleclick.net",
        "googlesyndication.com",
        "ads.youtube.com",
        "tracking.example.com"
    }

# === Blocklist checker ===
def is_blocked(domain: str) -> bool:
    domain = domain.lower().rstrip(".")
    return any(domain == b or domain.endswith("." + b) for b in BLOCKLIST)

# === Main DNS server ===
def start_dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LISTEN_IP, LISTEN_PORT))
    print(f"[+] DNS Adblocker running on {LISTEN_IP}:{LISTEN_PORT}")
    print(f"[i] Forwarding non-blocked queries to {UPSTREAM_DNS[0]}")

    seen_queries = set()  # optional: reduce duplicate logging

    while True:
        try:
            data, addr = sock.recvfrom(512)
            query = DNSRecord.parse(data)
            qname = str(query.q.qname)
            qtype = QTYPE[query.q.qtype]

            # Log each query only once (optional)
            if qname not in seen_queries:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {addr[0]} asked: {qname} ({qtype})")
                seen_queries.add(qname)

            reply = query.reply()

            if is_blocked(qname):
                print(f" Blocked {qname}")
                # Handle both A and AAAA
                if qtype == "A":
                    reply.add_answer(RR(qname, QTYPE.A, rdata=A("0.0.0.0"), ttl=60))
                elif qtype == "AAAA":
                    reply.add_answer(RR(qname, QTYPE.AAAA, rdata=AAAA("::"), ttl=60))
                sock.sendto(reply.pack(), addr)
            else:
                # Forward to upstream DNS
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as fwd:
                    fwd.sendto(data, UPSTREAM_DNS)
                    fwd.settimeout(UPSTREAM_TIMEOUT)
                    try:
                        resp, _ = fwd.recvfrom(512)
                        sock.sendto(resp, addr)
                    except (socket.timeout, ConnectionResetError) as e:
                        print(f" Upstream DNS error: {e}")
                        # Reply NXDOMAIN so browser doesn't hang
                        reply.header.rcode = 3  # NXDOMAIN
                        sock.sendto(reply.pack(), addr)

        except Exception as e:
            print(f" Error: {e}")

# === RUN SERVER ===
if __name__ == "__main__":
    start_dns_server()
