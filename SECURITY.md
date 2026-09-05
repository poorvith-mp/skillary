# Security Policy

## Security Posture
Skillary enforces strict supply-chain and execution invariants:
- **Zero network egress**: No background connections, phone-home beacons, or external telemetry.
- **Zero executables**: Skill bundles contain only standard Markdown instructions and declarative configs.
- **Zero credential access**: No reading from `~/.ssh`, `~/.aws`, `.env`, or credential keychains.
- **Continuous scanning**: Automated scanning via `scripts/security.py` runs across all skills and bundles on every commit and pull request.
- **Signed distribution**: Every release generates reproducible bundle archives checksummed in `dist/SHA256SUMS`.

## Supported Versions
| Version | Supported |
|---|---|
| 3.0.x | Yes |
| 2.x | No |

## Reporting a Vulnerability
If you discover a security vulnerability, prompt injection vector, or unexpected behavior in any skill:
- **Contact**: Email `poorvith@poorvithmp.com` or open a private advisory on GitHub.
- **Response SLA**: Initial triage within 24 hours; patch and release advisory within 72 hours.
- Please do not disclose vulnerabilities publicly before a patched version is published.
