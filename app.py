from flask import Flask, request, jsonify, send_from_directory
import random
import os
from collections import Counter
import re
import statistics
import math
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

app = Flask(__name__)

class SimpleMarkovModel:
    def __init__(self):
        self.model = {}

    def train(self, text):
        words = text.lower().split()
        for i in range(len(words) - 1):
            if words[i] not in self.model:
                self.model[words[i]] = {}
            if words[i + 1] not in self.model[words[i]]:
                self.model[words[i]][words[i + 1]] = 0
            self.model[words[i]][words[i + 1]] += 1

    def generate(self, start_word, length=20):
        if start_word not in self.model:
            return "I don't know how to respond to that."
        
        result = [start_word]
        for _ in range(length - 1):
            if result[-1] not in self.model:
                break
            next_word_options = list(self.model[result[-1]].keys())
            next_word_weights = list(self.model[result[-1]].values())
            next_word = random.choices(next_word_options, weights=next_word_weights)[0]
            result.append(next_word)
        
        return ' '.join(result)

# Initialize and train the model
model = SimpleMarkovModel()
model.train("""
Sadhak Calculator is a versatile tool for mathematical and statistical calculations.
It can perform basic arithmetic operations like addition, subtraction, multiplication, and division.
The calculator also handles more complex tasks such as calculating mean, median, and mode.
For statistical analysis, users can input data into a table to compute various measures.
Sadhak Calculator aims to be user-friendly and efficient for both simple and advanced calculations.
""")

def extract_numbers(text):
    return [float(match) for match in re.findall(r'-?\d+(?:\.\d+)?', text)]

def is_greeting(text):
    greeting_words = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    return any(word in text.lower() for word in greeting_words)

def is_compliment(text):
    compliment_words = ['thanks', 'thank you', 'appreciate', 'grateful', 'good job', 'well done', 'awesome']
    return any(word in text.lower() for word in compliment_words)

def interpret_query(prompt):
    prompt = prompt.lower()
    if 'median' in prompt:
        return 'median'
    elif any(word in prompt for word in ['mode', 'most', 'common', 'frequent']):
        return 'mode'
    elif any(word in prompt for word in ['mean', 'average']):
        return 'mean'
    elif any(word in prompt for word in ['sum', 'total', 'add']):
        return 'sum'
    elif any(word in prompt for word in ['subtract', 'difference']):
        return 'subtract'
    elif any(word in prompt for word in ['multiply', 'product']):
        return 'multiply'
    elif any(word in prompt for word in ['divide', 'quotient']):
        return 'divide'
    elif any(word in prompt for word in ['calculate', 'evaluate', 'simplify', 'expression']):
        return 'expression'
    else:
        return 'unknown'

def evaluate_expression(expression):
    try:
        expression = expression.strip().rstrip(',').replace('^', '**')
        expression = re.sub(r'\s+', '', expression)
        
        if re.search(r'[a-zA-Z]', expression):
            x, y, z = sympy.symbols('x y z')
            transformations = (standard_transformations + (implicit_multiplication_application,))
            expr = parse_expr(expression, transformations=transformations)
            result = sympy.simplify(expr)
            return str(result)
        else:
            return str(eval(expression))
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

