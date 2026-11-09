import os
import sys
from dotenv import load_dotenv
load_dotenv()

from openrouter import OpenRouter

client = OpenRouter(
        api_key= os.environ.get("API_KEY"),
        )

usr_input = input("Enter your prompt")

SYS_PROMPT = "You are an AI Agent and user is accessing you from a harness review their prompt and do the specified task"

response = client.chat.send(
    model="nvidia/nemotron-3.5-super-vl:free",
    messages = [
        {"role" : 'system', "content" : SYS_PROMPT},
        {"role" : 'user', "content" : usr_input}
        ],
    stream = False
)

output = response.choices[0].message.content

completion_details = response.usage.completion_tokens_details
prompt_details = response.usage.prompt_tokens_details

usage = {
        "prompt_tokens" : response.usage.prompt_tokens,
        "completion_tokens" : response.usage.completion_tokens,
        "reasoning_tokens" : getattr(completion_details, "reasoning_tokens", None),
        "cached_tokens" :  getattr(prompt_details, "cached_tokens",None)
        }

print("\n Agents: ", output, "\n")
print(usage)
