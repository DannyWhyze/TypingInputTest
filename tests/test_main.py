import unittest
from main import create_app  # Assuming create_app is a function that initializes the app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def test_app_initialization(self):
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.title, "Expected Title")  # Replace with actual expected title

    def test_main_window_setup(self):
        main_window = self.app.main_window
        self.assertIsNotNone(main_window)
        self.assertTrue(main_window.isVisible())

if __name__ == '__main__':
    unittest.main()