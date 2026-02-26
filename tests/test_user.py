import unittest
import os
import json
import tempfile
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from models.user import User


class UserTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        User.users_data = self.tmp.name
        User.users = []

    def tearDown(self):
        try:
            os.remove(self.tmp.name)
        except OSError:
            pass

    def test_add_and_save(self):
        User("Alice", "alice@example.com")
        User.save_users_to_file()
        with open(User.users_data) as f:
            data = json.load(f)
        self.assertEqual(data[0]["name"], "Alice")
        self.assertEqual(data[0]["email"], "alice@example.com")

    def test_load_from_file(self):
        with open(User.users_data, "w") as f:
            json.dump([{"name": "Bob", "email": "bob@x.com"}], f)
        User.users = []
        User.read_from_file()
        self.assertEqual(len(User.users), 1)
        self.assertEqual(User.users[0].name, "Bob")
        self.assertEqual(User.users[0].email, "bob@x.com")


if __name__ == "__main__":
    unittest.main()
