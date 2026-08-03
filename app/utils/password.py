"""密码哈希与校验（argon2id）。"""

from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    """对明文密码做 argon2id 哈希。"""
    return _password_hash.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """校验明文密码是否匹配哈希。"""
    return _password_hash.verify(plain_password, password_hash)
