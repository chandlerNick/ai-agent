import unittest
from functions.get_file_content import get_file_content

class TestGetFileContent(unittest.TestCase):
    def test_get_file_content(self):
        content = get_file_content("calculator", "lorem.txt")
        
        print(len(content))
        print(content[-100:])
        
        self.assertEqual(content[:11], "Lorem ipsum")
        self.assertEqual(len(content), 10051)

        content = get_file_content("calculator", "main.py")
        print(content)
        self.assertTrue(content.find("def main():") != -1)

        content = get_file_content("calculator", "pkg/calculator.py")
        print(content)
        self.assertTrue(content.find("def _apply_operator(self") != -1)

        content = get_file_content("calculator", "/bin/cat")
        print(content)
        self.assertTrue(content.startswith("Error"))

        content = get_file_content("calculator", "nonexistent.txt")
        print(content)
        self.assertTrue(content.startswith("Error"))

if __name__ == '__main__':
    unittest.main()