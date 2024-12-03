import os
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],  # This is also the default; it can be omitted
)

# Define the messages separately for better readability
messages = [
    {
        "role": "system",
        "content": "determine the size of context for the user input and respond with context length with in this format: 'contect':'size'. \
        show each contect and it's size in a list. Contect lengh needs to be from openAI where Context size refers to the maximum number of tokens (which can be words, parts of words, or even punctuation marks) that the model can process in a single interaction. This includes both the input you provide and the output the model generates.",
    },
    {
        "role": "user",
        "content": "There are apple, banana and mango in the basket. John Doe lives in a small house in mountain",
    }
]

# Create a chat completion using the defined messages
chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-4o-mini",  # Ensure this model name is correct
    # max_tokens=16,
    # temperature=1.0
)

# Print the assistant's response
print(chat_completion.choices[0].message.content)
