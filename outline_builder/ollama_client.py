from ollama import chat

llm_context = "You are a tool that extracts verse references from a text. A verse reference is a reference to a specific verse in the Bible. \
    For example 1 Cor 1:14 is a verse reference and Genesis 12:8 is also a verse reference. You are designed to return the verse references in \
    a piece of text to the user."

outline_point = "b. The current of the Divine Trinity within us as revealed in 2 Corinthians 13:14 is our spiritual pulse."
user_prompt = f"Give me the verse references in \"{outline_point}\"."

messages = [
  {
    'role': 'system',
    'content': llm_context,
  },
  {
    'role': 'user',
    'content': user_prompt,
  },
]

response = chat(
        'llama3.2',
        messages=messages
    )

print(response.message.content)