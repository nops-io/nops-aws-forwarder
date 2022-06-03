import json
import logging
import os

from logs import forward_logs
from parsing import parse
from settings import CT_EVENT_TYPES

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.environ.get("NOPS_LOG_LEVEL", "INFO").upper()))


def check_valid_event_type(event):
    # We only support EC2 Start and Stop for now
    return event["eventName"] in CT_EVENT_TYPES


def lambda_handler(event, context):
    # Event contains an S3 file
    # Read from S3 file
    # For each line in S3 File
    # Send it to API Collector with api_key
    # if good can send it in batch
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"Received Event:{json.dumps(event)}")

    events = transform(parse(event, context))
    aws_account_number = context.invoked_function_arn.split(":")[4]

    forward_logs(events, aws_account_number)

    return {"message": "success"}


def transform(events):
    """Performs transformations on complex events
    Ex: handles special cases with nested arrays of JSON objects
    Args:
        events (dict[]): the list of event dicts we want to transform
    """
    # Remove non cloudtrail event_type

    transformed_events = []
    for event in events:
        if check_valid_event_type(event):
            transformed_events.append(event)
    return transformed_events