def generate_response(prompt, max_length=20):
    print(f"Received prompt: {prompt}")  # Debug print

    if is_greeting(prompt):
        return "Hello! I'm Sadhak Calculator, your AI math assistant. How can I help you with calculations today?"
    
    if is_compliment(prompt):
        return "Thank you! I'm glad I could help. Math can be challenging, but it's also fascinating. Is there anything else you'd like to explore?"
    
    numbers = extract_numbers(prompt)
    query_type = interpret_query(prompt)

    try:
        if query_type == 'mean':
            if not numbers:
                return "I'd be happy to help you calculate the mean, but I couldn't find any numbers in your query. Could you please provide some numerical data? For example, you could ask 'What's the mean of 5, 7, 10, 12, and 15?'"
            
            sum_numbers = sum(numbers)
            count = len(numbers)
            mean = sum_numbers / count
            
            response = "Calculating the Mean\n\n"
            response += "Initial Explanation\n"
            response += "To calculate the mean (or average) of a set of numbers, you need to find the central value that represents the dataset. This involves adding up all the numbers and then dividing by the total number of values. The mean provides a measure of central tendency and is useful for understanding the overall distribution of the data.\n\n"
            response += "Mathematical Solution\n"
            response += "Sum the Numbers:\n\n"
            response += "Start by adding all the numbers together:\n\n"
            response += f"{' + '.join(map(str, numbers))} = {sum_numbers}\n\n"
            response += "Count the Numbers:\n\n"
            response += "Determine how many numbers are in the dataset:\n\n"
            response += f"n = {count}\n\n"
            response += "Calculate the Mean:\n\n"
            response += "Divide the sum by the count of numbers:\n\n"
            response += f"Mean = Sum / Count = {sum_numbers} / {count} = {mean:.1f}\n\n"
            response += "Concept Summary\n"
            response += "The mean is a measure of central tendency that gives you an average value from a set of numbers. By summing all values and dividing by the number of values, you obtain a single number that represents the center of the dataset. It's a fundamental concept in statistics used to understand the overall distribution and central value of numerical data."
            
            return response

        elif query_type == 'mode':
            if not numbers:
                return "I'd be happy to help you find the mode, but I couldn't find any numbers in your query. Could you please provide some numerical data? For example, you could ask 'What's the mode of 1, 2, 2, 3, 3, 3, 4?'"
            
            counts = Counter(numbers)
            max_count = max(counts.values())
            modes = [k for k, v in counts.items() if v == max_count]
            
            response = "Finding the Mode\n\n"
            response += "Initial Explanation\n"
            response += "The mode is the value (or values) that appear most frequently in a dataset. It's particularly useful for understanding the most common or typical value, especially in datasets with discrete values.\n\n"
            response += "Mathematical Solution\n"
            response += "Count the Occurrences:\n\n"
            for num, count in counts.items():
                response += f"{num} appears {count} time{'s' if count > 1 else ''}\n"
            response += f"\nIdentify the Highest Frequency: {max_count}\n\n"
            response += "Determine the Mode(s):\n\n"
            if len(modes) == 1:
                response += f"The mode is {modes[0]}, appearing {max_count} time{'s' if max_count > 1 else ''}.\n\n"
            else:
                response += f"There are multiple modes: {', '.join(map(str, modes))}, each appearing {max_count} times.\n\n"
            response += "Concept Summary\n"
            response += "The mode is particularly useful when you want to find the most common value in a dataset. It's the only measure of central tendency that can be used with nominal data (categories) as well as numerical data. In some cases, a dataset may have no mode, one mode, or multiple modes, providing insights into the distribution and frequency of values in the data."
            
            return response

        elif query_type == 'median':
            if not numbers:
                return "I'd be happy to help you find the median, but I couldn't find any numbers in your query. Could you please provide some numerical data? For example, you could ask 'What's the median of 10, 15, 20, 25, and 30?'"
            
            sorted_nums = sorted(numbers)
            n = len(sorted_nums)
            median = statistics.median(numbers)
            
            response = "Finding the Median\n\n"
            response += "Initial Explanation\n"
            response += "The median is the middle value in a sorted dataset. It's a robust measure of central tendency, less affected by extreme values or outliers compared to the mean.\n\n"
            response += "Mathematical Solution\n"
            response += "Sort the Numbers:\n\n"
            response += f"First, we arrange the numbers in ascending order: {', '.join(map(str, sorted_nums))}\n\n"
            response += "Find the Middle Value:\n\n"
            if n % 2 == 0:
                response += f"Since we have an even number of values ({n}), we take the average of the two middle numbers.\n"
                response += f"The two middle numbers are {sorted_nums[n//2-1]} and {sorted_nums[n//2]}.\n"
                response += f"Median = ({sorted_nums[n//2-1]} + {sorted_nums[n//2]}) / 2 = {median}\n\n"
            else:
                response += f"Since we have an odd number of values ({n}), we take the middle number.\n"
                response += f"The middle number is {median}.\n\n"
            response += "Concept Summary\n"
            response += "The median is particularly useful when dealing with skewed distributions or when you want to find the 'middle' value in a dataset. It's less sensitive to extreme values compared to the mean, making it a good choice for datasets with outliers."
            
            return response

        elif query_type == 'expression':
            expression_match = re.search(r'(calculate|evaluate|simplify)\s*(.*)', prompt, re.IGNORECASE)
            expression = expression_match.group(2) if expression_match else prompt
            
            result = evaluate_expression(expression)
            
            if 'Error' in result:
                return f"I apologize, but I encountered an error while evaluating the expression: {result}\n\nCould you please check the expression and try again? Make sure all operations are clearly stated and parentheses are properly balanced. If you're not sure how to format the expression, feel free to ask for examples."
            
            response = "Evaluating the Expression\n\n"
            response += "Initial Explanation\n"
            response += f"We'll evaluate the expression: {expression}. To solve this, we'll apply mathematical rules and operations in the correct order. This may involve simplifying fractions, combining like terms, or solving for variables.\n\n"
            response += "Mathematical Solution\n"
            response += "Step-by-step Evaluation:\n\n"
            response += f"1. Start with the original expression: {expression}\n"
            response += f"2. Apply mathematical rules and simplify: {result}\n\n"
            response += "Concept Summary\n"
            response += "This process of simplification and evaluation is crucial in algebra and calculus. It allows us to reduce complex expressions to their simplest form, making it easier to understand the relationships between variables or to find specific values."
            
            return response

        elif query_type == 'sum':
            if not numbers:
                return "I'd be happy to help you calculate the sum, but I couldn't find any numbers in your query. Could you please provide some numerical data? For example, you could ask 'What's the sum of 5, 10, 15, 20, and 25?'"
            
            total = sum(numbers)
            
            response = "Calculating the Sum\n\n"
            response += "Initial Explanation\n"
            response += "The sum is the total obtained by adding all the numbers together. It's a fundamental operation in mathematics used in various calculations and analyses.\n\n"
            response += "Mathematical Solution\n"
            response += "Add All Numbers:\n\n"
            response += f"{' + '.join(map(str, numbers))} = {total}\n\n"
            response += "Concept Summary\n"
            response += "The sum is useful in many contexts, such as calculating totals in financial statements, finding the total distance traveled in physics problems, or as a step in calculating averages."
            
            return response

        elif query_type == 'subtract':
            if len(numbers) < 2:
                return "I'd be happy to help you with subtraction, but I need at least two numbers to perform this operation. Could you please provide more numerical data? For example, you could ask 'What's the result of subtracting 15 and 7 from 100?'"
            
            result = numbers[0] - sum(numbers[1:])
            
            response = "Performing Subtraction\n\n"
            response += "Initial Explanation\n"
            response += "In subtraction, we start with the first number and subtract all subsequent numbers from it.\n\n"
            response += "Mathematical Solution\n"
            response += "Step-by-step Process:\n\n"
            response += f"1. Start with the first number: {numbers[0]}\n"
            response += f"2. Subtract the following numbers: {' - '.join(map(str, numbers[1:]))}\n"
            response += f"3. Perform the calculation: {numbers[0]} - ({' + '.join(map(str, numbers[1:]))}) = {result}\n\n"
            response += "Concept Summary\n"
            response += "Subtraction is a fundamental operation in mathematics, used to find the difference between values. It's essential in various real-world scenarios, from financial calculations to scientific measurements."
            
            return response

        elif query_type == 'multiply':
            if not numbers:
                return "I'd be happy to help you with multiplication, but I couldn't find any numbers in your query. Could you please provide some numerical data? For example, you could ask 'What's the product of 2, 3, 4, and 5?'"
            
            product = math.prod(numbers)
            
            response = "Performing Multiplication\n\n"
            response += "Initial Explanation\n"
            response += "Multiplication is the process of adding a number to itself a specified number of times. When multiplying multiple numbers, we find the product of all the numbers.\n\n"
            response += "Mathematical Solution\n"
            response += "Multiply All Numbers:\n\n"
            response += f"{' × '.join(map(str, numbers))} = {product}\n\n"
            response += "Concept Summary\n"
            response += "Multiplication is a fundamental operation in mathematics, often thought of as repeated addition. It's used in various fields, from calculating areas and volumes to more complex applications in physics and engineering."
            
            return response

        elif query_type == 'divide':
            if len(numbers) < 2:
                return "I'd be happy to help you with division, but I need at least two numbers to perform this operation. Could you please provide more numerical data? For example, you could ask 'What's the result of dividing 100 by 4 and then by 2?'"
            if 0 in numbers[1:]:
                return "I apologize, but I can't divide by zero. Division by zero is undefined in mathematics. Could you please provide a non-zero divisor?"
            
            result = numbers[0]
            for num in numbers[1:]:
                result /= num
            
            response = "Performing Division\n\n"
            response += "Initial Explanation\n"
            response += "In division, we start with the first number and divide it by each subsequent number in order.\n\n"
            response += "Mathematical Solution\n"
            response += "Step-by-step Process:\n\n"
            response += f"1. Start with the first number: {numbers[0]}\n"
            response += f"2. Divide by each subsequent number: ÷ {' ÷ '.join(map(str, numbers[1:]))}\n"
            response += f"3. Perform the calculation: {numbers[0]} ÷ {' ÷ '.join(map(str, numbers[1:]))} ≈ {result:.4f}\n\n"
            response += "Concept Summary\n"
            response += "Division is a fundamental operation in mathematics, used to distribute a quantity into equal parts or to find out how many times one quantity is contained within another. It's the inverse of multiplication and is crucial in various fields, from basic arithmetic to advanced scientific calculations."
            
            return response

        else:
            return "I'm not quite sure how to interpret your query. Could you please rephrase it or specify the type of calculation you want to perform? For example, you could ask about calculating the mean, median, mode, or perform basic arithmetic operations like addition, subtraction, multiplication, or division. I'm here to help with a wide range of mathematical calculations!"

    except Exception as e:
        print(f"Error in calculation: {str(e)}")
        return f"I apologize, but I encountered an error while processing your query: {str(e)}. Could you please check your input and try again? If you're not sure how to phrase your question, feel free to ask for examples of calculations I can perform."

