import google.generativeai as genai

# Option 2: Directly in code
genai.configure(api_key="AIzaSyCzUyAUbYUnpP_apr2FDXvqbklz74CT5n0")
# Create the model instance
model = genai.GenerativeModel("gemini-2.5-flash")

# Generate text
response = model.generate_content("Explain quantum computing in simple terms")

# Print the response
print(response.text)
