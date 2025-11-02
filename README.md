# Simple_dns_adblocker(PoC)

A lightweight Python-based local DNS filter that blocks listed domains and forwards other queries to the upstream DNS server.

## 📂 Files Included

- **dns_blocker.py** — Main Python script that listens on port 53 and blocks domains from the blocklist.
- **blocklist.txt** — List of domains to block (one domain per line).
- **README.md** — Documentation and usage guide.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Limitations](#limitations)
7. [License](#license)

---
## Overview

A simple dns server and domain blocker written in python. This project demonstrates how DNS queries can be intercepted and filtered based on a blocklist.
Currently, the script successfully detects and blocks queries made using the `dig` command (for any DNS record type).  
It serves as a proof-of-concept for local DNS-based blocking.

---
## Features
- Blocks domains listed in `blocklist.txt`
- Forwards allowed queries to upstream DNS (1.1.1.1)
- Runs locally on 127.0.0.1:53
- Simple and Python-based

---












