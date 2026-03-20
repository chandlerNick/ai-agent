import os
from google.genai import types

# All tools should return a string to allow graceful handling of errors.

def get_files_info(working_directory, directory=".") -> str:
    
    # Get target directory and validate it lies within the working directory.
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Build info string
    # - <name>: file_size=<file size in bytes> bytes, is_dir=<True/False> 
    try: 
        info = []
        for name in os.listdir(target_dir):
            path = os.path.join(target_dir, name)
            file_size = os.path.getsize(path) if os.path.isfile(path) else 0
            is_dir = os.path.isdir(path)
            info.append(f'- {name}: file_size={file_size} bytes, is_dir={is_dir}')
    except:
        return "Error: Unable to access the directory contents. Please check permissions and try again."
    
    return "\n".join(info)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)