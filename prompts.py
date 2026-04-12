def zero_shot_explanation(code):
    return f"""You are a code analysis expert. 
Analyze the code and tell me what it does.

Code:
{code}

Explanation:"""



def few_shot_explanation(code):
    return f"""You are a code analysis expert.
Here are two examples of code analysis:

Example 1:
Code:
def add(a, b):
    return a + b

Explanation:
This function takes two numbers as input and returns their sum.

Example 2:
Code:
def greet(name):
    print(f"Hello, {{name}}!")

Explanation:
This function takes a name as input and prints a greeting message.

Now analyze this code:
Code:
{code}

Explanation:"""



def chain_of_thought_explanation(code):
    return f"""You are a code analysis expert.
Analyze the following code step by step.

Follow these steps:
1. Identify the programming language
2. Identify the main components (functions, classes, variables)
3. Explain what each component does
4. Summarize the overall purpose of the code

Code:
{code}

Step-by-step analysis:"""



def zero_shot_similarity(code1, code2):
    return f"""You are a code analysis expert.
Analyze the following two code snippets and determine if they perform the same functionality.

Code 1:
{code1}

Code 2:
{code2}

Do these two code snippets perform the same functionality? Answer Yes or No and explain why."""



def few_shot_similarity(code1, code2):
    return f"""You are a code analysis expert.
Here are two examples of similarity detection:

Example 1:
Code 1:
def add(a, b):
    return a + b

Code 2:
def sum_two(x, y):
    return x + y

Answer: Yes. Both functions take two numbers and return their sum. The only difference is the function and parameter names.

Example 2:
Code 1:
def multiply(a, b):
    return a * b

Code 2:
def square(x):
    return x * x

Answer: No. The first function multiplies two different numbers together. The second function multiplies a number by itself.

Now analyze these:
Code 1:
{code1}

Code 2:
{code2}

Do these two code snippets perform the same functionality? Answer Yes or No and explain why."""



def chain_of_thought_similarity(code1, code2):
    return f"""You are a code analysis expert.
Analyze the following two code snippets step by step.

Follow these steps:
1. Understand what Code 1 does
2. Understand what Code 2 does
3. Compare their inputs and outputs
4. Compare their logic and approach
5. Conclude whether they perform the same functionality

Code 1:
{code1}

Code 2:
{code2}

Step-by-step analysis:"""



def zero_shot_obfuscated(code):
    return f"""You are a code analysis expert.
Analyze the following code and explain what it does.

Code:
{code}

Explanation:"""


def few_shot_obfuscated(code):
    return f"""You are a code analysis expert.
Here are two examples of obfuscated code analysis:

Example 1:
Code:
var _0x1a2b = function(_0x3c4d, _0x5e6f) {{
    return _0x3c4d + _0x5e6f;
}};

Explanation:
Despite the obfuscated variable names, this function takes two inputs and returns their sum.

Example 2:
Code:
var _0x9f8e = function(_0x7a6b) {{
    console['log']('Hello' + _0x7a6b);
}};

Explanation:
Despite the obfuscated syntax, this function takes a name input and prints a greeting message.

Now analyze this code:
Code:
{code}

Explanation:"""



def chain_of_thought_obfuscated(code):
    return f"""You are a code analysis expert.
Analyze the following code step by step.

Follow these steps:
1. Identify any obfuscation techniques used (renamed variables, encoded strings, control flow changes)
2. Try to mentally de-obfuscate each component
3. Identify the main components (functions, classes, variables)
4. Explain what each component does
5. Summarize the overall purpose of the code

Code:
{code}

Step-by-step analysis:"""


