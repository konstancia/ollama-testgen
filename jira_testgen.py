import ollama

def generate_test_code(user_story: str, framework: str = "Java + JUnit") -> str:
    prompt = f"""
You are a senior QA engineer.

Generate unit tests using {framework} for the following user story:

\"\"\"{user_story}\"\"\"

Include:
- At least 3 test cases (valid input, invalid input, edge case)
- Use proper test structure and assert statements
- Output code only
"""
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']
