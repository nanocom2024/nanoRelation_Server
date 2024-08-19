from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


def generate_ed25519_keypair():
    '''
    Generate a new Ed25519 keypair.

    Returns:
        (private_key, public_key)
    '''

    private_key = Ed25519PrivateKey.generate()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    private_key = private_key_bytes.hex()
    public_key = public_key_bytes.hex()

    return private_key, public_key


if __name__ == '__main__':
    private_key, public_key = generate_ed25519_keypair()
    print(f'private_key: {private_key}')
    print(f'public_key: {public_key}')

    # 本当に公開鍵から秘密鍵を復元できるか確認
    private_key_bytes = bytes.fromhex(private_key)
    public_key_bytes = bytes.fromhex(public_key)
    private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    public_key = private_key.public_key()
    assert public_key_bytes == public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    print('Test passed')
