import os  
import json
import requests

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CodeHistory, Profile
import re

def extract_section(text, section):
    pattern = rf"\[{section}\]\s*([\s\S]*?)(?=\n\[|$)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""

    if match:
        return match.group(1).strip()

    return ""

# =========================
# LANGUAGE MAP
# =========================
LANG_MAP = {
    "python": "python",
    "javascript": "javascript",
    "js": "javascript",
    "java": "java",
    "cpp": "cpp",
    "c++": "cpp",
    "c": "c",
}


# =========================
# AI (OLLAMA)
# =========================
# def get_ollama_response(prompt):
#     try:
#         res = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "phi3",
#                 "prompt": prompt,
#                 "stream": False
#             },
#             timeout=30
#         )

#         if res.status_code == 200:
#             return res.json().get("response", "No response")

#         return "AI error"

#     except Exception as e:
#         return str(e)

def get_ollama_response(prompt):
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        
        print("=== GROQ DEBUG ===")
        print("API KEY EXISTS:", bool(api_key))
        print("API KEY START:", api_key[:10] if api_key else "NONE")
        
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=30
        )
        
        print("GROQ STATUS:", res.status_code)
        print("GROQ RESPONSE:", res.text[:200])  # pehle 200 chars
        
        data = res.json()
        
        if "choices" not in data:
            print("NO CHOICES IN RESPONSE:", data)
            return f"Groq error: {data.get('error', {}).get('message', str(data))}"
        
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        print("GROQ TIMEOUT!")
        return "Request timed out. Please try again."
    
    except requests.exceptions.ConnectionError as e:
        print("CONNECTION ERROR:", str(e))
        return "Connection failed to Groq API."
    
    except Exception as e:
        print("GROQ ERROR:", type(e).__name__, str(e))
        return f"Error: {str(e)}"

# =========================
# SIGNUP
# =========================
@api_view(['POST'])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if User.objects.filter(username=username).exists():
        return Response({"error": "User exists"})

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    Profile.objects.create(user=user)

    return Response({"message": "Signup success"})


# =========================
# LOGIN
# =========================
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    print("LOGIN DATA:", username, password)

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username
        })

    return Response({
        "error": "Invalid username or password"
    }, status=401)
# =========================
# PROFILE (GET)
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    try:
        user = request.user

        profile, created = Profile.objects.get_or_create(user=user)

        return Response({
            "username": user.username,
            "email": user.email,
            "bio": profile.bio or "",
            "role": profile.role or "",
            "avatar": profile.avatar.url if profile.avatar else None,
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
# PROFILE UPDATE
# =========================
@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):

    try:
        user = request.user

        profile, _ = Profile.objects.get_or_create(
            user=user
        )

        # USER DATA
        user.username = request.data.get(
            "username",
            user.username
        )

        user.email = request.data.get(
            "email",
            user.email
        )

        # BIO
        profile.bio = request.data.get(
            "bio",
            profile.bio
        )

        # IMAGE
        avatar = request.FILES.get(
            "avatar"
        )

        if avatar:
            profile.avatar = avatar

        # SAVE
        user.save()
        profile.save()

        # SAFE URL
        avatar_url = None

        if (
            profile.avatar and
            hasattr(profile.avatar, "url")
        ):
            avatar_url = profile.avatar.url

        return Response({
            "message": "Profile updated successfully",
            "username": user.username,
            "email": user.email,
            "bio": profile.bio,
            "avatar": avatar_url
        })

    except Exception as e:

        print(
            "UPDATE PROFILE ERROR:",
            str(e)
        )

        return Response({
            "error": str(e)
        }, status=500)
# AI CHAT
# =========================
@api_view(['POST'])
def ai_chat(request):
    message = request.data.get("message")

    prompt = f"You are a coding mentor. Explain simply:\n{message}"

    reply = get_ollama_response(prompt)

    return Response({"reply": reply})


# =========================
# ANALYZE CODE
# =========================
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json


# =========================
# 🔥 OLLAMA AI FUNCTION
# =========================
# def get_ai_response(prompt):
#     try:
#         res = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "phi3",
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {
#                     "temperature": 0,
#                     "num_predict": 300
#                 }
#             },
#             timeout=30
#         )

#         raw = res.json().get("response", "").strip()

#         # Clean markdown fences if model wraps in ```json
#         if raw.startswith("```"):
#             raw = raw.strip("`").strip()
#             if raw.startswith("json"):
#                 raw = raw[4:].strip()

#         return json.loads(raw)

#     except Exception:
#         return None
import os

def get_ai_response(prompt):
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            },
            timeout=30
        )

        raw = res.json()["choices"][0]["message"]["content"].strip()

        if raw.startswith("```"):
            raw = raw.strip("`").strip()
            if raw.startswith("json"):
                raw = raw[4:].strip()

        return json.loads(raw)

    except Exception as e:
        print("AI ERROR:", e)
        return None

