import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(message)s'
)

log = logging.getLogger(__name__)

def handler(event, context):
    log.info('This is a log message')
    return 'This is a lambda function'