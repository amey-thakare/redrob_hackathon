with open("job_description.md","r") as f:
    jd = f.read()

with open("prompts/job_parser_prompt.txt") as f:
    prompt = f.read()

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input=f"{prompt}\n\nJob Description:\n{jd}"
)


import json

result = json.loads(response.output_text)


with open("outputs/job_profile.json","w") as f:
    json.dump(result,f,indent=4)


print(result)