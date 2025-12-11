import os
from openai import OpenAI
from config import apikey


# Initialize OpenAI Client
client = OpenAI(api_key=apikey)

# Prepare Request
prompt = "Write an email to my boss for resignation?"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Output
reply = response.choices[0].message.content
print("\n📩 AI Response:\n")
print(reply)

# Debug: Full Response Object
# print(response)

"""
Example Response:
-----------------
ChatCompletion(
    id='chatcmpl-xxxx',
    choices=[
        Choice(
            finish_reason='stop',
            message=ChatCompletionMessage(
                content="Certainly! Here is a professional resignation email...",
                role='assistant'
            )
        )
    ],
    model='gpt-4o-mini',
    usage={...}
)
"""
