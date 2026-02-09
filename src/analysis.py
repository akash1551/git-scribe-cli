from typing import List, Dict
import re

class Analyzer:
    def check_readiness(self, diff: str, changed_files: List[str]) -> List[str]:
        warnings = []
        
        # 1. Test Detection
        has_logic_changes = any(f.endswith('.py') and not f.startswith('tests/') and 'test' not in f for f in changed_files)
        has_tests = any('test' in f for f in changed_files)
        
        if has_logic_changes and not has_tests:
            warnings.append("⚠️  You modified logic files but I don't see any changes in tests.")

        # 2. Secret Scanning (Basic Regex)
        # Very basic check for AWS keys or generic secrets
        if re.search(r'(?i)API_KEY|SECRET_KEY|AWS_ACCESS_KEY_ID', diff):
             warnings.append("⚠️  Possibility of secrets detected in diff (API_KEY, SECRET_KEY, etc.).")

        # 3. Migration Check (Django specific example)
        if any('models.py' in f for f in changed_files) and not any('migrations' in f for f in changed_files):
             warnings.append("⚠️  You changed models.py but didn't generate a migration.")

        if not warnings:
            warnings.append("✅ Ready for review!")
            
        return warnings
