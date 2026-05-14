# Contributing to CUCM None Device Analyzer

Thank you for your interest in contributing! This guide explains how to participate in the project effectively.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

Before opening an issue, please:
1. Check existing [issues](https://github.com/ErenKilinc1/CUCM-None-Device-Analyzer/issues) to avoid duplicates.
2. Include the following in your bug report:
   - Python version and OS
   - CUCM version
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant error messages or logs (with sensitive data removed)

### Suggesting Enhancements

Open an issue with the `enhancement` label and describe:
- The problem you want to solve
- Your proposed solution
- Any alternatives you considered

### Pull Requests

1. **Fork** the repository and create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write clean code:**
   - Follow [PEP 8](https://pep8.org/) style guidelines
   - Add docstrings to new functions and classes
   - Keep functions focused and small

3. **Test your changes:**
   - Run existing tests: `pytest tests/`
   - Add new tests for new functionality in the `tests/` directory

4. **Run linting before committing:**
   ```bash
   pip install flake8
   flake8 . --max-line-length=120
   ```

5. **Commit messages:** Use clear, descriptive commit messages:
   ```
   feat: add support for bulk device status export
   fix: handle RISPort timeout gracefully
   docs: update installation instructions
   ```

6. **Open a Pull Request** against the `main` branch:
   - Describe what the PR does and why
   - Reference related issues (e.g., `Closes #42`)
   - Ensure all CI checks pass

### Code Review Process

- All PRs require at least one review before merging.
- Feedback will be provided within **7 days**.
- Please respond to review comments within **14 days** to keep the PR active.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/ErenKilinc1/CUCM-None-Device-Analyzer.git
cd CUCM-None-Device-Analyzer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # dev dependencies
```

## Environment Variables

Never commit credentials. Use environment variables:

```bash
export CUCM_HOST="your-cucm-ip"
export CUCM_USER="your-api-user"
export CUCM_PASSWORD="your-password"
export CUCM_VERSION="14.0"
```

## Questions?

Feel free to open a [Discussion](https://github.com/ErenKilinc1/CUCM-None-Device-Analyzer/discussions) for questions that aren't bugs or feature requests.
