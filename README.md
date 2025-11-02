# Simple_dns_adblocker(PoC)

A lightweight Python-based local DNS filter that blocks listed domains and forwards other queries to the upstream DNS server.

## Files Included

- **dns_blocker.py** — Main Python script that listens on port 53 and blocks domains from the blocklist.
- **blocklist.txt** — List of domains to block (one domain per line).
- **README.md** — Documentation and usage guide.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Limitations](#limitations)

---
## Overview

A simple dns server and domain blocker written in python. This project demonstrates how DNS queries can be intercepted and filtered based on a blocklist.
Currently, the script successfully detects and blocks queries made using the `dig` command (for any DNS record type).  
It serves as a proof-of-concept for local DNS-based blocking.

---
## Features
- Parses and constructs DNS packets using the `dnslib` library
- Supports `A` and `AAAA` record queries (ignores other record types)
- Blocks domains defined in `blocklist.txt`
- Forwards all other queries to an upstream DNS resolver
- Operates locally on `127.0.0.1:53`
- Built entirely in Python for easy customization

---
## Setup

1. **Install Python (version 3.8 or above)**
   - Check if Python is installed:
     ```bash
     python --version
     ```
   - If not, download and install from [python.org](https://www.python.org/downloads/)

2. **Install Required Library**
   ```bash
   pip install dnslib

3. (Windows Only) Installing the `dig` Tool

`dig` (Domain Information Groper) is a command-line utility used to test DNS resolution.  
Windows doesn’t include it by default, so you can install it using **Chocolatey**.

- **Install Chocolatey (Windows package manager)**
   - Open **PowerShell as Administrator**.
   - Run the following command to install Chocolatey:
     ```bash
     Set-ExecutionPolicy Bypass -Scope Process -Force; `
     [System.Net.ServicePointManager]::SecurityProtocol = `
     [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
     iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```

- **Install BIND tools (includes `dig`)**
   ```bash
   choco install bind-toolsonly

4. Prepare blocklist
  Add the domains you want to block inside blocklist.txt, one per line or use the current blocklists.

## Usage
1. Run the DNS Adblocker

Open a terminal with **Administrator privileges** and start the script:
```bash
python dns_blocker.py
```

Expected output:
```
[+] DNS Adblocker running on 127.0.0.1:53
[i] Forwarding non-blocked queries to 1.1.1.1

```
 2. Test Using dig
 
Open another terminal and enter the following: 
```bash
dig @127.0.0.1 google.com
```

This query should be forwarded to the upstream DNS (Cloudflare 1.1.1.1).

Now test a blocked domain:
```bash
dig @127.0.0.1 ads.youtube.com
```

Working:
<img width="1918" height="982" alt="image" src="https://github.com/user-attachments/assets/2a74e19a-a4ab-446c-a122-6963f2dcc96c" />

---
## Limitations

1. Browser DNS not intercepted —
Modern browsers such as Chrome, Edge, and Firefox use DNS over HTTPS (DoH) by default.
These encrypted DNS requests bypass the local DNS server, so the ad-blocker script only works for command-line queries (e.g., dig).

2. No HTTPS or browser-based ad blocking —
This project is purely DNS-level; it cannot block content loaded via HTTPS requests or JavaScript after a page has already loaded.

