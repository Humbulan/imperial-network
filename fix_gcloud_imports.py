#!/usr/bin/env python3
import os
import re

# Path to the importing.py file
file_path = 'google-cloud-sdk/lib/googlecloudsdk/core/util/importing.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Replace the imp import with a compatibility layer
new_import = '''import sys
if sys.version_info >= (3, 4):
    import importlib.util
    # Create a compatibility module
    class imp_compat:
        @staticmethod
        def find_module(name, path=None):
            if path is None:
                path = None
            try:
                spec = importlib.util.find_spec(name, path)
                if spec is None:
                    return None
                if spec.origin is None:
                    return None
                return spec.origin, spec.origin, ('.py', 'r', 1)
            except (ImportError, AttributeError, ValueError):
                return None
    imp = imp_compat
else:
    import imp
'''

# Replace the import line
new_content = re.sub(r'import imp', new_import, content)

# Also update the _find_module function to handle the new imp object
new_content = re.sub(
    r'return imp\.find_module\(submodule_name, parent_path\)',
    'return imp.find_module(submodule_name, parent_path)',
    new_content
)

# Write back
with open(file_path, 'w') as f:
    f.write(new_content)

print("Fixed importing.py for Python 3.4+ compatibility")
