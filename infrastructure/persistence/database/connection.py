"""SQLite 数据库连接管理"""
import sqlite3
import logging
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """SQLite 数据库连接管理器"""

    def __init__(self, db_path: str):
        """初始化数据库连接

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        self._ensure_database_exists()

    def _ensure_database_exists(self) -> None:
        """确保数据库文件和表结构存在"""
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

        # 创建数据库和表结构
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 返回字典格式

        # 读取 schema.sql 并执行
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
                conn.executescript(schema_sql)
                conn.commit()
                logger.info(f"Database initialized at {self.db_path}")
        else:
            logger.warning(f"Schema file not found: {schema_path}")

        conn.close()

    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接（单例模式）"""
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            # 启用外键约束
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection

    @contextmanager
    def transaction(self):
        """事务上下文管理器

        Usage:
            with db.transaction() as conn:
                conn.execute("INSERT INTO ...")
                conn.execute("UPDATE ...")
        """
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction failed: {e}")
            raise

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """执行 SQL 语句

        Args:
            sql: SQL 语句
            params: 参数元组

        Returns:
            Cursor 对象
        """
        conn = self.get_connection()
        return conn.execute(sql, params)

    def execute_many(self, sql: str, params_list: list) -> None:
        """批量执行 SQL 语句

        Args:
            sql: SQL 语句
            params_list: 参数列表
        """
        conn = self.get_connection()
        conn.executemany(sql, params_list)
        conn.commit()

    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[dict]:
        """查询单条记录

        Args:
            sql: SQL 语句
            params: 参数元组

        Returns:
            字典格式的记录，如果不存在返回 None
        """
        cursor = self.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        """查询多条记录

        Args:
            sql: SQL 语句
            params: 参数元组

        Returns:
            字典列表
        """
        cursor = self.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        """关闭数据库连接"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Database connection closed")


# 全局数据库实例
_db_instance: Optional[DatabaseConnection] = None


def get_database(db_path: str = "data/aitext.db") -> DatabaseConnection:
    """获取全局数据库实例

    Args:
        db_path: 数据库文件路径

    Returns:
        DatabaseConnection 实例
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection(db_path)
    return _db_instance
