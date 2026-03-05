#!/usr/bin/env python3
import os
import re

# Path to the importing.py file
file_path = 'google-cloud-sdk/lib/googlecloudsdk/core/util/importing.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Replace the imp import with our compatibility module
new_content = content.replace(
    'import imp',
    'from googlecloudsdk.core.util import imp_compat as imp'
)

# Write back
with open(file_path, 'w') as f:
    f.write(new_content)

print("Fixed importing.py to use imp_compat")