# =========================
# 🔥 ANALYZE CODE API
# =========================
@api_view(['POST'])
def analyze_code(request):
    code = request.data.get("code", "")

    if not code.strip():
        return Response({"result": {
            "code_understanding": "No code provided",
            "errors": "Empty input",
            "improvements": "Write some code first",
            "fixed_code": "",
            "output": "",
            "verdict": "Incorrect"
        }})

    # ---------------- RUN CODE ----------------
    output = ""
    error = ""
    try:
        res = requests.post(
            "https://emkc.org/api/v2/piston/execute",
            json={
                "language": "python",
                "version": "*",
                "files": [{"content": code}]
            },
            timeout=15
        )
        run = res.json().get("run", {})
        output = (run.get("stdout") or "").strip()
        error = (run.get("stderr") or "").strip()

    except Exception as e:
        error = str(e)

    # ---------------- PROMPT ----------------
    prompt = f"""Return ONLY valid JSON. No explanation. No markdown. No code fences. Just pure JSON.

{{
  "code_understanding": "brief explanation of what the code does",
  "errors": "list any syntax or runtime errors, or write No errors",
  "improvements": "suggest specific improvements",
  "fixed_code": "corrected version of the code",
  "output": "expected output of the code",
  "verdict": "Correct or Incorrect"
}}

CODE:
{code}

EXECUTION OUTPUT:
{output if output else "No output"}

EXECUTION ERROR:
{error if error else "No error"}
"""

    ai = get_ai_response(prompt)

    # ---------------- FALLBACK ----------------
    if not ai or not isinstance(ai, dict):
        ai = {
            "code_understanding": "Code ran successfully" if not error else "Code failed to execute",
            "errors": error if error else "No errors",
            "improvements": "Add comments and use descriptive variable names",
            "fixed_code": code,
            "output": output if output else "(no output)",
            "verdict": "Incorrect" if error else "Correct"
        }

    # ✅ Save to history
    CodeHistory.objects.create(
        code=code,
        output=str(ai.get("output", ""))
    )

    return Response({"result": ai})






# RUN CODE
# =========================
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import tempfile
import subprocess
import json
import os


