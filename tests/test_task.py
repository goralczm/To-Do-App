import json
import unittest

from src.task import Task, TaskPriority, TaskStatus


class TestTask(unittest.TestCase):

    def setUp(self):
        self.laundry_task = Task(
            description="Do laundry",
            priority=TaskPriority.HIGH,
            status=TaskStatus.IN_PROGRESS
        )

    def test_task_initialization(self):
        self.assertEqual(self.laundry_task.description, "Do laundry")
        self.assertEqual(self.laundry_task.priority, TaskPriority.HIGH)
        self.assertEqual(self.laundry_task.status, TaskStatus.IN_PROGRESS)

    def test_empty_description(self):
        with self.assertRaises(ValueError):
            self.laundry_task.description = ''

    def test_invalid_type_description(self):
        with self.assertRaises(TypeError):
            Task(
                description=42,
                priority=TaskPriority.HIGH,
                status=TaskStatus.TO_BE_DONE,
            )

    def test_invalid_type_priority(self):
        with self.assertRaises(TypeError):
            Task(
                description='New Task',
                priority='HIGH',
                status=TaskStatus.TO_BE_DONE,
            )

    def test_invalid_type_status(self):
        with self.assertRaises(TypeError):
            Task(
                description='New Task',
                priority=TaskPriority.HIGH,
                status='Done',
            )

    def test_change_status(self):
        self.assertEqual(self.laundry_task.status, TaskStatus.IN_PROGRESS)
        self.laundry_task.status = TaskStatus.DONE
        self.assertEqual(self.laundry_task.status, TaskStatus.DONE)

    def test_str_representation(self):
        self.assertEqual(str(self.laundry_task), 'Do laundry - In progress - High')

    def test_to_json(self):
        task_json = self.laundry_task.to_json()
        data = json.loads(task_json)

        self.assertEqual(data["description"], self.laundry_task.description)
        self.assertEqual(data["priority"], "HIGH")
        self.assertEqual(data["status"], "IN_PROGRESS")

    def test_from_json(self):
        task_json = self.laundry_task.to_json()
        new_task = Task.from_json(task_json)

        self.assertEqual(new_task.description, self.laundry_task.description)
        self.assertEqual(new_task.priority, self.laundry_task.priority)
        self.assertEqual(new_task.status, self.laundry_task.status)

if __name__ == '__main__': # pragma: no cover
    unittest.main()