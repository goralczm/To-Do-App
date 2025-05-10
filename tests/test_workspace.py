import os
import shutil
import tempfile
import unittest

from src.task_list import TaskList
from src.workspace import Workspace


class TestWorkspace(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.tmpdir)

        self.workspace = Workspace('Test Workspace')

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.tmpdir)

    def test_workspace_initialization(self):
        self.assertEqual(self.workspace.name, 'Test Workspace')
        self.assertEqual(self.workspace.task_lists, {})

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Workspace('')

    def test_invalid_name_type(self):
        with self.assertRaises(TypeError):
            Workspace(123)

    def test_add_task_list(self):
        task_list = TaskList('List 1')
        self.workspace.add_task_list(task_list)
        self.assertIn('List 1', self.workspace.task_lists)
        self.assertIs(self.workspace.task_lists['List 1'], task_list)

    def test_add_duplicate_task_list(self):
        first = TaskList('List 1')
        second = TaskList('List 1')
        self.workspace.add_task_list(first)
        with self.assertRaises(ValueError):
            self.workspace.add_task_list(second)

    def test_remove_task_list(self):
        task_list = TaskList('List 1')
        self.workspace.add_task_list(task_list)
        self.workspace.remove_task_list(task_list.name)
        self.assertNotIn('List 1', self.workspace.task_lists)

    def test_remove_task_list_not_exists(self):
        with self.assertRaises(KeyError):
            self.workspace.remove_task_list('List 2')

    def test_find_task_list_by_name(self):
        task_list = TaskList('List 1')
        self.workspace.add_task_list(task_list)
        found = self.workspace.find_task_list_by_name('List 1')
        self.assertIs(found, task_list)

    def test_find_task_list_by_name_not_exists(self):
        with self.assertRaises(ValueError):
            self.workspace.find_task_list_by_name('List 2')

    def test_sort_tasks_by_status(self):
        a = TaskList('A')
        b = TaskList('B')
        self.workspace.add_task_list(a)
        self.workspace.add_task_list(b)
        self.workspace.sort_tasks_by_status()

    def test_sort_tasks_by_priority(self):
        a = TaskList('A')
        b = TaskList('B')
        self.workspace.add_task_list(a)
        self.workspace.add_task_list(b)
        self.workspace.sort_tasks_by_priority()

    def test_sort_tasks_by_status_then_priority(self):
        a = TaskList('A')
        b = TaskList('B')
        self.workspace.add_task_list(a)
        self.workspace.add_task_list(b)
        self.workspace.sort_tasks_by_status_then_priority()

    def test_str_representation(self):
        a = TaskList('ListX')
        self.workspace.add_task_list(a)
        s = str(self.workspace)
        expected = 'Test Workspace\n └ TaskList(ListX)'
        self.assertEqual(s, expected)

    def test_to_json(self):
        a = TaskList('X')
        b = TaskList('Y')
        self.workspace.add_task_list(a)
        self.workspace.add_task_list(b)
        j = self.workspace.to_json()
        data = json.loads(j)
        self.assertEqual(data["name"], 'Test Workspace')
        # order of lists doesn’t matter, but both dicts should appear
        self.assertCountEqual(data["task_list"], [{"name": "X", "dummy": True}, {"name": "Y", "dummy": True}])

    def test_from_json(self):
        # build a JSON blob
        blob = {
            "name": "Imported",
            "task_list": [
                {"name": "L1", "dummy": True},
                {"name": "L2", "dummy": True},
            ]
        }
        j = json.dumps(blob)
        # patch TaskList.from_json so Workspace.from_json uses our dummy
        with patch.object(TaskList, 'from_json', side_effect=TaskList.from_json):
            ws2 = Workspace.from_json(j)
        self.assertEqual(ws2.name, "Imported")
        self.assertIn("L1", ws2.task_lists)
        self.assertIn("L2", ws2.task_lists)
        self.assertIsInstance(ws2.task_lists["L1"], TaskList)
        self.assertIsInstance(ws2.task_lists["L2"], TaskList)

    def test_save_to_file_and_load_from_file(self):
        # prepare workspace with one dummy list
        a = TaskList('SaveMe')
        self.workspace.add_task_list(a)
        # patch to_json/from_json to avoid real TaskList
        with patch.object(Workspace, 'to_json', return_value='{"name":"Test","task_list":[]}'):
            # save
            self.workspace.save_to_file('test.json')
        self.assertTrue(os.path.isdir('saves'))
        path = os.path.join('saves', 'test.json')
        self.assertTrue(os.path.isfile(path))
        # write a known JSON and load
        with open(path, 'w') as f:
            f.write('{"name":"Reload","task_list":[{"name":"TL","dummy":true}]}')
        with patch.object(TaskList, 'from_json', side_effect=TaskList.from_json):
            loaded = Workspace.load_from_file('test.json')
        self.assertEqual(loaded.name, 'Reload')
        self.assertIn('TL', loaded.task_lists)
        self.assertIsInstance(loaded.task_lists['TL'], TaskList)

if __name__ == '__main__':
    unittest.main()