import unittest
from src.models.main_model import MainModel

class TestMainModel(unittest.TestCase):

    def setUp(self):
        self.model = MainModel()

    def test_initial_data(self):
        self.assertEqual(self.model.get_data(), [])

    def test_add_data(self):
        self.model.add_data('test_item')
        self.assertIn('test_item', self.model.get_data())

    def test_remove_data(self):
        self.model.add_data('test_item')
        self.model.remove_data('test_item')
        self.assertNotIn('test_item', self.model.get_data())

    def test_data_manipulation(self):
        self.model.add_data('item1')
        self.model.add_data('item2')
        self.model.remove_data('item1')
        self.assertEqual(self.model.get_data(), ['item2'])

if __name__ == '__main__':
    unittest.main()