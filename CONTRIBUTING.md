# Contributing to SayerDark

Thank you for your interest in contributing to SayerDark! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section
2. Use the bug report template
3. Include detailed steps to reproduce
4. Add screenshots if applicable
5. Specify your environment details

### Suggesting Features

1. Check if the feature has already been suggested
2. Use the feature request template
3. Explain the problem you're trying to solve
4. Describe the proposed solution
5. List any alternatives you've considered

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature/fix
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SayerDark.git
cd SayerDark
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

## Coding Standards

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write unit tests for new features
- Keep code DRY (Don't Repeat Yourself)

## Documentation

- Update README.md for major changes
- Add comments for complex code
- Document new features
- Update configuration examples

## Testing

1. Run existing tests:
```bash
python -m pytest
```

2. Add new tests for your changes
3. Ensure all tests pass before submitting PR

## Commit Messages

Use clear and descriptive commit messages:
- Start with a verb (Add, Fix, Update, etc.)
- Keep it under 50 characters
- Use present tense
- Reference issues when applicable

Example:
```
Add support for new market parser
Fix price history tracking bug
Update documentation for new feature
```

## Review Process

1. All PRs require at least one review
2. Address review comments
3. Keep PRs focused and small
4. Update PR description if needed

## Getting Help

- Check existing documentation
- Search closed issues
- Join our community chat
- Contact maintainers

Thank you for contributing to SayerDark! 