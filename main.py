import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the file's content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file we want to read",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python script from a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the .py file we want to run",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file we want write contents into. May need creating",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents that should be written into the file"
            )
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

model_name ='gemini-2.0-flash-001'


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_dict = {
    "write_file": write_file,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "get_file_content": get_file_content
    }
    
    if not function_call_part.name in function_dict:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )

    fnct = function_dict[function_call_part.name]

    function_call_part.args["working_directory"] = "./calculator"

    function_result = fnct(**function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

verbose = False

if len(sys.argv) == 3:
    if sys.argv[2] == '--verbose':
        verbose = True

for i in range(20):

    response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    ),
    )

    for candidate in response.candidates:
        messages.append(candidate.content)


    if response.function_calls:
        function_call_part = response.function_calls[0]

        result = call_function(function_call_part, verbose)

        messages.append(result)

        continue
    
    print(response.text)
    
    break


