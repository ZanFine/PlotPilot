"""
数据库迁移脚本：为 triples 表添加新字段

添加字段：
- entity_type: 实体类型 ('character' | 'location')
- importance: 重要程度
- location_type: 地点类型
"""
import sqlite3
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.persistence.database.connection import DatabaseConnection


def migrate_add_triple_fields():
    """为 triples 表添加新字段"""
    db_path = "data/aitext.db"

    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(triples)")
        columns = [row[1] for row in cursor.fetchall()]

        # 添加 entity_type 字段
        if 'entity_type' not in columns:
            print("添加 entity_type 字段...")
            cursor.execute("ALTER TABLE triples ADD COLUMN entity_type TEXT")
            print("✓ entity_type 字段已添加")
        else:
            print("✓ entity_type 字段已存在")

        # 添加 importance 字段
        if 'importance' not in columns:
            print("添加 importance 字段...")
            cursor.execute("ALTER TABLE triples ADD COLUMN importance TEXT")
            print("✓ importance 字段已添加")
        else:
            print("✓ importance 字段已存在")

        # 添加 location_type 字段
        if 'location_type' not in columns:
            print("添加 location_type 字段...")
            cursor.execute("ALTER TABLE triples ADD COLUMN location_type TEXT")
            print("✓ location_type 字段已添加")
        else:
            print("✓ location_type 字段已存在")

        # 创建新索引
        print("创建索引...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_triples_entity_type
            ON triples(novel_id, entity_type)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_triples_importance
            ON triples(importance)
        """)
        print("✓ 索引已创建")

        conn.commit()
        print("\n✅ 数据库迁移完成！")

        # 显示统计信息
        cursor.execute("SELECT COUNT(*) FROM triples")
        total = cursor.fetchone()[0]
        print(f"\n当前三元组总数: {total}")

        cursor.execute("SELECT COUNT(*) FROM triples WHERE entity_type IS NOT NULL")
        typed = cursor.fetchone()[0]
        print(f"已分类三元组: {typed}")
        print(f"未分类三元组: {total - typed}")

    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    migrate_add_triple_fields()
