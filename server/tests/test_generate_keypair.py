from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))
from crypto.generate import generate_ed25519_keypair


def test_generate_keypair():
    private_key, public_key = generate_ed25519_keypair()
    assert private_key
    assert public_key
    assert len(private_key) == 64
    assert len(public_key) == 64
    assert private_key != public_key

    private_key_bytes = bytes.fromhex(private_key)
    public_key_bytes = bytes.fromhex(public_key)
    private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    public_key = private_key.public_key()
    assert public_key_bytes == public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
