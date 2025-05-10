from enum import auto

from src.utils.sortable_enum import SortableEnum


class TaskPriority(SortableEnum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()