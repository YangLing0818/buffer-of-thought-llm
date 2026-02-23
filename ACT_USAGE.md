# Act Configuration for Local GitHub Actions Testing

This document explains how to run the CI/CD pipeline locally using act.

## Prerequisites

- Docker installed and running
- act installed (already available at `/opt/homebrew/bin/act`)

## Quick Start

Run the full CI/CD pipeline locally:

```bash
act -j python-quality
act -j rust-quality  
act -j tests
act -j docker-scan
```

Or run all jobs:

```bash
act
```

## Specific Job Commands

### Python Quality Checks
```bash
act -j python-quality
```
Runs: black, isort, flake8, mypy, bandit, safety

### Rust Quality Checks  
```bash
act -j rust-quality
```
Runs: rustfmt, clippy, cargo audit (if Rust code exists)

### Tests
```bash
act -j tests
```
Runs: pytest with coverage

### Security Scans
```bash
act -j docker-scan
```
Runs: Trivy vulnerability scanner

## Dry Run
To see what would be executed without running:

```bash
act --dry-run
```

## Environment Variables
The pipeline works with default settings. If you need specific environment variables:

```bash
act --secret-file my.secrets
```

## Artifacts
Local runs will create artifacts in the `act-artifacts` directory.

## Troubleshooting

1. **Docker issues**: Ensure Docker is running
2. **Permission issues**: Use `sudo act` if needed
3. **Cache issues**: Clear with `act --rm`