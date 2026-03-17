#!/usr/bin/env python3
"""Validate ast-grep rule YAML structure."""
import yaml
import sys
from pathlib import Path


def validate_rule(file_path):
    """Validate a single rule file."""
    try:
        content = Path(file_path).read_text()
    except FileNotFoundError:
        print(f"❌ {file_path} - File not found")
        return False
    except Exception as e:
        print(f"❌ {file_path} - Cannot read: {e}")
        return False

    # First check if YAML is valid
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"❌ {file_path} - Invalid YAML: {e}")
        return False

    if data is None:
        print(f"❌ {file_path} - Empty YAML file")
        return False

    errors = []

    # Check required fields
    required = ['id', 'language', 'severity', 'message', 'rule']
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Check constraints/utils/transform at wrong level (common mistake)
    if 'rule' in data and isinstance(data['rule'], dict):
        misplaced_fields = ['constraints', 'utils', 'transform', 'fix']
        for field in misplaced_fields:
            if field in data['rule']:
                errors.append(f"{field} inside rule: - must be at TOP LEVEL")

    # Check severity is valid
    if 'severity' in data:
        valid_severities = ['error', 'warning', 'hint', 'info']
        if data['severity'] not in valid_severities:
            errors.append(f"Invalid severity '{data['severity']}' - must be one of: {', '.join(valid_severities)}")

    # Check rule structure
    if 'rule' in data and isinstance(data['rule'], dict):
        rule = data['rule']
        # Check for multiple keys that should be wrapped in all:/any:
        complex_keys = ['pattern', 'all', 'any', 'kind', 'regex', 'has', 'inside', 'not', 'matches']
        found_keys = [k for k in rule.keys() if k in complex_keys]

        # If we have pattern + other conditions, they should be in 'all'
        if 'pattern' in rule and len(found_keys) > 1:
            if 'all' not in rule and 'any' not in rule:
                errors.append(f"Multiple rule conditions ({', '.join(found_keys)}) should be wrapped in 'all:' or 'any:'")

    # Check for duplicate keys by re-parsing with custom constructor
    try:
        class DuplicateKeyChecker(yaml.SafeLoader):
            def construct_mapping(self, node, deep=False):
                mapping = {}
                for key_node, value_node in node.value:
                    key = self.construct_object(key_node, deep=deep)
                    if key in mapping:
                        errors.append(f"Duplicate key in YAML: '{key}'")
                    mapping[key] = self.construct_object(value_node, deep=deep)
                return mapping

        yaml.load(content, Loader=DuplicateKeyChecker)
    except Exception:
        pass  # Already caught above

    if errors:
        print(f"❌ {file_path}")
        for err in errors:
            print(f"   - {err}")
        return False
    else:
        print(f"✓ {file_path}")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate-rule.py <rule-file.yml> [rule-file2.yml ...]")
        print("")
        print("Validates ast-grep rule YAML files for common structural errors:")
        print("  - Missing required fields (id, language, severity, message, rule)")
        print("  - constraints/utils/transform inside rule: (must be top-level)")
        print("  - Multiple conditions not wrapped in all:/any:")
        print("  - Duplicate YAML keys")
        print("  - Invalid severity values")
        sys.exit(1)

    all_valid = True
    for path in sys.argv[1:]:
        if not validate_rule(path):
            all_valid = False

    if all_valid:
        print("\n✓ All rules valid")
    else:
        print("\n❌ Some rules have errors")

    sys.exit(0 if all_valid else 1)
