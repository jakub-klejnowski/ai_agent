import os

def get_files_info(working_directory, directory=None):

    try:
        abs_wrk_dir = os.path.abspath(working_directory)

        full_path = os.path.join(working_directory, directory)

        abs_dir = os.path.abspath(full_path)

        if not abs_dir.startswith(abs_wrk_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        dir_objects = os.listdir(full_path)

        r = ""
        
        for obj in dir_objects:
            obj_path =  os.path.join(full_path, obj)
            f = f"- {obj}: file_size={os.path.getsize(obj_path)}, is_dir={os.path.isdir(obj_path)}\n"
            r += f
        
        return r


    except Exception as e:
        return f"Error: {e}"