import os

def get_file_content(working_directory, file_path):

    try:
        abs_wrk_dir = os.path.abspath(working_directory)

        full_path = os.path.join(working_directory, file_path)

        abs_dir = os.path.abspath(full_path)

        if not abs_dir.startswith(abs_wrk_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000

        with open(abs_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string

    except Exception as e:
        return f"Error: {e}"