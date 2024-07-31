import os
from flask import Flask, request, jsonify, render_template
import cohere
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Set up Cohere API key
co = cohere.Client(os.getenv("COHERE_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bot', methods=['POST'])
def bot():
    user_input = request.json.get('message')
    response = get_cohere_response(user_input)
    return jsonify({"response": response})

def get_cohere_response(message):
    try:
        response = co.generate(
            model='command-r-plus',  # You can specify other models if needed
            prompt=message,
            max_tokens=150
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
