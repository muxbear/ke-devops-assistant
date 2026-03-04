"""MySQL 配置类."""

import os


class MySQLConfig:
    """MySQL 配置类."""

    url: str | None = os.getenv("mysql_url")
    username: str | None = os.getenv("mysql_username")
    password: str | None = os.getenv("mysql_password")