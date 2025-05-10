from enum import auto

from src.utils.sortable_enum import SortableEnum


class TaskStatus(SortableEnum):
    TO_BE_DONE = auto()
    IN_PROGRESS = auto()
    DONE = auto()