from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6Js-Z00zVMEl7acJBnhBwJLOOVmH08bn18gYs6HEl7jQA"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text)