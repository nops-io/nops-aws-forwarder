from unittest.mock import MagicMock

import boto3
import pytest
from moto import mock_s3

from parsing import s3_handler


@pytest.fixture
def lambda_context():
    mock_context = MagicMock()
    mock_context.function_name.lower.return_value = "forwarder"
    mock_context.function_version = 1
    mock_context.invoked_function_arn = (
        "arn:aws:lambda:eu-west-1:123456789012:function:ExampleLambdaFunctionResourceName-ABCDEF"
    )
    mock_context.memory_limit_in_mb = 1
    return mock_context


@pytest.fixture
def get_lambda_event():
    @mock_s3
    def get_event():
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {"name": "test_bucket"},
                        "object": {"key": "1234567890-west-2_20220508T0000Z_Wy0kl7YSKHsbaaaa.json.gz"},
                    }
                }
            ]
        }

        conn = boto3.resource("s3")
        # We need to create the bucket since this is all in Moto's 'virtual' AWS account

        conn.create_bucket(Bucket="test_bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})

        conn.Bucket("test_bucket").upload_file(
            "tests/data/1234567890-west-2_20220508T0000Z_Wy0kl7YSKHsbaaaa.json.gz",
            "1234567890-west-2_20220508T0000Z_Wy0kl7YSKHsbaaaa.json.gz",
        )
        logs = s3_handler(event, {}, {})
        for log in logs:
            assert log
        return event

    return get_event
