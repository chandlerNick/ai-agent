import subprocess
import os
from google.genai import types

def run_python_file(working_directory, file_path, args=None) -> str:

    # Get target file and validate it lies within the working directory.
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file.'
    
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ['python', target_file]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, cwd=working_directory, timeout=30)

        output_string = []

        if result.returncode != 0:
            output_string.append(f"Error: Process failed with return code {result.returncode}")
        elif not result.stdout.strip() and not result.stderr.strip():
            output_string.append("No output produced")
        else:
            output_string.append("Process executed successfully")
            if result.stdout.strip():
                output_string.append(f"STDOUT:\n{result.stdout.strip()}")
            if result.stderr.strip():
                output_string.append(f"STDERR:\n{result.stderr.strip()}")

        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)
