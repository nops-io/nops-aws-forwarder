import logging
import os

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
NOPS_FORWARDER_VERSION = "1.0.1"

CT_EVENT_TYPES = [
    "RunInstances", 
    "StartInstances", 
    "StopInstances", 
    "TerminateInstances", 
    "PurchaseReservedInstancesOffering",
    "DeleteQueuedReservedInstances",
    "ModifyReservedInstances",
    "AcceptReservedInstancesExchangeQuote"
]


if "NOPS_API_KEY" in os.environ:
    logger.debug("Fetching the Datadog API key from environment variable NOPS_API_KEY")
    NOPS_API_KEY = os.environ["NOPS_API_KEY"]

if "NOPS_URL" in os.environ:
    logger.debug("Fetching the Datadog API key from environment variable NOPS_URL")
    NOPS_URL = os.environ["NOPS_URL"]

if "NOPS_PORT" in os.environ:
    logger.debug("Fetching the Datadog API key from environment variable NOPS_PORT")
    NOPS_PORT = os.environ["NOPS_PORT"]

if "NOPS_SKIP_SSL_VALIDATION" in os.environ:
    NOPS_SKIP_SSL_VALIDATION = os.environ["NOPS_SKIP_SSL_VALIDATION"].upper() == "TRUE"
