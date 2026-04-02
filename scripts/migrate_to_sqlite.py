"""数据迁移脚本：JSON → SQLite"""
import sys
import json
import logging
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from infrastructure.persistence.database.connection import get_database
from infrastructure.persistence.database.sqlite_novel_repository import SqliteNovelRepository
from infrastructure.persistence.database.sqlite_chapter_repository import SqliteChapterRepository
from infrastructure.persistence.database.sqlite_knowledge_repository import SqliteKnowledgeRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_novels():
    """迁移所有小说数据"""
    db = get_database()
    novel_repo = SqliteNovelRepository(db)
    chapter_repo = SqliteChapterRepository(db)
    knowledge_repo = SqliteKnowledgeRepository(db)

    novels_dir = Path("data/novels")
    if not novels_dir.exists():
        logger.warning("No novels directory found")
        return

    migrated_count = 0
    for novel_dir in novels_dir.iterdir():
        if not novel_dir.is_dir():
            continue

        try:
            migrate_single_novel(novel_dir, novel_repo, chapter_repo, knowledge_repo)
            migrated_count += 1
        except Exception as e:
            logger.error(f"Failed to migrate {novel_dir.name}: {e}")

    logger.info(f"Migration completed: {migrated_count} novels migrated")


def migrate_single_novel(novel_dir: Path, novel_repo, chapter_repo, knowledge_repo):
    """迁移单个小说"""
    novel_id = novel_dir.name
    logger.info(f"Migrating novel: {novel_id}")

    # 1. 迁移小说元数据（从目录名推断）
    from domain.novel.entities.novel import Novel
    from domain.novel.value_objects.novel_id import NovelId

    # 尝试从 knowledge 文件获取标题
    knowledge_file = novel_dir / "novel_knowledge.json"
    title = "未命名小说"
    if knowledge_file.exists():
        with open(knowledge_file, 'r', encoding='utf-8') as f:
            knowledge_data = json.load(f)
            # 从 premise_lock 提取标题（简化处理）
            premise = knowledge_data.get('premise_lock', '')
            if premise:
                title = premise[:50]  # 取前50字作为标题

    novel = Novel(
        id=NovelId(novel_id),
        title=title,
        author="未知作者",  # 默认作者
        target_chapters=5  # 默认值
    )
    novel_repo.save(novel)

    # 2. 迁移章节
    chapters_dir = novel_dir / "chapters"
    if chapters_dir.exists():
        for chapter_file in sorted(chapters_dir.glob("*.json")):
            migrate_chapter(chapter_file, novel_id, chapter_repo)

    # 3. 迁移知识库（三元组）
    if knowledge_file.exists():
        migrate_knowledge(knowledge_file, novel_id, knowledge_repo)

    logger.info(f"✓ Migrated novel: {novel_id}")


def migrate_chapter(chapter_file: Path, novel_id: str, chapter_repo):
    """迁移单个章节"""
    with open(chapter_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    from domain.novel.entities.chapter import Chapter, ChapterStatus
    from domain.novel.value_objects.chapter_id import ChapterId
    from domain.novel.value_objects.novel_id import NovelId

    # 映射状态
    status_map = {
        'draft': ChapterStatus.DRAFT,
        'reviewing': ChapterStatus.REVIEWING,
        'completed': ChapterStatus.COMPLETED
    }
    status = status_map.get(data.get('status', 'draft'), ChapterStatus.DRAFT)

    chapter = Chapter(
        id=data['id'],
        novel_id=NovelId(novel_id),
        number=data['number'],
        title=data.get('title', ''),
        content=data.get('content', ''),
        status=status
    )
    chapter_repo.save(chapter)
    logger.info(f"  ✓ Migrated chapter {chapter.number}")


def migrate_knowledge(knowledge_file: Path, novel_id: str, knowledge_repo):
    """迁移知识库"""
    with open(knowledge_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    knowledge_repo.save_all(novel_id, data)
    logger.info(f"  ✓ Migrated knowledge: {len(data.get('facts', []))} triples")


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Starting migration: JSON → SQLite")
    logger.info("=" * 60)
    migrate_novels()
    logger.info("=" * 60)
    logger.info("Migration completed!")
    logger.info("=" * 60)
