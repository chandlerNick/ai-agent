import os
from google.genai import types

MAX_CHARS = 10000  # Maximum number of characters to read from the file to prevent excessive memory usage

def get_file_content(working_directory, file_path) -> str:
    
    # Get target file and validate it lies within the working directory.
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)  # Read up to MAX_CHARS characters to prevent excessive memory usage
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content (up to 10,000 characters) of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)