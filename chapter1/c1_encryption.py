from secrets import token_bytes
from typing import Tuple

def random_key(length: int) -> int:
    tp: bytes = token_bytes(length)

    return int.from_bytes(tp, 'big')

def encrypt(origin: str) -> Tuple[int, int]:
    origin_to_bytes: bytes = origin.encode()
    dummy: int = random_key(len(origin_to_bytes))
    origin_key: int = int.from_bytes(origin_to_bytes, 'big')
    encrypted_key: int = origin_key ^ dummy

    return dummy, encrypted_key

def decrypt(key1: int, key2: int) -> str:
    decrypted: int = key1 ^ key2
    origin_key: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, 'big')

    return origin_key.decode()


if __name__ == "__main__":
    key1, key2 = encrypt('My Life!')
    result: str = decrypt(key1, key2)
    print(result)