import json

from src.task import Task, TaskStatus


class TaskList:
    def __init__(self, name: str):
        self.name = name
        self.tasks = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError('Name must be a string')

        if name == '':
            raise ValueError('Name cannot be empty')

        self._name = name

    @property
    def progress(self) -> str:
        done = sum([1 for task in self.tasks.values() if task.status == TaskStatus.DONE])
        tasks_count = len(self.tasks)
        return f'{done}/{tasks_count}'

    def add_task(self, task: Task):
        if task.description in self.tasks:
            raise ValueError('There is already task with this description')

        self.tasks[task.description] = task

    def remove_task(self, task_description: str):
        if task_description not in self.tasks:
            raise ValueError('No task with provided description')

        del self.tasks[task_description]

    def find_task_by_description(self, task_description: str) -> Task:
        if task_description in self.tasks:
            return self.tasks[task_description]

        raise ValueError('No task with provided description')

    def sort_tasks_by_status(self):
        self.tasks = {k: v for k, v in sorted(self.tasks.items(), key=lambda task: task[1].status)}

    def sort_tasks_by_status_then_priority(self):
        self.tasks = {k: v for k, v in sorted(self.tasks.items(), key=lambda task: (task[1].status, task[1].priority))}

    def sort_tasks_by_priority(self):
        self.tasks = {k: v for k, v in sorted(self.tasks.items(), key=lambda task: task[1].priority)}

    def __str__(self) -> str:
        formatted_tasks = []
        for index, task in enumerate(self.tasks.values()):
            prefix = '├' if index != len(self.tasks) - 1 else '└'
            formatted_tasks.append(f'\t {prefix} {task}')

        return f'{self.name} {self.progress}\n' + '\n'.join(formatted_tasks)

    def to_json(self) -> str:
        data = {
            "name": self.name,
            "tasks": [
                task.to_json() for task in self.tasks.values()
            ],
        }

        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str) -> "TaskList":
        data = json.loads(json_str)

        task_list = cls(
            data["name"],
        )

        for task in data["tasks"]:
            task_list.add_task(
                Task.from_json(task)
            )

        return task_list