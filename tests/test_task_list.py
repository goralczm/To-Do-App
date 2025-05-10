import json
import unittest

from src.task import Task
from src.task_list import TaskList
from src.utils.task_priority import TaskPriority
from src.utils.task_status import TaskStatus


class TestTaskList(unittest.TestCase):

    def setUp(self):
        self.task_list = TaskList('Test Task List')
        self.medium_priority_done_task = Task('A', TaskPriority.MEDIUM, TaskStatus.DONE)
        self.low_priority_to_be_done_task = Task('B', TaskPriority.LOW, TaskStatus.TO_BE_DONE)
        self.high_priority_to_be_done_task = Task('C', TaskPriority.HIGH, TaskStatus.TO_BE_DONE)
        self.high_priority_in_progress_task = Task('D', TaskPriority.HIGH, TaskStatus.IN_PROGRESS)

    def test_task_list_initialization(self):
        self.assertEqual(self.task_list.name, 'Test Task List')
        self.assertEqual(self.task_list.tasks, {})

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            TaskList(
                name=''
            )

    def test_invalid_name_type(self):
        with self.assertRaises(TypeError):
            TaskList(
                name=42
            )

    def test_add_task(self):
        self.low_priority_to_be_done_task.name = 'B'
        self.task_list.add_task(self.low_priority_to_be_done_task)
        self.assertIn('B', self.task_list.tasks)

    def test_add_duplicate_task(self):
        self.task_list.add_task(self.low_priority_to_be_done_task)
        with self.assertRaises(ValueError):
            self.task_list.add_task(self.low_priority_to_be_done_task)

    def test_remove_task(self):
        self.task_list.add_task(self.low_priority_to_be_done_task)
        self.task_list.remove_task(self.low_priority_to_be_done_task.description)

    def test_remove_task_not_exists(self):
        with self.assertRaises(ValueError):
            self.task_list.remove_task('Not existing task')

    def test_find_task_by_description(self):
        self.low_priority_to_be_done_task.description = 'B'
        self.task_list.add_task(self.low_priority_to_be_done_task)
        self.assertIs(self.task_list.find_task_by_description('B'), self.low_priority_to_be_done_task)

    def test_find_task_by_description_not_exists(self):
        with self.assertRaises(ValueError):
            self.task_list.find_task_by_description('G')

    def test_sort_tasks_by_status(self):
        self.task_list.add_task(self.medium_priority_done_task)
        self.task_list.add_task(self.low_priority_to_be_done_task)
        self.task_list.add_task(self.high_priority_to_be_done_task)
        self.task_list.add_task(self.high_priority_in_progress_task)
        self.task_list.sort_tasks_by_status()
        statuses = [t.status for t in self.task_list.tasks.values()]
        self.assertEqual(statuses, sorted(statuses))

    def test_sort_tasks_by_priority(self):
        self.task_list.add_task(self.medium_priority_done_task)
        self.task_list.add_task(self.low_priority_to_be_done_task)
        self.task_list.add_task(self.high_priority_to_be_done_task)
        self.task_list.add_task(self.high_priority_in_progress_task)
        self.task_list.sort_tasks_by_priority()
        priorities = [t.priority for t in self.task_list.tasks.values()]
        self.assertEqual(priorities, sorted(priorities))

    def test_sort_tasks_by_status_then_priority(self):
        self.task_list.add_task(self.medium_priority_done_task) # C
        self.task_list.add_task(self.low_priority_to_be_done_task) # B
        self.task_list.add_task(self.high_priority_to_be_done_task) # D
        self.task_list.add_task(self.high_priority_in_progress_task) # A
        self.task_list.sort_tasks_by_status_then_priority()
        keys = list(self.task_list.tasks.keys())
        self.assertEqual(keys, ['C', 'B', 'D', 'A'])

    def test_progress(self):
        self.assertEqual(self.task_list.progress, '0/0')
        self.task_list.add_task(self.low_priority_to_be_done_task)
        self.assertEqual(self.task_list.progress, '0/1')
        self.task_list.add_task(self.medium_priority_done_task)
        self.assertEqual(self.task_list.progress, '1/2')
        self.low_priority_to_be_done_task.status = TaskStatus.DONE
        self.assertEqual(self.task_list.progress, '2/2')

    def test_str_representation(self):
        self.task_list.add_task(self.low_priority_to_be_done_task) # B
        self.task_list.add_task(self.medium_priority_done_task) # A
        s = str(self.task_list)
        self.assertIn('Test Task List 1/2', s)
        self.assertIn(str(self.low_priority_to_be_done_task), s)
        self.assertIn(str(self.medium_priority_done_task), s)

    def test_to_json(self):
        self.task_list.add_task(self.low_priority_to_be_done_task)
        self.task_list.add_task(self.medium_priority_done_task)

        task_list_json = self.task_list.to_json()
        data = json.loads(task_list_json)

        self.assertEqual(data['name'], self.task_list.name)
        self.assertIn(self.low_priority_to_be_done_task.to_json(), data['tasks'])
        self.assertIn(self.medium_priority_done_task.to_json(), data['tasks'])

    def test_from_json(self):
        self.task_list.add_task(self.low_priority_to_be_done_task) # B
        self.task_list.add_task(self.medium_priority_done_task) # A

        task_list_json = self.task_list.to_json()
        new_task_list = TaskList.from_json(task_list_json)

        self.assertEqual(new_task_list.name, self.task_list.name)
        self.assertIn('B', new_task_list.tasks)
        self.assertIn('A', new_task_list.tasks)

if __name__ == '__main__': # pragma: no cover
    unittest.main()