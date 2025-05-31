# SPYQ Examples

This directory contains example scripts that demonstrate how to use SPYQ for Python code validation.

## Example Scripts

### `validate_script.py`

A command-line tool that validates Python scripts using SPYQ.

**Usage:**
```bash
python examples/validate_script.py path/to/your/script.py
```

### `test_script.py`

An example Python script with intentional style issues for testing SPYQ validation.

## Running the Examples

1. First, make sure SPYQ is installed in your environment:
   ```bash
   pip install -e .
   ```

2. Run the validation example:
   ```bash
   # This should pass validation
   python examples/validate_script.py examples/validate_script.py
   
   # This should fail validation due to style issues
   python examples/validate_script.py examples/test_script.py
   ```

## Docker Testing

You can also run the integration tests using Docker:

```bash
docker-compose up ansible-test
```

This will run the Ansible playbook that tests SPYQ validations in a containerized environment.
