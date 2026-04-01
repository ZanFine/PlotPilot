"""生成结果 DTO"""
from dataclasses import dataclass
from typing import Optional
from domain.novel.value_objects.consistency_report import ConsistencyReport


@dataclass(frozen=True)
class GenerationResult:
    """章节生成结果值对象

    包含生成的内容和相关元数据
    """
    content: str
    consistency_report: ConsistencyReport
    context_used: str
    token_count: int

    def __post_init__(self):
        if not self.content or not self.content.strip():
            raise ValueError("content cannot be empty")
        if self.token_count < 0:
            raise ValueError("token_count must be non-negative")
        if not self.context_used:
            raise ValueError("context_used cannot be empty")
