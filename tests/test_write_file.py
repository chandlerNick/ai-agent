import unittest
from unittest import result
from functions.write_file import write_file

class TestWriteFile(unittest.TestCase):
    def test_write_file(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertIn('Successfully wrote to "lorem.txt"', result)

        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)
        self.assertIn('Successfully wrote to "pkg/morelorem.txt"', result)

        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        self.assertIn('Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory', result)

if __name__ == '__main__':
     unittest.main()