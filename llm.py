import os
import sys
import subprocess
import json

from dotenv import load_dotenv
load_dotenv()

from openrouter import OpenRouter

client = OpenRouter(
        api_key= os.environ.get("API_KEY"),
        )

usr_input = input("Enter your prompt")

SYS_PROMPT = """
You are an AI Agent and user is accessing you from a harness.
Review their prompt and do the specified task.
also check if it is windows or linux/unix.
use bash tool for inspecting file 
"""

BASH_TOOL = {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command and return its output",
            "parameters": {
                "type": "object",
                "properties":{
                    "command": {
                        "type": "string",
                        "description":  "The shell command to run"
                        }
            },
                "required": ["command"],        
        },
    },
}


def bashtool(command):
    result = subprocess.run(command, shell = True, capture_output = True, text = True)
    return result.stdout + result.stderr

response = client.chat.send(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages = [
        {"role" : 'system', "content" : SYS_PROMPT},
        {"role" : 'user', "content" : usr_input}
        ],
    tools=[BASH_TOOL],
)


message = response.choices[0].message
output = message.content

completion_details = response.usage.completion_tokens_details
prompt_details = response.usage.prompt_tokens_details

usage = {
        "prompt_tokens" : response.usage.prompt_tokens,
        "completion_tokens" : response.usage.completion_tokens,
        "reasoning_tokens" : getattr(completion_details, "reasoning_tokens", None),
        "cached_tokens" :  getattr(prompt_details, "cached_tokens",None)
        }

print("\n Agents: ", output, "\n")

if message.tool_calls:
    tool_call = message.tool_calls[0]
    command = json.loads(tool_call.function.arguments)["command"]
    print("Tool: Bash ", command)
    print(bashtool(command), "\n")

print(usage)
