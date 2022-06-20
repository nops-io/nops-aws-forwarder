import base64
import logging
import os

import boto3
import botocore.config

logger = logging.getLogger()


def get_env_var(envvar, default, boolean=False):
    """
    Return the value of the given environment variable with debug logging.
    When boolean=True, parse the value as a boolean case-insensitively.
    """
    value = os.getenv(envvar, default=default)
    if boolean:
        value = value.lower() == "true"
    logger.debug(f"{envvar}: {value}")
    return value


NOPS_API_KEY = ""
NOPS_NO_SSL = False
NOPS_PORT = "443"
NOPS_SKIP_SSL_VALIDATION = True
NOPS_URL = "app.nops.io"
NOPS_FORWARDER_VERSION = "1.0.7"

CT_EVENT_TYPES = [
    "RunInstances",
    "StartInstances",
    "StopInstances",
    "TerminateInstances",
    "PurchaseReservedInstancesOffering",
    "DeleteQueuedReservedInstances",
    "ModifyReservedInstances",
    "AcceptReservedInstancesExchangeQuote",
]


if "NOPS_URL" in os.environ:
    logger.debug("Fetching the API key from environment variable NOPS_URL")
    NOPS_URL = os.environ["NOPS_URL"]

if "NOPS_PORT" in os.environ:
    logger.debug("Fetching the API key from environment variable NOPS_PORT")
    NOPS_PORT = os.environ["NOPS_PORT"]

if "NOPS_SKIP_SSL_VALIDATION" in os.environ:
    NOPS_SKIP_SSL_VALIDATION = os.environ["NOPS_SKIP_SSL_VALIDATION"].upper() == "TRUE"


def get_api_key():
    boto3_config = botocore.config.Config(
        connect_timeout=5, read_timeout=5, retries={"max_attempts": 2}, region_name=os.environ.get("AWS_REGION")
    )
    api_key = ""
    if "NOPS_KMS_API_KEY" in os.environ and os.environ["NOPS_KMS_API_KEY"]:
        ENCRYPTED_API_KEY = os.environ["NOPS_KMS_API_KEY"]
        api_key = boto3.client("kms", config=boto3_config).decrypt(
            CiphertextBlob=base64.b64decode(bytes(ENCRYPTED_API_KEY, "utf-8"))
        )["Plaintext"]
        if type(api_key) is bytes:
            api_key = api_key.decode("utf-8")

    elif "NOPS_API_KEY" in os.environ:
        logger.debug("Fetching the API key from environment variable NOPS_API_KEY")
        api_key = os.environ["NOPS_API_KEY"]

    return api_key.strip()


NOPS_API_KEY = get_api_key()
