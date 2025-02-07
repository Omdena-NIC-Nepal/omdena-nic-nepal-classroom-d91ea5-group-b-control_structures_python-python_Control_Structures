import io
import sys
import pytest
# import assignment  # Assumes the student's solution is in assignment.py

import nbconvert
import io

def notebook_to_python(notebook_path):
    """Convert Jupyter notebook to Python script"""
    exporter = nbconvert.PythonExporter()
    python_code, _ = exporter.from_filename(notebook_path)
    return python_code

# In test file
import importlib.util
import sys

def import_notebook_module(notebook_path):
    """Dynamically import notebook as a module"""
    module_name = 'assignment'
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    
    with open(notebook_path, 'r') as f:
        notebook_content = nbconvert.PythonExporter().from_filename(notebook_path)[0]
    
    exec(notebook_content, module.__dict__)
    return module

# Then use in tests
assignment = import_notebook_module('assignment.ipynb')

def test_while_loop_even_numbers(capsys):
    """Test the while loop for printing even numbers up to 16"""
    assignment.while_loop()
    captured = capsys.readouterr().out.strip().split('\n')
    
    # Expected output: even numbers from 0 to 16
    expected = [str(x) for x in range(0, 18, 2)]
    
    assert len(captured) == len(expected), "Incorrect number of printed numbers"
    for actual, expect in zip(captured, expected):
        assert actual.strip() == expect, f"Expected {expect}, got {actual}"

def test_for_loop_skip_divisible_by_3(capsys):
    """Test for loop that skips numbers divisible by 3"""
    assignment.for_loop_continue()
    captured = capsys.readouterr().out.strip().split('\n')
    
    # Expected numbers: 1,2,4,5,7,8,10,11,13,14
    expected = [str(x) for x in range(1, 16) if x % 3 != 0]
    
    assert len(captured) == len(expected), "Incorrect number of printed numbers"
    for actual, expect in zip(captured, expected):
        assert actual.strip() == expect, f"Expected {expect}, got {actual}"

def test_number_classification():
    """Test if-else number classification"""
    # Capture stdout
    def test_input(input_val):
        # Redirect stdin and stdout
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(str(input_val))
        
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the function
        try:
            assignment.number_classification()
        finally:
            # Restore stdin and stdout
            sys.stdin = old_stdin
            sys.stdout = sys.__stdout__
        
        return captured_output.getvalue().strip()

    # Test cases
    assert "negative" in test_input(-5).lower(), "Failed to identify negative number"
    assert "positive" in test_input(10).lower(), "Failed to identify positive number"
    assert "zero" in test_input(0).lower(), "Failed to identify zero"

def test_multiplication_table(capsys):
    """Test nested loops multiplication table"""
    assignment.multiplication_table()
    captured = capsys.readouterr().out.strip().split('\n')
    
    # Check total number of lines (5x5 = 25 lines)
    assert len(captured) == 25, "Incorrect number of multiplication table rows"
    
    # Verify first few entries
    expected_start = [
        "1 x 1 = 1",
        "1 x 2 = 2",
        "1 x 3 = 3",
        "1 x 4 = 4",
        "1 x 5 = 5"
    ]
    
    for actual, expect in zip(captured[:5], expected_start):
        assert actual.strip() == expect, f"Incorrect multiplication table start: {actual}"