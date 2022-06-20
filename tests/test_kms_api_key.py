import base64

import boto3
from moto import mock_kms

from settings import get_api_key


@mock_kms
def test_kms_api_key(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-2")

    conn = boto3.client("kms", "us-west-2")
    key = conn.create_key(Description="nops/key")
    key_id = key["KeyMetadata"]["KeyId"]

    conn.generate_data_key(
        KeyId=key_id,
        NumberOfBytes=32,
    )
    ciphertext = conn.encrypt(Plaintext="1234.abcdef", KeyId=key_id)
    encrypted_key = base64.b64encode(ciphertext["CiphertextBlob"])
    monkeypatch.setenv("NOPS_API_KEY", "WRONG_KEY")
    monkeypatch.setenv("NOPS_KMS_API_KEY", encrypted_key.decode("utf-8"))
    NOPS_API_KEY = get_api_key()

    assert NOPS_API_KEY == "1234.abcdef"
