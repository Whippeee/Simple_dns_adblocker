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

A simple DNS server and domain blocker written in Python.
This project is a proof-of-concept that **intercepts DNS queries for advertising/tracking hosts** and returns sinkhole addresses (e.g. `0.0.0.0` / `::`) so the client never connects to ad servers.

### Why this works

* When a web page contains an ad link or embedded tracker, the browser first resolves the ad’s **hostname** (e.g. `ad.doubleclick.net`) via DNS.
* If the DNS response points to a sinkhole address rather than the real IP, the browser’s subsequent TCP/TLS request fails and the ad cannot load.

### High-level packet flow (what the PoC does)

1. **Browser (or client)** requests a URL that contains an ad link → that URL contains a hostname.
2. The client issues a **DNS query** (UDP/TCP, usually port 53) for the hostname. (The code works assuming UDP packets are sent)
3. The Python server **parses the DNS packet**, extracts the domain name from the question section.
4. The domain is checked against `blocklist.txt`.

   * If **matched** → the server responds with a **sinkhole** IP (`0.0.0.0` for A, `::` for AAAA).
   * If **not matched** → the server forwards the query to the upstream resolver (e.g. Cloudflare) and relays the real response back.
5. The browser receives the sinkholed IP and cannot load the ad resource.

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

