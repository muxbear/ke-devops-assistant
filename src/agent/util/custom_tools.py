from langchain_core.tools import tool

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

@tool
def build_mysql_db(database_name: str) -> bool:
    """在 mysql 中创建一个数据库
    Args:
        database_name: 数据库名称

    Returns:
        bool: 是否成功创建
    """
    print(f'成功创建 mysql 数据库 {database_name}')
    return True
