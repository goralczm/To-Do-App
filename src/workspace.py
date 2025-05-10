import json
import pathlib

from src.task_list import TaskList


class Workspace:
    def __init__(self, name: str):
        self.name = name
        self.task_lists = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError('Name must be a string')

        if name == '':
            raise ValueError('Name cannot be empty')

        self._name = name

    def add_task_list(self, task_list: TaskList):
        self.task_lists[task_list.name] = task_list

    def remove_task_list(self, task_list_name: str):
        if task_list_name not in self.task_lists:
            raise KeyError('No task list with provided name')

        del self.task_lists[task_list_name]

    def find_task_list_by_name(self, name: str) -> TaskList:
        if name in self.task_lists:
            return self.task_lists[name]

        raise ValueError('No task list with provided name')

    def sort_tasks_by_status(self):
        for task_list in self.task_lists.values():
            task_list.sort_tasks_by_status()

    def sort_tasks_by_status_then_priority(self):
        for task_list in self.task_lists.values():
            task_list.sort_tasks_by_status_then_priority()

    def sort_tasks_by_priority(self):
        for task_list in self.task_lists.values():
            task_list.sort_tasks_by_priority()

    def __str__(self):
        return f'{self.name}\n' + '\n'.join([f' └ {task_list}' for task_list in self.task_lists.values()])

    def to_json(self):
        data = {
            "name": self.name,
            "task_list": [
                task_list.to_json() for task_list in self.task_lists.values()
            ],
        }

        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)

        workspace = cls(
            data["name"],
        )

        for task_list in data["task_list"]:
            workspace.add_task_list(
                TaskList.from_json(task_list)
            )

        return workspace

    def save_to_file(self, file_name: str):
        path = pathlib.Path('saves')
        path.mkdir(parents=True, exist_ok=True)

        with open(f'saves/{file_name}', 'w') as output_file:
            output_file.write(self.to_json())

    @classmethod
    def load_from_file(cls, file_name: str) -> "Workspace":
        path = pathlib.Path('saves')
        path.mkdir(parents=True, exist_ok=True)

        with open(f'saves/{file_name}', 'r') as input_file:
            saved_json = input_file.read()

            return Workspace.from_json(saved_json)
