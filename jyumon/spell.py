import os
from openai import OpenAI

api_key = ''

system_message = """
You are an AI that scores between 0 and 100 depending on the strength of the order.

If the user gives you an order, please score it.

However, you have to meet the criteria below.

1. The basic score starts at zero.
2. Orders related to fire add 30 points.
3. Orders related to the ball add 50 points.


If your order doesn't meet the above criteria, don't add your score arbitrarily.

Please print out the results in the format as below. No further explanation is needed. :

Score: 80
Reason: 30 points related to ball and 50 points related to ball plus 80 points.
"""


client = OpenAI(api_key=api_key)

def call_gpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=150, temperature=0.7, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return response


def get_score(spell):
    # example
    dialogue = call_gpt(spell)

    # print the total tokens used
    total_tokens = dialogue.usage.total_tokens
    print(f"Total tokens used: {total_tokens}")

    # print(dialogue.choices)
    return dialogue.choices[0].message.content


# spell = "アイシクルランス"
# print(get_score(spell))
