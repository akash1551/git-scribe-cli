import pytest
import os
from git_scribe.analysis import Analyzer

def test_analyzer_test_detection():
    analyzer = Analyzer()
    diff = "some changes"
    # Case 1: Logic changed, no tests -> Warning
    files = ["src/git_scribe/logic.py", "README.md"]
    warnings = analyzer.check_readiness(diff, files)
    assert any("modified logic files but I don't see any changes in tests" in w for w in warnings)

    # Case 2: Logic changed, tests changed -> No Warning (or Ready)
    files = ["src/git_scribe/logic.py", "tests/test_logic.py"]
    warnings = analyzer.check_readiness(diff, files)
    assert not any("modified logic files but I don't see any changes in tests" in w for w in warnings)

def test_analyzer_secret_scanning():
    analyzer = Analyzer()
    files = ["src/git_scribe/config.py"]
    
    # Secret in diff -> Warning
    diff = "AWS_ACCESS_KEY_ID=AKIA..."
    warnings = analyzer.check_readiness(diff, files)
    assert any("Possibility of secrets detected" in w for w in warnings)

    # No secret -> Ready
    diff = "print('hello')"
    warnings = analyzer.check_readiness(diff, files)
    assert not any("Possibility of secrets detected" in w for w in warnings)

def test_analyzer_complexity(tmp_path):
    analyzer = Analyzer()
    # Create a complex file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "complex_test.py"
    p.write_text("""
def high_complexity(n):
    if n > 0:
        if n > 1:
            if n > 2:
                if n > 3:
                    if n > 4:
                        if n > 5:
                            if n > 6:
                                if n > 7:
                                    if n > 8:
                                        if n > 9:
                                            print(10)
""")
    
    # Threshold is 10 in restored analysis.py
    warnings = analyzer.check_readiness("diff", [str(p)])
    assert any("High cyclomatic complexity" in w for w in warnings)


