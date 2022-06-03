import responses

from logs import forward_logs


@responses.activate
def test_forward_logs():
    rsp1 = responses.Response(
        responses.POST,
        "https://app.nops.io:443/svc/event_collector/v1/cloudtrail_event_collector",
        status=200,
    )

    responses.add(rsp1)

    forward_logs([{"abc": "def"}, {"bcd": "efg"}], "1234")
    assert rsp1.call_count == 1
