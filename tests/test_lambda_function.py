import logging

import responses
from moto import mock_s3

from lambda_function import lambda_handler


@responses.activate
def test_healthcheck(lambda_context, caplog):
    rsp1 = responses.Response(
        responses.POST,
        "https://app.nops.io:443/svc/event_collector/v1/cloudtrail_event_collector",
        status=200,
    )

    responses.add(rsp1)

    event = {"healthcheck": True}
    with caplog.at_level(logging.DEBUG):
        result = lambda_handler(event, lambda_context)
        assert result["healthcheck"] == "ok"

    assert rsp1.call_count == 1


@responses.activate
@mock_s3
def test_lambda_handler(lambda_context, get_lambda_event):
    # End to end test, the same as  test Parsing
    rsp1 = responses.Response(
        responses.POST,
        "https://app.nops.io:443/svc/event_collector/v1/cloudtrail_event_collector",
        status=200,
    )

    responses.add(rsp1)

    event = get_lambda_event()
    result = lambda_handler(event, lambda_context)
    assert result == {"message": "success"}
    assert rsp1.call_count == 1


@responses.activate
def test_healthcheck_failed(lambda_context, caplog):
    rsp1 = responses.Response(
        responses.POST,
        "https://app.nops.io:443/svc/event_collector/v1/cloudtrail_event_collector",
        status=301,
    )

    responses.add(rsp1)

    event = {"healthcheck": True}
    with caplog.at_level(logging.DEBUG):
        result = lambda_handler(event, lambda_context)
        assert result["healthcheck"] == "failed"
    assert rsp1.call_count == 1
