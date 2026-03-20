import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_get_files_info(self):
        # Assuming the current directory has some files and directories for testing
        result = get_files_info(working_directory="calculator", directory=".")
        self.assertIsInstance(result, str)
        self.assertIn("file_size", result)
        self.assertIn("is_dir", result)
        print(result)

        result = get_files_info(working_directory="calculator", directory="pkg")
        self.assertIsInstance(result, str)
        self.assertIn("file_size", result)
        self.assertIn("is_dir", result)
        print(result)

        result = get_files_info(working_directory=".", directory="../")
        self.assertEqual(result, 'Error: Cannot list "../" as it is outside the permitted working directory')
        print(result)
        
        result = get_files_info(working_directory=".", directory="/etc")
        self.assertEqual(result, 'Error: Cannot list "/etc" as it is outside the permitted working directory')
        print(result)

if __name__ == "__main__":
    unittest.main()