@app.route('/')
def index():
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/styles.css')
def styles():
    try:
        return send_from_directory('.', 'styles.css')
    except Exception as e:
        print(f"Error serving styles.css: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/script.js')
def script():
    try:
        return send_from_directory('.', 'script.js')
    except Exception as e:
        print(f"Error serving script.js: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data['prompt']
        response = generate_response(prompt)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in generate route: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Sadhak Calculator server...")
    
    # Test cases
    test_prompts = [
        "Hi there!",
        "Thank you for your help!",
        "Good morning, Sadhak!",
        "You're awesome!",
        "What's the mode of these numbers: 1, 2, 3, 3, 4, 4, 5, 5, 5?",
        "Can you find the average of 10, 15, 20, 25, and 30?",
        "What's the sum of 5, 10, 15, 20, and 25?",
        "If I have 100 and subtract 20, 15, and 5, what's left?",
        "Multiply 2, 3, 4, and 5 together.",
        "Divide 100 by 2, then by 5.",
        "What's the most common fruit among: apple, banana, apple, orange, banana, apple?",
        "How many books on average did students read if one read 3, another 5, and a third read 4?",
        "A teacher recorded the number of books read by six students over the summer: Student A: 10 books Student B: 15 books Student C: 8 books Student D: 12 books Student E: 9 books Student F: 14 books What is the median number of books read by the students?",
        "Calculate 2 + 3 * 4.",
        "What is the result of (8 + 2) / 5?",
        "Evaluate 2x^2 + 3x - 5 when x=3.",
        "Simplify (x^2 + 2x + 1)/(x + 1).",
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest case {i}:")
        print("Input:", prompt)
        print("Result:", generate_response(prompt))
    
    app.run(debug=True, port=5001)