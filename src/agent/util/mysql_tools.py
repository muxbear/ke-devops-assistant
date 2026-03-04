"""MySQL 工具函数."""

import logging
import re

from langchain_core.tools import tool
from sqlalchemy import create_engine, text

from agent.config.mysql_config import MySQLConfig

logger = logging.getLogger(__name__)


def _validate_database_name(database_name: str) -> str:
    """验证并规范化数据库名称（仅小写字母和下划线）.
    
    Args:
        database_name: 原始数据库名称
        
    Returns:
        规范化后的数据库名称
    """
    # 移除非允许字符，只保留小写字母、数字和下划线
    name = re.sub(r'[^a-z0-9_]', '_', database_name.lower())
    # 移除连续和结尾的下划线
    name = re.sub(r'_+', '_', name).strip('_')
    # 确保不为空
    if not name:
        name = 'database'
    # 确保不以数字开头
    elif name[0].isdigit():
        name = 'db_' + name
    return name


def create_mysql_database_impl(database_name: str, charset: str = "utf8mb4") -> dict[str, bool]:
    """创建MySQL数据库的内部实现.
    
    Args:
        database_name: 数据库名称（会自动转换为小写和下划线）
        charset: 字符集，默认utf8mb4
    
    Returns:
        包含创建结果的字典
    """
    # 验证和规范化数据库名称
    validated_name = _validate_database_name(database_name)
    
    # 构建连接URL（不指定数据库，连接到MySQL服务器）
    connection_url = f"mysql+pymysql://{MySQLConfig.username}:{MySQLConfig.password}@{MySQLConfig.url}/"
    
    try:
        engine = create_engine(connection_url)
        with engine.connect() as conn:
            # 检查数据库是否已存在
            check_query = text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :name")
            result = conn.execute(check_query, {"name": validated_name})
            if result.fetchone():
                logger.info(f"数据库已存在: {validated_name}")
                return {"is_database_created": True}
            
            # 创建数据库
            create_query = text(f"CREATE DATABASE `{validated_name}` CHARACTER SET {charset} COLLATE {charset}_unicode_ci")
            conn.execute(create_query)
            conn.commit()
            
            logger.info(f"成功创建数据库: {validated_name}")
            return {"is_database_created": True}
            
    except Exception as e:
        logger.error(f"创建数据库失败: {e}")
        raise


@tool
def create_mysql_database(database_name: str, charset: str = "utf8mb4") -> dict[str, bool]:
    """创建MySQL数据库工具.
    
    Args:
        database_name: 数据库名称（会自动转换为小写和下划线）
        charset: 字符集，默认utf8mb4
    
    Returns:
        包含创建结果的字典
    """
    return create_mysql_database_impl(database_name, charset)