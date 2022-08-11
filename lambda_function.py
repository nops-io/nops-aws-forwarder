import json
import logging
import os
import urllib

from logs import forward_logs
from parsing import generate_metadata
from parsing import parse
from settings import CT_EVENT_TYPES
from settings import NOPS_FORWARDER_VERSION

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.environ.get("NOPS_LOG_LEVEL", "INFO").upper()))


def check_valid_event_type(event):
    # We only support EC2 Start and Stop for now
    return event["eventName"] in CT_EVENT_TYPES


def get_account_number_from_event(event):
    # This would parse the event to get account number
    # Key format
    # /AWSLogs/o-123456/1234567890/CloudTrail/us-west-2/2022/08/10/1234567890_CloudTrail_us-west-2_20220810T1640Z_ABCdef123.json.gz
    try:
        if "Sns" in event["Records"][0]:
            event = json.loads(event["Records"][0]["Sns"]["Message"])
        aws_account_number = (
            urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"]).split("/")[-1].split("_")[0]
        )
        return aws_account_number
    except Exception:
        return None


def lambda_handler(event, context):
    # Event contains an S3 file
    # Read from S3 file
    # For each line in S3 File
    # Send it to API Collector with api_key
    # if good can send it in batch

    aws_account_number_context = context.invoked_function_arn.split(":")[4]

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"Received Event:{json.dumps(event)}")
        logger.debug(f"Forwarder version: {NOPS_FORWARDER_VERSION}")
        if "healthcheck" in event:
            event = generate_metadata(context)
            event["nopssource"] = "lambda_healthcheck"
            forward_logs(
                [event],
                aws_account_number_context,
            )
            return {"message": "success", "healthcheck": "ok"}

    events = transform(parse(event, context))

    aws_account_number = get_account_number_from_event(event) or aws_account_number_context
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
