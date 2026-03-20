import unittest
from functions.run_python_file import run_python_file

class TestRunPythonFile(unittest.TestCase):
    def test_run_python_file(self):
        result = run_python_file("calculator", "main.py")
        print(result)
        

        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)

        result = run_python_file("calculator", "tests.py")
        print(result)

        result = run_python_file("calculator", "../main.py")
        print(result)
        self.assertIn('Error: Cannot execute "../main.py" as it is outside the permitted working directory', result)

        result = run_python_file("calculator", "nonexistent.py")
        print(result)
        self.assertIn('Error: "nonexistent.py" does not exist or is not a regular file.', result)

        result = run_python_file("calculator", "lorem.txt")
        print(result)
        self.assertIn('Error: "lorem.txt" is not a Python file', result)

if __name__ == '__main__':
    unittest.main()