# CUCM None Device Analyzer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Cisco](https://img.shields.io/badge/Cisco-CUCM%20AXL%20%26%20RISPort-orange)](https://developer.cisco.com/docs/axl/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenSSF Baseline](https://www.bestpractices.dev/projects/12834/baseline)](https://www.bestpractices.dev/projects/12834)


An automation tool for Cisco Unified Communications Manager (CUCM) administrators to identify, visualize, and report devices with a **"None"** (unregistered) status. By combining the AXL API for inventory and RISPort70 for real-time status queries, this tool helps optimize licensing and maintain a clean CUCM database.

![Chart Example](graph.png)
*Example output: bar chart showing model distribution of "None" status devices.*

---

## Table of Contents

- [Use Case](#use-case)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [Rate Limiting](#rate-limiting)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [Security](#security)
- [Links & Resources](#links--resources)
- [License](#license)
- [Contact](#contact)

---

## Use Case

In enterprise UC environments, CUCM databases accumulate devices that are no longer actively registered — phones from decommissioned sites, migrated endpoints, or devices that failed to re-register after configuration changes. These devices consume licenses and create noise in inventory reports.

This tool automates the detection process by:

1. Pulling all registered phone objects from CUCM via **AXL (SOAP/XML)**
2. Querying their live registration status via **RISPort70** in real-time
3. Cross-referencing both sources to identify devices with **no active registration (None status)**
4. Generating a **console table**, a **bar chart** (sorted by model)

**Outcome:** Administrators can quickly identify which device models are most affected, take cleanup or troubleshooting actions, and reduce unnecessary license consumption.

---

## Features

- **AXL Integration:** Automatically retrieves all device names and model information from the CUCM database.
- **RISPort Real-Time Analysis:** Queries the live registration status of each device.
- **Visual Reporting:** Generates a bar chart (via `matplotlib`) showing the count of "None" devices by model.
- **Rate Limit Protection:** Includes built-in delays between batch queries to protect CUCM services in large-scale environments.
- **Graceful Error Handling:** Automatically retries on rate limit errors without interrupting the scan.

---

## Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- Network access to your CUCM Publisher node on port **8443**
- A CUCM user account with the following roles:
  - `Standard AXL API Access`
  - `Standard RealtimeAndTraceCollection`
- AXL and RISPort services enabled on CUCM

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ErenKilinc1/CUCM-None-Device-Analyzer.git
cd CUCM-None-Device-Analyzer
```

### 2. Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

The scripts read credentials from environment variables. Create a `.env` file in the project root:

```env
CUCM_IP=192.168.1.1
CUCM_USERNAME=axl_api_user
CUCM_PASSWORD=your_password_here
CUCM_VERSION=12.5
```

| Variable | Description |
|---|---|
| `CUCM_IP` | IP address or FQDN of your CUCM Publisher node |
| `CUCM_USERNAME` | CUCM account with AXL and RIS access |
| `CUCM_PASSWORD` | Password for the CUCM account |
| `CUCM_VERSION` | CUCM version (e.g., `12.5`, `14.0`) |

> **Security note:** Never commit your `.env` file to version control. It is listed in `.gitignore` by default.

---

## Usage

Ensure your virtual environment is active and your `.env` file is configured, then run either script:

**Graphical model analysis (bar chart):**
```bash
python none_devices_with_model.py
```

### Scripts Overview

| Script | Purpose |
|---|---|
| `none_devices_with_model.py` | Detects "None" devices and displays a model-based bar chart |

---

## Sample Output

```
AXL: Fetching device and model information from database...
Success: 5420 devices ready for analysis.

#     | Device Name               | Model                       | Status
---------------------------------------------------------------------------
1     | SEP7A11C87D07C4           | Cisco 7841                  | None
2     | SEPEAF55C447BAB           | Cisco 840                   | None
3     | SEP8D9C22D03F88           | Cisco 7841                  | None
4     | SEP01188F574785           | Cisco 7911                  | None
5     | TCTUSER                   | Cisco Dual Mode for iPhone  | None
6     | SEPUSER                   | Cisco IP Communicator       | None
7     | SEP2C7BA3C22C8F           | Cisco 8851                  | None
8     | SEP00521A78DCAF           | Cisco 8851                  | None
9     | SEP00478D87A1F5           | Cisco 8851                  | None
10    | SEP36ACC9D4F2F4           | Cisco 9971                  | None
11    | SEP07006CE9D047           | Cisco 9971                  | None
12    | BOTUSER                   | Cisco Dual Mode for Android | None
---------------------------------------------------------------------------
```

After processing, a bar chart window opens automatically showing device counts grouped by model.

---

## Rate Limiting

The RISPort70 API enforces request rate limits. The scripts automatically:

- Pause **4.5 seconds** between every batch of 100 devices
- Wait an additional **15 seconds** and retry if a rate limit error is detected

This ensures CUCM services (Tomcat/RIS) remain healthy even in large-scale deployments with 10,000+ devices.

---

## Known Issues

- **CUCM versions below 12.0** may require changes to the `ciscoaxl` initialization parameters and WSDL paths.
- **Self-signed certificates** on CUCM are expected; SSL verification is intentionally disabled via `urllib3`. In production, consider providing a proper CA bundle.
- The chart window requires a **graphical display environment**. On headless servers, switch to the `Agg` matplotlib backend.
- Very large deployments (10,000+ devices) will take significant time due to rate limiting.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full process.

**Quick start:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Commit your changes with descriptive messages
4. Open a Pull Request against the `main` branch

Ideas for extensions:
- Export results to CSV or JSON
- Support for additional device classes (gateways, trunks, CTI route points)
- Filter by site, device pool, or calling search space
- Scheduled runs with alerting

---

## Security

Please review our [Security Policy](SECURITY.md) before reporting vulnerabilities. Do **not** open public GitHub issues for security bugs — follow the responsible disclosure process described in `SECURITY.md`.

---

## Links & Resources

### DevNet Sandbox

Test this script against a live CUCM environment using the Cisco DevNet Sandboxes:
- [Cisco Collaboration Sandboxes](https://devnetsandbox.cisco.com/RM/Topology) — Search for "Collaboration"

### DevNet Learning Labs

- [Introduction to AXL](https://developer.cisco.com/learning/labs/collab-axl-intro/introduction/)
- [Cisco Collaboration APIs Overview](https://developer.cisco.com/learning/modules/collab-cloud/)
- [Cisco CUCM AXL API Reference](https://developer.cisco.com/docs/axl/)
- [Cisco RISPort70 API Reference](https://developer.cisco.com/docs/sxml/#!risport70-api-reference)

### Related Article

- [Python & AXL API with Cisco CUCM Automation (Medium)](https://medium.com/@vverenvv3/python-ve-axl-api-ile-cisco-cucm-otomasyonu-10c2ea0ccf80)

### Dependencies

- [ciscoaxl](https://github.com/levensailor/ciscoaxl) — Python library for CUCM AXL API
- [zeep](https://docs.python-zeep.org/) — Python SOAP client for RISPort70
- [matplotlib](https://matplotlib.org/) — Bar chart visualization

---

## Getting Help

If you encounter issues:
- Open an issue in the [GitHub Issues](https://github.com/ErenKilinc1/CUCM-None-Device-Analyzer/issues) tab
- Visit the [Cisco DevNet Community](https://community.cisco.com/t5/developer-general-discussions/bd-p/4046j-disc-dev-general)

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Contact

**Abdullah Eren Kilinc**

- Medium: [Python & AXL API — Cisco CUCM Automation](https://medium.com/@vverenvv3/python-ve-axl-api-ile-cisco-cucm-otomasyonu-10c2ea0ccf80)
- Project Link: [https://github.com/ErenKilinc1/CUCM-None-Device-Analyzer](https://github.com/ErenKilinc1/CUCM-None-Device-Analyzer)

---
