import os

def write_file(working_directory, file_path, content):
    try:
        abs_wrk_dir = os.path.abspath(working_directory)

        full_path = os.path.join(working_directory, file_path)

        abs_dir = os.path.abspath(full_path)

        if not abs_dir.startswith(abs_wrk_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        with open(abs_dir, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}"