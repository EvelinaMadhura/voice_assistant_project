import openai

def load_api_key():
    with open('credentials/openai_api_key.txt', 'r') as file:
        return file.read().strip()

openai.api_key = load_api_key()

def generate_questions(topic):
    prompt = f"Generate five interview questions for a candidate on the topic of {topic}."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert interviewer."},
            {"role": "user", "content": prompt}
        ]
    )
    questions = response.choices[0].message['content'].strip().split('\n')
    return [q for q in questions if q]  # Filter out empty questions

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an interviewer. Ask interview questions and rate responses."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()
