import re
import os
from typing import List
import mccabe
import ast

class Analyzer:
    def check_readiness(self, diff: str, changed_files: List[str]) -> List[str]:
        warnings = []
        
        # 1. Test Detection
        # Check if any .py files were changed that are NOT tests
        has_logic_changes = any(f.endswith('.py') and not f.startswith('tests/') and 'test' not in f for f in changed_files)
        # Check if any test files were changed
        has_tests = any('test' in f for f in changed_files)
        
        if has_logic_changes and not has_tests:
            warnings.append("⚠️  You modified logic files but I don't see any changes in tests.")

        # 2. Secret Scanning (Basic Regex)
        if re.search(r'(?i)API_KEY|SECRET_KEY|AWS_ACCESS_KEY_ID', diff):
             warnings.append("⚠️  Possibility of secrets detected in diff (API_KEY, SECRET_KEY, etc.).")

        # 3. Migration Check (Django specific)
        if any('models.py' in f for f in changed_files) and not any('migrations' in f for f in changed_files):
             warnings.append("⚠️  You changed models.py but didn't generate a migration.")

        # 4. Complexity Check
        for f_path in changed_files:
            # We need to handle the case where we are in a sub-directory
            if f_path.endswith('.py') and os.path.exists(f_path):
                try:
                    with open(f_path, "r") as f:
                        code = f.read()
                    tree = ast.parse(code)
                    visitor = mccabe.PathGraphingAstVisitor()
                    visitor.preorder(tree, visitor)
                    for graph in visitor.graphs.values():
                        complexity = graph.complexity()
                        if complexity > 10:
                            warnings.append(f"⚠️  High cyclomatic complexity ({complexity}) detected in {f_path}:{graph.entity}.")
                except Exception:
                    # Skip files that can't be parsed or read
                    pass

        if not warnings:
            warnings.append("✅ Ready for review!")
            
        return warnings
