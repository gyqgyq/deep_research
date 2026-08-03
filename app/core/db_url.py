"""数据库 URL 规范化与连接参数工具。"""

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def normalize_database_url(url: str) -> str:
    """统一为 SQLAlchemy asyncpg 驱动前缀。"""
    for prefix in (
        "postgresql+psycopg_async://",
        "postgresql+psycopg://",
        "postgres://",
        "postgresql://",
    ):
        if url.startswith(prefix):
            return "postgresql+asyncpg://" + url.removeprefix(prefix)
    return url


def database_connect_args(url: str) -> dict:
    """根据 URL 查询参数构建 connect_args（如 sslmode → ssl）。"""
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    connect_args: dict = {}
    sslmode = query.get("sslmode")
    if sslmode in {"require", "verify-ca", "verify-full"}:
        connect_args["ssl"] = True
    return connect_args


def database_url_for_engine(url: str) -> str:
    """去掉 asyncpg 不支持的 sslmode 查询参数。"""
    parsed = urlparse(url)
    query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True) if k != "sslmode"]
    return urlunparse(parsed._replace(query=urlencode(query)))
