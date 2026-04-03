"""Knowledge Triple entity"""
from typing import Optional, Literal
from domain.shared.base_entity import BaseEntity


class KnowledgeTriple(BaseEntity):
    """知识三元组实体

    表示一个知识事实：主语-谓词-宾语
    """

    def __init__(
        self,
        id: str,
        subject: str,
        predicate: str,
        object: str,
        chapter_id: Optional[int] = None,
        note: str = "",
        entity_type: Optional[Literal['character', 'location']] = None,
        importance: Optional[str] = None,
        location_type: Optional[Literal['city', 'region', 'building', 'faction', 'realm']] = None
    ):
        """初始化知识三元组

        Args:
            id: 三元组唯一标识
            subject: 主语
            predicate: 谓词/关系
            object: 宾语
            chapter_id: 关联章节号
            note: 备注说明
            entity_type: 实体类型 ('character' | 'location')
            importance: 重要程度 (人物: 'primary'|'secondary'|'minor', 地点: 'core'|'important'|'normal')
            location_type: 地点类型 ('city'|'region'|'building'|'faction'|'realm')
        """
        super().__init__(id)
        self.subject = subject
        self.predicate = predicate
        self.object = object
        self.chapter_id = chapter_id
        self.note = note
        self.entity_type = entity_type
        self.importance = importance
        self.location_type = location_type

    def __repr__(self) -> str:
        type_str = f" [{self.entity_type}]" if self.entity_type else ""
        return f"<KnowledgeTriple {self.id}{type_str}: {self.subject} -> {self.predicate} -> {self.object}>"