@csrf_exempt
def run_code(request):

    if request.method != "POST":
        return JsonResponse({
            "output": "Only POST method allowed"
        })

    try:

        body = json.loads(request.body)

        code = body.get("code", "")
        language = body.get("language", "python")

        suffix_map = {
            "python": ".py",
            "javascript": ".js",
        }

        suffix = suffix_map.get(language)

        if not suffix:
            return JsonResponse({
                "output": f"{language} not supported"
            })

        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            delete=False,
            mode="w",
            encoding="utf-8"
        ) as f:

            f.write(code)
            file_name = f.name

        try:

            if language == "python":

                result = subprocess.run(
                    ["python", file_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

            elif language == "javascript":

                result = subprocess.run(
                    ["node", file_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

            output = (
                result.stdout
                if result.stdout
                else result.stderr
            )

            return JsonResponse({
                "output": output
            })

        finally:

            if os.path.exists(file_name):
                os.remove(file_name)

    except Exception as e:

        return JsonResponse({
            "output": str(e)
        })
# =========================
# PRACTICE QUESTIONS (LEETCODE STYLE)
# =========================

from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

QUESTIONS = [

    # ==================== ARRAYS (10 Questions) ====================
    {"id": 1, "title": "Two Sum", "difficulty": "Easy", "topic": "Arrays",
     "description": "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.",
     "examples": [{"input": "nums = [2,7,11,15], target = 9", "output": "[0, 1]"}, {"input": "nums = [3,2,4], target = 6", "output": "[1, 2]"}],
     "constraints": ["2 <= nums.length <= 10^4", "Exactly one solution exists"],
     "starter_code": "def two_sum(nums, target):\n    # Write your solution here\n    pass\n\nprint(two_sum([2,7,11,15], 9))",
     "input": "nums=[2,7,11,15], target=9", "output": "[0, 1]"},

    {"id": 2, "title": "Maximum Subarray", "difficulty": "Easy", "topic": "Arrays",
     "description": "Given an integer array nums, find the subarray with the largest sum and return its sum. (Kadane's Algorithm)",
     "examples": [{"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6"}, {"input": "nums = [1]", "output": "1"}],
     "constraints": ["1 <= nums.length <= 10^5"],
     "starter_code": "def max_subarray(nums):\n    # Write your solution here\n    pass\n\nprint(max_subarray([-2,1,-3,4,-1,2,1,-5,4]))",
     "input": "nums=[-2,1,-3,4,-1,2,1,-5,4]", "output": "6"},

    {"id": 3, "title": "Contains Duplicate", "difficulty": "Easy", "topic": "Arrays",
     "description": "Given an integer array nums, return True if any value appears at least twice, False if every element is distinct.",
     "examples": [{"input": "nums = [1,2,3,1]", "output": "True"}, {"input": "nums = [1,2,3,4]", "output": "False"}],
     "constraints": ["1 <= nums.length <= 10^5"],
     "starter_code": "def contains_duplicate(nums):\n    # Write your solution here\n    pass\n\nprint(contains_duplicate([1,2,3,1]))",
     "input": "nums=[1,2,3,1]", "output": "True"},

    {"id": 4, "title": "Find Missing Number", "difficulty": "Easy", "topic": "Arrays",
     "description": "Given an array containing n distinct numbers in range [0, n], return the only missing number.",
     "examples": [{"input": "nums = [3,0,1]", "output": "2"}, {"input": "nums = [0,1]", "output": "2"}],
     "constraints": ["n == nums.length", "All numbers are unique"],
     "starter_code": "def missing_number(nums):\n    # Write your solution here\n    pass\n\nprint(missing_number([3,0,1]))",
     "input": "nums=[3,0,1]", "output": "2"},

    {"id": 5, "title": "Best Time to Buy and Sell Stock", "difficulty": "Easy", "topic": "Arrays",
     "description": "Given prices array where prices[i] is price on day i, return maximum profit. If no profit possible return 0.",
     "examples": [{"input": "prices = [7,1,5,3,6,4]", "output": "5"}, {"input": "prices = [7,6,4,3,1]", "output": "0"}],
     "constraints": ["1 <= prices.length <= 10^5"],
     "starter_code": "def max_profit(prices):\n    # Write your solution here\n    pass\n\nprint(max_profit([7,1,5,3,6,4]))",
     "input": "prices=[7,1,5,3,6,4]", "output": "5"},

    {"id": 6, "title": "Move Zeroes", "difficulty": "Easy", "topic": "Arrays",
     "description": "Given an integer array nums, move all 0s to the end while maintaining the relative order of non-zero elements. Do it in-place.",
     "examples": [{"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]"}, {"input": "nums = [0]", "output": "[0]"}],
     "constraints": ["1 <= nums.length <= 10^4", "In-place, no extra array"],
     "starter_code": "def move_zeroes(nums):\n    # Write your solution here\n    pass\n\nnums = [0,1,0,3,12]\nmove_zeroes(nums)\nprint(nums)",
     "input": "nums=[0,1,0,3,12]", "output": "[1,3,12,0,0]"},

    {"id": 7, "title": "Second Largest Element", "difficulty": "Easy", "topic": "Arrays",
     "description": "Given an array of integers, find the second largest element without sorting.",
     "examples": [{"input": "nums = [12,35,1,10,34,1]", "output": "34"}, {"input": "nums = [10,5,10]", "output": "5"}],
     "constraints": ["2 <= nums.length <= 10^5"],
     "starter_code": "def second_largest(nums):\n    # Write your solution here\n    pass\n\nprint(second_largest([12,35,1,10,34,1]))",
     "input": "nums=[12,35,1,10,34,1]", "output": "34"},

    {"id": 8, "title": "Rotate Array", "difficulty": "Medium", "topic": "Arrays",
     "description": "Given an integer array nums, rotate the array to the right by k steps in-place.",
     "examples": [{"input": "nums = [1,2,3,4,5,6,7], k = 3", "output": "[5,6,7,1,2,3,4]"}],
     "constraints": ["1 <= nums.length <= 10^5", "In-place with O(1) space"],
     "starter_code": "def rotate(nums, k):\n    # Write your solution here\n    pass\n\nnums = [1,2,3,4,5,6,7]\nrotate(nums, 3)\nprint(nums)",
     "input": "nums=[1,2,3,4,5,6,7], k=3", "output": "[5,6,7,1,2,3,4]"},

    {"id": 9, "title": "Product of Array Except Self", "difficulty": "Medium", "topic": "Arrays",
     "description": "Return an array where each element is the product of all other elements. O(n) without division.",
     "examples": [{"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]"}],
     "constraints": ["2 <= nums.length <= 10^5", "O(n) time, no division"],
     "starter_code": "def product_except_self(nums):\n    # Write your solution here\n    pass\n\nprint(product_except_self([1,2,3,4]))",
     "input": "nums=[1,2,3,4]", "output": "[24,12,8,6]"},

    {"id": 10, "title": "3Sum", "difficulty": "Medium", "topic": "Arrays",
     "description": "Given an integer array nums, return all unique triplets that sum to zero.",
     "examples": [{"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"}],
     "constraints": ["3 <= nums.length <= 3000", "No duplicate triplets in output"],
     "starter_code": "def three_sum(nums):\n    # Write your solution here\n    pass\n\nprint(three_sum([-1,0,1,2,-1,-4]))",
     "input": "nums=[-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"},

    # ==================== STRINGS (10 Questions) ====================
    {"id": 11, "title": "Reverse String", "difficulty": "Easy", "topic": "Strings",
     "description": "Write a function that reverses a string. Do it in-place with O(1) extra memory.",
     "examples": [{"input": "s = ['h','e','l','l','o']", "output": "['o','l','l','e','h']"}],
     "constraints": ["1 <= s.length <= 10^5", "In-place only"],
     "starter_code": "def reverse_string(s):\n    # Write your solution here\n    pass\n\ns = ['h','e','l','l','o']\nreverse_string(s)\nprint(s)",
     "input": "s=['h','e','l','l','o']", "output": "['o','l','l','e','h']"},

    {"id": 12, "title": "Valid Palindrome", "difficulty": "Easy", "topic": "Strings",
     "description": "A phrase is palindrome if after converting to lowercase and removing non-alphanumeric characters it reads same forward and backward.",
     "examples": [{"input": "s = 'A man, a plan, a canal: Panama'", "output": "True"}, {"input": "s = 'race a car'", "output": "False"}],
     "constraints": ["1 <= s.length <= 2*10^5"],
     "starter_code": "def is_palindrome(s):\n    # Write your solution here\n    pass\n\nprint(is_palindrome('A man, a plan, a canal: Panama'))",
     "input": "s='A man, a plan, a canal: Panama'", "output": "True"},

    {"id": 13, "title": "Valid Anagram", "difficulty": "Easy", "topic": "Strings",
     "description": "Given two strings s and t, return True if t is an anagram of s, False otherwise.",
     "examples": [{"input": "s = 'anagram', t = 'nagaram'", "output": "True"}, {"input": "s = 'rat', t = 'car'", "output": "False"}],
     "constraints": ["1 <= s.length, t.length <= 5*10^4"],
     "starter_code": "def is_anagram(s, t):\n    # Write your solution here\n    pass\n\nprint(is_anagram('anagram', 'nagaram'))",
     "input": "s='anagram', t='nagaram'", "output": "True"},

    {"id": 14, "title": "Count Vowels", "difficulty": "Easy", "topic": "Strings",
     "description": "Given a string s, return the total number of vowels (a, e, i, o, u) — both uppercase and lowercase.",
     "examples": [{"input": "s = 'Hello World'", "output": "3"}, {"input": "s = 'rhythm'", "output": "0"}],
     "constraints": ["1 <= s.length <= 10^5"],
     "starter_code": "def count_vowels(s):\n    # Write your solution here\n    pass\n\nprint(count_vowels('Hello World'))",
     "input": "s='Hello World'", "output": "3"},

    {"id": 15, "title": "First Non-Repeating Character", "difficulty": "Easy", "topic": "Strings",
     "description": "Given a string s, find the first non-repeating character and return its index. Return -1 if none exists.",
     "examples": [{"input": "s = 'leetcode'", "output": "0"}, {"input": "s = 'aabb'", "output": "-1"}],
     "constraints": ["1 <= s.length <= 10^5"],
     "starter_code": "def first_uniq_char(s):\n    # Write your solution here\n    pass\n\nprint(first_uniq_char('leetcode'))",
     "input": "s='leetcode'", "output": "0"},

    {"id": 16, "title": "Reverse Words in a String", "difficulty": "Easy", "topic": "Strings",
     "description": "Given a string s, reverse the order of the words. Words are separated by spaces.",
     "examples": [{"input": "s = 'the sky is blue'", "output": "'blue is sky the'"}, {"input": "s = '  hello world  '", "output": "'world hello'"}],
     "constraints": ["1 <= s.length <= 10^4", "Handle extra spaces"],
     "starter_code": "def reverse_words(s):\n    # Write your solution here\n    pass\n\nprint(reverse_words('the sky is blue'))",
     "input": "s='the sky is blue'", "output": "'blue is sky the'"},

    {"id": 17, "title": "Check Pangram", "difficulty": "Easy", "topic": "Strings",
     "description": "A pangram is a sentence where every letter of the alphabet appears at least once. Return True if the string is a pangram.",
     "examples": [{"input": "s = 'thequickbrownfoxjumpsoverthelazydog'", "output": "True"}, {"input": "s = 'hello'", "output": "False"}],
     "constraints": ["1 <= s.length <= 1000"],
     "starter_code": "def is_pangram(s):\n    # Write your solution here\n    pass\n\nprint(is_pangram('thequickbrownfoxjumpsoverthelazydog'))",
     "input": "s='thequickbrownfoxjumpsoverthelazydog'", "output": "True"},

    {"id": 18, "title": "Longest Common Prefix", "difficulty": "Easy", "topic": "Strings",
     "description": "Write a function to find the longest common prefix string amongst an array of strings. Return empty string if none.",
     "examples": [{"input": "strs = ['flower','flow','flight']", "output": "'fl'"}, {"input": "strs = ['dog','racecar','car']", "output": "''"}],
     "constraints": ["1 <= strs.length <= 200"],
     "starter_code": "def longest_common_prefix(strs):\n    # Write your solution here\n    pass\n\nprint(longest_common_prefix(['flower','flow','flight']))",
     "input": "strs=['flower','flow','flight']", "output": "'fl'"},

    {"id": 19, "title": "Group Anagrams", "difficulty": "Medium", "topic": "Strings",
     "description": "Given an array of strings, group the anagrams together and return them.",
     "examples": [{"input": "strs = ['eat','tea','tan','ate','nat','bat']", "output": "[['eat','tea','ate'],['tan','nat'],['bat']]"}],
     "constraints": ["1 <= strs.length <= 10^4"],
     "starter_code": "def group_anagrams(strs):\n    # Write your solution here\n    pass\n\nprint(group_anagrams(['eat','tea','tan','ate','nat','bat']))",
     "input": "strs=['eat','tea','tan','ate','nat','bat']", "output": "[['eat','tea','ate'],['tan','nat'],['bat']]"},

    {"id": 20, "title": "Longest Substring Without Repeating", "difficulty": "Medium", "topic": "Strings",
     "description": "Given a string s, find the length of the longest substring without repeating characters.",
     "examples": [{"input": "s = 'abcabcbb'", "output": "3"}, {"input": "s = 'bbbbb'", "output": "1"}],
     "constraints": ["0 <= s.length <= 5*10^4"],
     "starter_code": "def length_of_longest_substring(s):\n    # Write your solution here\n    pass\n\nprint(length_of_longest_substring('abcabcbb'))",
     "input": "s='abcabcbb'", "output": "3"},

    # ==================== DICTIONARY / HASHMAP (8 Questions) ====================
    {"id": 21, "title": "Two Sum using HashMap", "difficulty": "Easy", "topic": "Dictionary",
     "description": "Solve Two Sum using a dictionary for O(n) time complexity. Return indices of two numbers that add to target.",
     "examples": [{"input": "nums = [2,7,11,15], target = 9", "output": "[0, 1]"}],
     "constraints": ["Must use dictionary", "O(n) time complexity"],
     "starter_code": "def two_sum(nums, target):\n    seen = {}\n    # Write your solution here\n    pass\n\nprint(two_sum([2,7,11,15], 9))",
     "input": "nums=[2,7,11,15], target=9", "output": "[0, 1]"},

    {"id": 22, "title": "Word Frequency Count", "difficulty": "Easy", "topic": "Dictionary",
     "description": "Given a string of words, return a dictionary with the frequency of each word.",
     "examples": [{"input": "s = 'apple banana apple orange banana apple'", "output": "{'apple':3,'banana':2,'orange':1}"}],
     "constraints": ["Words are lowercase", "1 <= words <= 10^4"],
     "starter_code": "def word_frequency(s):\n    # Write your solution here\n    pass\n\nprint(word_frequency('apple banana apple orange banana apple'))",
     "input": "s='apple banana apple orange banana apple'", "output": "{'apple':3,'banana':2,'orange':1}"},

    {"id": 23, "title": "Find Duplicates", "difficulty": "Easy", "topic": "Dictionary",
     "description": "Given an integer array nums, return all elements that appear more than once.",
     "examples": [{"input": "nums = [4,3,2,7,8,2,3,1]", "output": "[2,3]"}],
     "constraints": ["1 <= nums.length <= 10^4", "Use a dictionary"],
     "starter_code": "def find_duplicates(nums):\n    # Write your solution here\n    pass\n\nprint(find_duplicates([4,3,2,7,8,2,3,1]))",
     "input": "nums=[4,3,2,7,8,2,3,1]", "output": "[2,3]"},

    {"id": 24, "title": "Intersection of Two Arrays", "difficulty": "Easy", "topic": "Dictionary",
     "description": "Given two integer arrays nums1 and nums2, return their intersection (common elements, no duplicates).",
     "examples": [{"input": "nums1 = [1,2,2,1], nums2 = [2,2]", "output": "[2]"}, {"input": "nums1 = [4,9,5], nums2 = [9,4,9,8,4]", "output": "[9,4]"}],
     "constraints": ["Use a set or dictionary"],
     "starter_code": "def intersection(nums1, nums2):\n    # Write your solution here\n    pass\n\nprint(intersection([1,2,2,1],[2,2]))",
     "input": "nums1=[1,2,2,1], nums2=[2,2]", "output": "[2]"},

    {"id": 25, "title": "Majority Element", "difficulty": "Easy", "topic": "Dictionary",
     "description": "Given array nums of size n, return the majority element (appears more than n/2 times). It always exists.",
     "examples": [{"input": "nums = [3,2,3]", "output": "3"}, {"input": "nums = [2,2,1,1,1,2,2]", "output": "2"}],
     "constraints": ["Majority element always exists"],
     "starter_code": "def majority_element(nums):\n    # Write your solution here\n    pass\n\nprint(majority_element([2,2,1,1,1,2,2]))",
     "input": "nums=[2,2,1,1,1,2,2]", "output": "2"},

    {"id": 26, "title": "Subarray Sum Equals K", "difficulty": "Medium", "topic": "Dictionary",
     "description": "Given an integer array nums and integer k, return the total number of subarrays whose sum equals k.",
     "examples": [{"input": "nums = [1,1,1], k = 2", "output": "2"}, {"input": "nums = [1,2,3], k = 3", "output": "2"}],
     "constraints": ["Use prefix sum with hashmap", "O(n) solution"],
     "starter_code": "def subarray_sum(nums, k):\n    # Write your solution here\n    pass\n\nprint(subarray_sum([1,1,1], 2))",
     "input": "nums=[1,1,1], k=2", "output": "2"},

    {"id": 27, "title": "Top K Frequent Elements", "difficulty": "Medium", "topic": "Dictionary",
     "description": "Given an integer array nums and integer k, return the k most frequent elements.",
     "examples": [{"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]"}],
     "constraints": ["Use a dictionary + sorting or heap"],
     "starter_code": "def top_k_frequent(nums, k):\n    # Write your solution here\n    pass\n\nprint(top_k_frequent([1,1,1,2,2,3], 2))",
     "input": "nums=[1,1,1,2,2,3], k=2", "output": "[1,2]"},

    {"id": 28, "title": "Longest Consecutive Sequence", "difficulty": "Medium", "topic": "Dictionary",
     "description": "Given unsorted array, return length of longest consecutive elements sequence in O(n).",
     "examples": [{"input": "nums = [100,4,200,1,3,2]", "output": "4"}, {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9"}],
     "constraints": ["Must be O(n) using a set/dictionary"],
     "starter_code": "def longest_consecutive(nums):\n    # Write your solution here\n    pass\n\nprint(longest_consecutive([100,4,200,1,3,2]))",
     "input": "nums=[100,4,200,1,3,2]", "output": "4"},

    # ==================== STACK (6 Questions) ====================
    {"id": 29, "title": "Valid Parentheses", "difficulty": "Easy", "topic": "Stack",
     "description": "Given a string containing '(', ')', '{', '}', '[', ']', determine if the input string is valid using a stack.",
     "examples": [{"input": "s = '()[]{}'", "output": "True"}, {"input": "s = '(]'", "output": "False"}],
     "constraints": ["1 <= s.length <= 10^4", "Must use a stack"],
     "starter_code": "def is_valid(s):\n    # Write your solution here\n    stack = []\n    pass\n\nprint(is_valid('()[]{}'))",
     "input": "s='()[]{}'", "output": "True"},

    {"id": 30, "title": "Implement Stack using Queue", "difficulty": "Easy", "topic": "Stack",
     "description": "Implement a last-in-first-out stack using only Python lists (as queues). Implement push, pop, top, and empty.",
     "examples": [{"input": "push(1), push(2), top(), pop(), empty()", "output": "2, 2, False"}],
     "constraints": ["Only use list append and pop(0) operations"],
     "starter_code": "class MyStack:\n    def __init__(self):\n        self.queue = []\n\n    def push(self, x):\n        pass\n\n    def pop(self):\n        pass\n\n    def top(self):\n        pass\n\n    def empty(self):\n        pass",
     "input": "push(1),push(2),top(),pop(),empty()", "output": "2, 2, False"},

    {"id": 31, "title": "Daily Temperatures", "difficulty": "Medium", "topic": "Stack",
     "description": "Given temperatures array, return array where answer[i] is number of days until a warmer temperature. Use monotonic stack.",
     "examples": [{"input": "temperatures = [73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]"}],
     "constraints": ["Use monotonic stack for O(n)"],
     "starter_code": "def daily_temperatures(temperatures):\n    # Write your solution here\n    stack = []\n    pass\n\nprint(daily_temperatures([73,74,75,71,69,72,76,73]))",
     "input": "temperatures=[73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]"},

    {"id": 32, "title": "Min Stack", "difficulty": "Medium", "topic": "Stack",
     "description": "Design a stack that supports push, pop, top and retrieving the minimum element in O(1) time.",
     "examples": [{"input": "push(-2),push(0),push(-3),getMin(),pop(),top(),getMin()", "output": "-3, 0, -2"}],
     "constraints": ["All operations must be O(1)"],
     "starter_code": "class MinStack:\n    def __init__(self):\n        self.stack = []\n        self.min_stack = []\n\n    def push(self, val):\n        pass\n\n    def pop(self):\n        pass\n\n    def top(self):\n        pass\n\n    def getMin(self):\n        pass",
     "input": "operations as above", "output": "-3, 0, -2"},

    {"id": 33, "title": "Next Greater Element", "difficulty": "Medium", "topic": "Stack",
     "description": "Given array nums, return array where answer[i] is the next greater element for nums[i]. Return -1 if none exists.",
     "examples": [{"input": "nums = [2,1,2,4,3]", "output": "[4,2,4,-1,-1]"}],
     "constraints": ["Use monotonic stack", "O(n) time"],
     "starter_code": "def next_greater_element(nums):\n    # Write your solution here\n    stack = []\n    pass\n\nprint(next_greater_element([2,1,2,4,3]))",
     "input": "nums=[2,1,2,4,3]", "output": "[4,2,4,-1,-1]"},

    {"id": 34, "title": "Evaluate Reverse Polish Notation", "difficulty": "Medium", "topic": "Stack",
     "description": "Evaluate the value of an arithmetic expression in Reverse Polish Notation (postfix). Valid operators are +, -, *, /.",
     "examples": [{"input": "tokens = ['2','1','+','3','*']", "output": "9"}, {"input": "tokens = ['4','13','5','/'+']", "output": "6"}],
     "constraints": ["Use a stack", "Division truncates toward zero"],
     "starter_code": "def eval_rpn(tokens):\n    # Write your solution here\n    stack = []\n    pass\n\nprint(eval_rpn(['2','1','+','3','*']))",
     "input": "tokens=['2','1','+','3','*']", "output": "9"},

    # ==================== LINKED LIST (6 Questions) ====================
    {"id": 35, "title": "Reverse Linked List", "difficulty": "Easy", "topic": "Linked List",
     "description": "Given the head of a singly linked list, reverse the list and return the new head.",
     "examples": [{"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"}],
     "constraints": ["0 <= Number of nodes <= 5000", "Iterative or recursive both fine"],
     "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverse_list(head):\n    prev = None\n    # Write your solution here\n    pass",
     "input": "head=[1,2,3,4,5]", "output": "[5,4,3,2,1]"},

    {"id": 36, "title": "Merge Two Sorted Lists", "difficulty": "Easy", "topic": "Linked List",
     "description": "Merge two sorted linked lists and return the head of the merged sorted list.",
     "examples": [{"input": "l1 = [1,2,4], l2 = [1,3,4]", "output": "[1,1,2,3,4,4]"}],
     "constraints": ["0 <= Number of nodes <= 50", "Both lists are sorted in non-decreasing order"],
     "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef merge_two_lists(l1, l2):\n    # Write your solution here\n    pass",
     "input": "l1=[1,2,4], l2=[1,3,4]", "output": "[1,1,2,3,4,4]"},

    {"id": 37, "title": "Detect Cycle in Linked List", "difficulty": "Easy", "topic": "Linked List",
     "description": "Given head of a linked list, determine if it has a cycle. Use Floyd's tortoise and hare algorithm.",
     "examples": [{"input": "head = [3,2,0,-4], pos = 1", "output": "True"}, {"input": "head = [1,2], pos = -1", "output": "False"}],
     "constraints": ["Use O(1) memory only", "Floyd's algorithm required"],
     "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef has_cycle(head):\n    slow = head\n    fast = head\n    # Write your solution here\n    pass",
     "input": "head=[3,2,0,-4], pos=1", "output": "True"},

    {"id": 38, "title": "Find Middle of Linked List", "difficulty": "Easy", "topic": "Linked List",
     "description": "Given head of a singly linked list, return the middle node. If two middles exist, return the second one.",
     "examples": [{"input": "head = [1,2,3,4,5]", "output": "Node 3"}, {"input": "head = [1,2,3,4,5,6]", "output": "Node 4"}],
     "constraints": ["Use slow and fast pointer (one pass only)"],
     "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef middle_node(head):\n    slow = head\n    fast = head\n    # Write your solution here\n    pass",
     "input": "head=[1,2,3,4,5]", "output": "3"},

    {"id": 39, "title": "Remove Nth Node From End", "difficulty": "Medium", "topic": "Linked List",
     "description": "Given linked list head and integer n, remove the nth node from the end of list and return head.",
     "examples": [{"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]"}],
     "constraints": ["Use two pointer technique", "One pass only"],
     "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef remove_nth_from_end(head, n):\n    # Write your solution here\n    pass",
     "input": "head=[1,2,3,4,5], n=2", "output": "[1,2,3,5]"},

    {"id": 40, "title": "Palindrome Linked List", "difficulty": "Medium", "topic": "Linked List",
     "description": "Given head of a linked list, return True if it is a palindrome, False otherwise. Use O(n) time and O(1) space.",
     "examples": [{"input": "head = [1,2,2,1]", "output": "True"}, {"input": "head = [1,2]", "output": "False"}],
     "constraints": ["O(1) extra space", "Hint: find middle, reverse second half, compare"],
     "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef is_palindrome(head):\n    # Write your solution here\n    pass",
     "input": "head=[1,2,2,1]", "output": "True"},
]


@api_view(['GET'])
def practice_question(request):
    difficulty = request.GET.get("difficulty", None)
    topic = request.GET.get("topic", None)

    filtered = QUESTIONS

    if difficulty:
        filtered = [q for q in filtered if q["difficulty"].lower() == difficulty.lower()]
    if topic:
        filtered = [q for q in filtered if q["topic"].lower() == topic.lower()]

    return Response({"questions": filtered})


@api_view(['GET'])
def generate_test(request):
    easy = random.sample([q for q in QUESTIONS if q["difficulty"] == "Easy"], 3)
    medium = random.sample([q for q in QUESTIONS if q["difficulty"] == "Medium"], 2)

    return Response({
        "time": 60,
        "questions": easy + medium
    })
    


# =========================
# GENERATE TEST (SAFE VERSION)
# =========================
@api_view(['GET'])
def generate_test(request):
    return Response({
        "time": 60,
        "questions": [
            {
                "title": "Two Sum",
                "difficulty": "Easy",
                "input": "nums=[2,7], target=9",
                "output": "[0,1]"
            },
            {
                "title": "Reverse String",
                "difficulty": "Easy",
                "input": "hello",
                "output": "olleh"
            }
        ]
    })


# =========================
# HISTORY
# =========================
# # =========================
# HISTORY
# =========================

@api_view(['GET'])
def get_history(request):
    history = CodeHistory.objects.all().order_by("-created_at")
    return Response([
        {
            "id": h.id,           # ← add karo
            "code": h.code,
            "output": h.output,
            "language": getattr(h, 'language', 'python'),  # ← add karo
            "time": h.created_at
        }
        for h in history
    ])
@api_view(['DELETE'])
def delete_history(request, pk):
    try:
        item = CodeHistory.objects.get(pk=pk)
        item.delete()
        return Response({"message": "Deleted"})
    except CodeHistory.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(['DELETE'])
def clear_history(request):
    CodeHistory.objects.all().delete()
    return Response({"message": "All cleared"})

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get("email")

    user = User.objects.filter(email=email).first()

    if user:
        return Response({"message": "Reset link sent"})
    return Response({"error": "User not found"})
@api_view(['POST'])
def reset_password(request):
    email = request.data.get("email")
    new_password = request.data.get("password")

    if not email or not new_password:
        return Response({"error": "Missing fields"})

    user = User.objects.filter(email=email).first()

    if user:
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated"})

    return Response({"error": "User not found"})
@api_view(['POST'])
def test_mode(request):
    code = request.data.get("code")

    if not code:
        return Response({"result": "No code provided"})

    result = get_ollama_response(code)

    return Response({"result": result})
@api_view(['POST'])
def evaluate_answer(request):

    user_code = request.data.get("code")
    expected_output = request.data.get("expected_output")

    if not user_code:
        return Response({"error": "No code provided"})

    try:
        res = requests.post(
            "https://emkc.org/api/v2/piston/execute",
            json={
                "language": "python",
                "version": "*",
                "files": [{"content": user_code}]
            },
            timeout=15
        )

        output = res.json().get("run", {}).get("output", "").strip()

        correct = output.strip() == str(expected_output).strip()

        return Response({
            "output": output,
            "expected": expected_output,
            "correct": correct,
            "score": 100 if correct else 0
        })

    except Exception as e:
        return Response({"error": str(e), "score": 0})
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json


# =========================
# AI QUESTION GENERATOR
# =========================
@api_view(['GET'])
def generate_ai_question(request):

    prompt = """
You are a FAANG-level coding interviewer.

Generate ONE coding question.

Return ONLY valid JSON:

{
  "title": "string",
  "difficulty": "Easy/Medium/Hard",
  "description": "problem statement",
  "input": "example input",
  "output": "expected output",
  "hint": "short hint"
}

Rules:
- Must be DSA based
- Only JSON, no explanation
"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        raw = res.json().get("response", "")

        try:
            data = json.loads(raw)
        except:
            # 🔥 SMART FALLBACK QUESTIONS (LeetCode style)
            data = {
                "title": random.choice(["Two Sum", "Binary Search", "Reverse String"]),
                "difficulty": "Easy",
                "description": "Solve using optimal approach",
                "input": "nums=[1,2,3], target=3",
                "output": "[0,2]",
                "hint": "Use hashmap / two pointers"
            }

        return Response(data)

    except Exception as e:
        return Response({
            "error": str(e),
            "title": "Two Sum",
            "difficulty": "Easy",
            "description": "Fallback question",
            "input": "nums=[2,7], target=9",
            "output": "[0,1]",
            "hint": "Use hashmap"
        })
def update_user_stats(user, correct):
    perf, created = Performance.objects.get_or_create(user=user)

    perf.solved += 1

    if correct:
        perf.score += 10

    # accuracy calculation
    total = perf.solved
    correct_count = perf.score / 10

    perf.accuracy = (correct_count / total) * 100 if total > 0 else 0

    perf.save()
    
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
@login_required
def user_data(request):
    user = request.user
    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
    })