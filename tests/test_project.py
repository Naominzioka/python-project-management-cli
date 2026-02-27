import unittest
import os
import json
import tempfile
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from models.project import Project


class ProjectTests(unittest.TestCase):
    def setUp(self):
        # temporary file for project data
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        Project.projects_data = self.tmp.name
        Project.projects = []
        Project.id_counter = 1

    def tearDown(self):
        try:
            os.remove(self.tmp.name)
        except OSError:
            pass
        Project.projects = []
        Project.id_counter = 1

    def test_create_and_id(self):
        p1 = Project("T1", "D", "2025-12-31", "owner@example.com")
        p2 = Project("T2", "D", "2025-12-31", "owner@example.com")
        self.assertEqual(p1.id, 1)
        self.assertEqual(p2.id, 2)
        self.assertEqual(len(Project.projects), 2)

    def test_due_date_validation(self):
        p = Project("T", "D", "invalid", "o@e.com")
        self.assertEqual(p.due_date, "TBD")
        p2 = Project("T", "D", "2025-01-01", "o@e.com")
        self.assertEqual(p2.due_date, "2025-01-01")

    def test_to_dict(self):
        p = Project("T", "D", "2025-06-30", "o@e.com")
        d = p.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["title"], "T")
        self.assertIn("id", d)

    def test_save_and_load(self):
        Project("T", "D", "2025-06-30", "o@e.com")
        Project.save_projects_to_file()
        # clear and reload
        Project.projects = []
        Project.id_counter = 1
        Project.read_from_file()
        self.assertEqual(len(Project.projects), 1)
        self.assertEqual(Project.projects[0].title, "T")

    def test_delete_project(self):
        p = Project("T", "D", "2025-06-30", "o@e.com")
        Project.save_projects_to_file()
        self.assertTrue(Project.delete_project(p.id))
        self.assertEqual(len(Project.projects), 0)
        self.assertFalse(Project.delete_project(999))


if __name__ == "__main__":
    unittest.main()
