import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_wrk_dir = os.path.abspath(working_directory)

        full_path = os.path.join(working_directory, file_path)

        abs_dir = os.path.abspath(full_path)
    
        if not abs_dir.startswith(abs_wrk_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_dir):
            return f'Error: File "{file_path}" not found.'

        if not abs_dir.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        results = subprocess.run(
            ["python3", full_path],
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.PIPE,  # Capture stderr
            text=True,               # Return strings instead of bytes
            timeout=30               # 30 second timeout
        )       

        final = f'''STDOUT: {results.stdout}
                   STDERR: {results.stderr}'''

        if results.returncode != 0:
            final += f'\nProcess exited with code {results.returncode}'

        if not results.stdout.strip() and not results.stderr.strip():
            final += f'\nNo output produced'

        return final



    except Exception as e:
        return f"Error: executing Python file: {e}"