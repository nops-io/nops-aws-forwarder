import gzip
import json
import logging
import os
import urllib
from io import BufferedReader
from io import BytesIO

import boto3
import botocore

from settings import NOPS_FORWARDER_VERSION

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.environ.get("NOPS_LOG_LEVEL", "INFO").upper()))


def parse(event, context):
    """Parse Lambda input to normalized events"""
    metadata = generate_metadata(context)
    try:
        # Route to the corresponding parser
        logger.debug("Start start S3 handler")
        events = s3_handler(event, context, metadata)
        logger.debug("Finished S3 handler")
    except Exception as e:
        # Logs through the socket the error
        err_message = "Error parsing the object. Exception: {} for event {}".format(str(e), event)
        logger.error(err_message)
    return normalize_events(events, metadata)


def generate_metadata(context):
    metadata = {
        "nopssourcecategory": "aws",
        "aws": {
            "function_version": context.function_version,
            "invoked_function_arn": context.invoked_function_arn,
        },
    }
    # Add custom tags here by adding new value with the following format "key1:value1, key2:value2"  - might be subject to modifications
    nops_custom_tags_data = {
        "forwardername": context.function_name.lower(),
        "forwarder_memorysize": context.memory_limit_in_mb,
        "forwarder_version": NOPS_FORWARDER_VERSION,
    }

    metadata["nopstags"] = ",".join(
        filter(
            None,
            [
                "",
                ",".join(["{}:{}".format(k, v) for k, v in nops_custom_tags_data.items()]),
            ],
        )
    )

    return metadata


def merge_dicts(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception(
                    "Conflict while merging metadatas and the log entry at %s" % ".".join(path + [str(key)])
                )
        else:
            a[key] = b[key]
    return a


# Handle S3 events
def s3_handler(event, context, metadata):
    # Need to use path style to access s3 via VPC Endpoints
    # https://github.com/gford1000-aws/lambda_s3_access_using_vpc_endpoint#boto3-specific-notes
    NOPS_USE_VPC = False
    if NOPS_USE_VPC:
        s3 = boto3.client(
            "s3",
            os.environ["AWS_REGION"],
            config=botocore.config.Config(s3={"addressing_style": "path"}),
        )
    else:
        s3 = boto3.client("s3")
    # if this is a S3 event carried in a SNS message, extract it and override the event
    metadata["nopssource"] = "cloudtrail"
    if "Sns" in event["Records"][0]:
        event = json.loads(event["Records"][0]["Sns"]["Message"])

    # Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])

    # Extract the S3 object
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response["Body"]
    data = body.read()

    # Decompress data that has a .gz extension or magic header http://www.onicos.com/staff/iz/formats/gzip.html
    if key[-3:] == ".gz" or data[:2] == b"\x1f\x8b":
        with gzip.GzipFile(fileobj=BytesIO(data)) as decompress_stream:
            # Reading line by line avoid a bug where gzip would take a very long time (>5min) for
            # file around 60MB gzipped
            data = b"".join(BufferedReader(decompress_stream))

    cloud_trail = json.loads(data)
    for event in cloud_trail["Records"]:
        # Create structured object and send it
        yield event


def normalize_events(events, metadata):
    normalized = []
    events_counter = 0

    for event in events:
        events_counter += 1
        if isinstance(event, dict):
            normalized.append(merge_dicts(event, metadata))
        elif isinstance(event, str):
            normalized.append(merge_dicts({"message": event}, metadata))
        else:
            # drop this log
            continue

    return normalized
