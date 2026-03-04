"""GitLab 配置类."""

import os


class GitLabConfig:
    """GitLab 配置类."""

    url: str | None = os.getenv("gitlab_url")
    token: str | None = os.getenv("gitlab_token")
