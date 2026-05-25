import sys

def handler(event, context):
    return f'This is a lambda container - {sys.version_info}'