from flask import Flask, request, jsonify, render_template
import openai
from anthropic import Anthropic
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Set your API keys here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

openai.api_key = OPENAI_API_KEY
anthropic_client = Anthropic(api_key=CLAUDE_API_KEY)

def get_openai_signature_info(email_content):
    prompt ='''Extract the signature information from the following email and
    format it as JSON.The JSON should include "name","title", "company","phone",
    "email", and "address". If any information is missing, use `null`.
    Email:
    Dear John,
    Thank you for your email.
    Best regards,
    Jane Doe
    Senior Developer
    Tech Solutions Inc.
    jane.doe@techsolutions.com
    123-456-7890
    456 Tech Avenue, Suite 100, Tech City, TC 12345
    
    JSON:
    {
      "name": "Jane Doe",
      "title": "Senior Developer",
      "company": "Tech Solutions Inc.",
      "phone": "123-456-7890",
      "email": "jane.doe@techsolutions.com",
      "address": "456 Tech Avenue, Suite 100, Tech City, TC 12345"
    }'''
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=["\n\n"]
    )
    
    return response.choices[0].text.strip()

def get_claude_signature_info(email_content):
    prompt = f"Extract the signature information from the following email and format it as JSON. The JSON should include 'name', 'title', 'company', 'phone', 'email', and 'address'. If any information is missing, use `null`.\n\nEmail:\n---\n{email_content}\n---\n\nJSON:"
    
    response = anthropic_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=150,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response['messages'][0]['content'].strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_signature', methods=['POST'])
def extract_signature():
    email_content = request.form.get('email_content')
    model = request.form.get('model')
    
    if model == 'openai':
        result = get_openai_signature_info(email_content)
    elif model == 'claude':
        result = get_claude_signature_info(email_content)
        # Debugging output
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())
    else:
        return jsonify({'error': 'Invalid model specified.'}), 400
    
    return render_template('index.html', email_content=email_content, model=model, result=result)

if __name__ == '__main__':
    app.run(debug=True)

