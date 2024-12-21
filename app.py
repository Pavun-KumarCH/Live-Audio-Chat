from google import genai

client = genai.Client()

response = client.models.generate_content(
    model ="gemini-2.0-flash-exp",
    contents = "Is Gemini 2.0 Flash Exprensive"\
)

print(response.text)