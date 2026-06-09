from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# 🔥 AI-like question bank (you can replace with OpenAI later)
easy_questions = [
    {
        "title": "Add Two Numbers",
        "difficulty": "Easy",
        "description": "Return sum of two numbers",
        "input": "a=2, b=3",
        "output": "5"
    },
    {
        "title": "Reverse String",
        "difficulty": "Easy",
        "description": "Reverse a string",
        "input": "hello",
        "output": "olleh"
    }
]

medium_questions = [
    {
        "title": "Two Sum",
        "difficulty": "Medium",
        "description": "Find indices of two numbers",
        "input": "[2,7,11,15], target=9",
        "output": "[0,1]"
    }
]

hard_questions = [
    {
        "title": "Longest Substring",
        "difficulty": "Hard",
        "description": "Find longest substring without repeat",
        "input": "abcabcbb",
        "output": "3"
    }
]

@app.route("/generate-test")
def generate_test():
    test = {
        "time": 30,
        "questions": random.sample(easy_questions, 1) +
                     random.sample(medium_questions, 1) +
                     random.sample(hard_questions, 1)
    }
    return jsonify(test)

if __name__ == "__main__":
    app.run(debug=True)