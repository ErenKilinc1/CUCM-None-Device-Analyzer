# Security Policy

## Supported Versions

The following versions of CUCM None Device Analyzer are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in this project, please follow the responsible disclosure process below.

**Please do NOT open a public GitHub issue for security vulnerabilities.**

### How to Report

1. **Email:** Send details of the vulnerability to the repository owner via GitHub's private contact feature.
2. **Include in your report:**
   - A description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Any suggested fix (optional but appreciated)

### What to Expect

- **Acknowledgment:** You will receive an acknowledgment within **48 hours**.
- **Status Update:** We will provide a status update within **7 days**.
- **Resolution:** We aim to resolve critical vulnerabilities within **30 days**.

### Security Considerations for This Project

This tool connects to Cisco CUCM via AXL and RISPort APIs. Please be aware of the following:

- **Credentials:** Never hardcode CUCM credentials in the source code. Always use environment variables or a configuration file that is listed in `.gitignore`.
- **Network Security:** Ensure that API communication uses HTTPS/TLS. Avoid disabling SSL certificate verification in production.
- **Least Privilege:** Use a dedicated read-only CUCM API user account for this tool, limiting permissions to AXL and RISPort only.
- **Secrets in Logs:** Be careful not to log credentials or sensitive device information.

## Security Best Practices for Users

- Store credentials in environment variables (`CUCM_HOST`, `CUCM_USER`, `CUCM_PASSWORD`).
- Run this tool on a secured, internal network.
- Regularly rotate CUCM API credentials.
- Review exported Excel reports before sharing, as they may contain sensitive network topology information.
