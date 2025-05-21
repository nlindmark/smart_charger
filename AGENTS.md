# AGENTS Instructions

## Setup

To run tests and development tools for this repository, install the recommended Python packages:

```bash
pip install -U pytest pytest-cov flake8 black
```

These packages are used for testing, coverage reporting, linting and code formatting.

## Testing

Run the following command to execute the test suite:

```bash
pytest
```

If no tests are present, pytest will report `collected 0 items`. You can add tests under a `tests/` directory in the future.

