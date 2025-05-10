import json

from src.utils.task_priority import TaskPriority
from src.utils.task_status import TaskStatus


class Task:
    def __init__(self, description: str, priority: TaskPriority = TaskPriority.MEDIUM, status: TaskStatus = TaskStatus.TO_BE_DONE):
        self.description = description
        self.priority = priority
        self.status = status

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        if not isinstance(description, str):
            raise TypeError('Description must be a string')

        if description == '':
            raise ValueError('Description cannot be empty')

        self._description = description

    @property
    def status(self) -> TaskStatus:
        return self._status

    @status.setter
    def status(self, status: TaskStatus) -> None:
        if not isinstance(status, TaskStatus):
            raise TypeError('Status must be a TaskStatus type')

        self._status = status

    @property
    def priority(self) -> TaskPriority:
        return self._priority

    @priority.setter
    def priority(self, priority: TaskPriority) -> None:
        if not isinstance(priority, TaskPriority):
            raise TypeError('Priority must be a TaskPriority type')

        self._priority = priority

    def __str__(self):
        formatted_status = self.status.name.replace('_', ' ').capitalize()
        formatted_priority = self.priority.name.capitalize()
        return f'{self.description} - {formatted_status} - {formatted_priority}'

    def to_json(self):
        data = {
            "description": self.description,
            "priority": self.priority.name,
            "status": self.status.name,
        }

        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        priority = TaskPriority[data["priority"]]
        status = TaskStatus[data["status"]]

        task = cls(
            data["description"],
            priority,
            status,
        )

        return task