"""GitLab 配置类."""

import os


class GitLabConfig:
    """GitLab 配置类."""

    url: str | None = os.getenv("gitlab_url")
    username: str | None = os.getenv("gitlab_username")
    password: str | None = os.getenv("gitlab_password")
    token: str | None = os.getenv("gitlab_token")
