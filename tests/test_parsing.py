from moto import mock_s3

from lambda_function import transform
from parsing import parse


@mock_s3
def test_s3_handler(get_lambda_event, lambda_context):
    event = get_lambda_event()
    normalized_logs = parse(event, lambda_context)
    events = transform(normalized_logs)
    assert events
