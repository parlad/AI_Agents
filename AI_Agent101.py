import openai
from openai import OpenAI
import time
import os

# Goal configuration
MainObjective = "Become a machine learning expert."  # Overall objective
InitialTask = "Learn about tensors."  # First task to research

# API Key
OPENAI_API_KEY = "dud"  # Replace with your actual API key
openai.api_key = OPENAI_API_KEY

# Initialize the OpenAI client with your API key
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# Model configuration
OPENAI_API_MODEL = "gpt-4"  # Use "gpt-4" or "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7
OPENAI_MAX_TOKENS = 1024

# Print the objective
print("*****OBJECTIVE*****")
print(f"{MainObjective}")

# Dump task array to string
def dumpTask(task):
    d = ""  # Init
    for tasklet in task:
        d += f"\n{tasklet.get('task_name', '')}"
    return d.strip()

# OpenAI inference with error handling and backoff
def OpenAiInference(
    prompt: str,
    model: str = OPENAI_API_MODEL,
    temperature: float = OPENAI_TEMPERATURE,
    max_tokens: int = 1024,
):
    while True:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_message = str(e).lower()
            if "rate limit" in error_message:
                print("Rate limit exceeded. Waiting 10 seconds and retrying...")
                time.sleep(10)
            elif "timeout" in error_message:
                print("Timeout occurred. Waiting 10 seconds and retrying...")
                time.sleep(10)
            elif "api connection" in error_message:
                print("Connection error. Check your network and retrying in 10 seconds...")
                time.sleep(10)
            elif "invalid request" in error_message:
                print(f"Invalid request: {e}. Ensure input parameters are valid.")
                raise
            else:
                print(f"Unexpected error: {e}")
                raise

# Expound on a task based on the main objective
def ExpoundTask(MainObjective: str, CurrentTask: str):
    print(f"****Expounding based on task:**** {CurrentTask}")
    prompt = (
        f"You are an AI assistant designed to complete tasks. Your main objective is: {MainObjective}.\n"
        f"Here is your current task: {CurrentTask}\n"
        f"Respond with actionable insights or steps:"
    )
    response = OpenAiInference(prompt, OPENAI_API_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS)
    new_tasks = response.split("\n") if "\n" in response else [response]
    return [{"task_name": task_name.strip()} for task_name in new_tasks if task_name.strip()]

# Generate new tasks based on the main objective and task expansion
def GenerateTasks(MainObjective: str, TaskExpansion: str):
    prompt = (
        f"You are an AI assistant tasked with generating sub-tasks. The main objective is: {MainObjective}.\n"
        f"Based on the research or findings here: {TaskExpansion}, create a detailed list of follow-up tasks.\n"
        f"Respond with a numbered list of tasks:"
    )
    response = OpenAiInference(prompt, OPENAI_API_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS)
    task_list = [task.strip() for task in response.split("\n") if task.strip()]
    return [{"task_name": task.split(". ", 1)[-1]} for task in task_list if ". " in task]

# Initial task expansion and task generation
q = ExpoundTask(MainObjective, InitialTask)
ExpoundedInitialTask = dumpTask(q)

q = GenerateTasks(MainObjective, ExpoundedInitialTask)

TaskCounter = 0
for Task in q:
    TaskCounter += 1
    print(f"#### ({TaskCounter}) Generated Task ####")
    e = ExpoundTask(MainObjective, Task["task_name"])
    print(dumpTask(e))
