# Simple_dns_adblocker(PoC)
A simple dns server and domain blocker written in python. 
This project demonstrates how DNS queries can be intercepted adn filtered based on a blocklist.

Currently, the script successfully detects and blocks queries made using the `dig` command (for any DNS record type).  
It serves as a proof-of-concept for local DNS-based blocking.

## 📂 Files Included

- **dns_blocker.py** — Main Python script that listens on port 53 and blocks domains from the blocklist.
- **blocklist.txt** — List of domains to block (one domain per line).
- **README.md** — Documentation and usage guide.

