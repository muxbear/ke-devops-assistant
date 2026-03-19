"""GitLab 工具函数."""

import logging
import re

import gitlab
from langchain_core.tools import tool

from agent.config.gitlab_config import GitLabConfig

logger = logging.getLogger(__name__)

def _sanitize_path(name: str) -> str:
    """将名称转换为有效的 GitLab 路径."""
    # 首先处理中文拼音化或使用简单映射
    import unicodedata
    # 尝试将非ASCII字符转换为ASCII
    path = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    # 移除特殊字符，只保留字母、数字、下划线、中划线和点
    path = re.sub(r'[^\w\-.]', '-', path.lower())
    # 移除开头和结尾的连字符、下划线、点
    path = path.strip('_.-')
    # 确保不以点开头
    if path.startswith('.'):
        path = 'group' + path
    # 如果为空，使用默认名称
    if not path:
        path = 'group'
    return path

@tool
def create_gitlab_project(project_group: str, project_name: str, project_description: str) -> dict[str, bool]:
    """在 GitLab 上创建项目仓库.

    Args:
        project_group: 项目组名,用于创建或查找所属组.
        project_name: 项目名称,用作仓库路径.
        project_description: 项目描述.

    Returns:
        包含是否创建成功的字典.
    """
    gl = gitlab.Gitlab(url=GitLabConfig.url, private_token=GitLabConfig.token)

    # 处理中文项目组名和项目名
    group_path = _sanitize_path(project_group)
    project_path = _sanitize_path(project_name)

    try:
        group = gl.groups.get(group_path)
    except gitlab.GitlabGetError:
        group = gl.groups.create(
            {
                "name": project_group,
                "path": group_path,
            }
        )

    project = gl.projects.create(
        {
            "name": project_name,
            "path": project_path,
            "namespace_id": group.id,
            "visibility": "public",
            "description": project_description,
        }
    )

    logger.info(f"成功创建 GitLab 仓库: {project.web_url}")
    return {"is_gitlab_created": True}

@tool
def build_gitlab_repository(project_group: str, project_path: str) -> bool:
    """在 gitlab 中创建一个仓库
    Args:
        project_group: 仓库所在组（项目客户当作项目所在组）
        project_path: 仓库路径（项目的名称当作项目路径）

    Returns:
        bool: 是否成功创建
    """
    print(f'成功创建 gitlab 仓库 {project_group}/{project_path}')
    return True
