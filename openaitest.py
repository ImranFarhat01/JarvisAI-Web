import os
from openai import OpenAI
from config import apikey

client = OpenAI(api_key=apikey)

response = client.chat.completions.create(
    model = "gpt-4.1-mini",
    messages = [
        {"role": "user", "content": "Write an email to my boss for resignation?"}
    ],
    temperature = 0.7,
    max_tokens = 256,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0
)

# print(response.choices[0].message.content)

print(response)


''' ChatCompletion(
    id='chatcmpl-CkBk7Z0hBcb92F4sY82megI8kXiGv',
    choices=[Choice(finish_reason='stop', index=0,
                    logprobs=None,
                    message=ChatCompletionMessage(content="Certainly!
                     Here's a professional and polite resignation email template you can use:
                     \n\n---\n\n**Subject:** Resignation - [Your Full Name]\n\nDear [Boss’s Name],
                     \n\nI hope this message finds you well. 
                     I am writing to formally resign from my position as [Your Position] at [Company Name], 
                     effective [Last Working Day, typically two weeks from the date of the email].
                     \n\nI have appreciated the opportunity to work with you and the team, and 
                     I am grateful for the support and experiences I have gained during my time here. 
                     I will do my best to ensure a smooth transition and complete any outstanding tasks 
                     before my departure.\n\nPlease let me know how I can assist during this transition period. 
                     Thank you again for the opportunity and understanding.
                     \n\nBest regards,  \n[Your Full Name]  \n[Your Contact Information]\n\n---\n\nIf you want, 
                     I can customize it further based on your specific situation.", 
                     refusal=None, role='assistant', annotations=[], 
                     audio=None, function_call=None, tool_calls=None))], created=1765124263, model='gpt-4.1-mini-2025-04-14', object='chat.completion', 
                     service_tier='default', system_fingerprint='fp_7abc656409', usage=CompletionUsage(completion_tokens=177, prompt_tokens=16, total_tokens=193, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
'''