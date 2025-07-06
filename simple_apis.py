from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# 1. Hello World
@app.route('/')
def hello_world():
    """Return a simple Hello World message."""
    return 'Hello, World!'

# 2. Echo (repeat what user sends)
@app.route('/echo', methods=['GET'])
def echo():
    """Echo back the 'msg' query parameter."""
    msg = request.args.get('msg', '')
    return f'You said: {msg}'

# 3. Add two numbers
@app.route('/add', methods=['GET'])
def add():
    """Add two numbers from query parameters 'a' and 'b'."""
    a = request.args.get('a', type=float, default=0)
    b = request.args.get('b', type=float, default=0)
    return jsonify(result=a + b)

# 4. Subtract two numbers
@app.route('/subtract', methods=['GET'])
def subtract():
    """Subtract 'b' from 'a'."""
    a = request.args.get('a', type=float, default=0)
    b = request.args.get('b', type=float, default=0)
    return jsonify(result=a - b)

# 5. Multiply two numbers
@app.route('/multiply', methods=['GET'])
def multiply():
    """Multiply two numbers."""
    a = request.args.get('a', type=float, default=1)
    b = request.args.get('b', type=float, default=1)
    return jsonify(result=a * b)

# 6. Divide two numbers
@app.route('/divide', methods=['GET'])
def divide():
    """Divide 'a' by 'b'."""
    a = request.args.get('a', type=float, default=1)
    b = request.args.get('b', type=float, default=1)
    if b == 0:
        return jsonify(error='Division by zero!'), 400
    return jsonify(result=a / b)

# 7. Reverse a string
@app.route('/reverse', methods=['GET'])
def reverse():
    """Reverse the 'text' query parameter."""
    text = request.args.get('text', '')
    return text[::-1]

# 8. Uppercase a string
@app.route('/uppercase', methods=['GET'])
def uppercase():
    """Convert 'text' to uppercase."""
    text = request.args.get('text', '')
    return text.upper()

# 9. Lowercase a string
@app.route('/lowercase', methods=['GET'])
def lowercase():
    """Convert 'text' to lowercase."""
    text = request.args.get('text', '')
    return text.lower()

# 10. Dummy user login (no DB)
@app.route('/login', methods=['POST'])
def login():
    """Dummy login: username=admin, password=secret"""
    data = request.json
    if not data:
        return jsonify(error='No data provided'), 400
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == 'secret':
        return jsonify(message='Login successful!')
    return jsonify(error='Invalid credentials'), 401

# 11. Random quote
QUOTES = [
    "The best way to get started is to quit talking and begin doing.",
    "Don't let yesterday take up too much of today.",
    "It's not whether you get knocked down, it's whether you get up.",
    "If you are working on something exciting, it will keep you motivated."
]
@app.route('/quote', methods=['GET'])
def quote():
    """Return a random quote."""
    return random.choice(QUOTES)

# 12. Dictionary lookup
DICTIONARY = {
    'python': 'A high-level programming language.',
    'flask': 'A lightweight WSGI web application framework.',
    'api': 'Application Programming Interface.'
}
@app.route('/define', methods=['GET'])
def define():
    """Look up a word in the dictionary."""
    word = request.args.get('word', '').lower()
    meaning = DICTIONARY.get(word)
    if meaning:
        return meaning
    return 'Word not found.'

# 13. Get current time
@app.route('/time', methods=['GET'])
def get_time():
    """Return the current server time."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 14. Status check
@app.route('/status', methods=['GET'])
def status():
    """Return API status."""
    return jsonify(status='OK')

# 15. Simple counter (in-memory)
counter = {'count': 0}
@app.route('/counter', methods=['GET', 'POST'])
def simple_counter():
    """GET: return count, POST: increment count."""
    if request.method == 'POST':
        counter['count'] += 1
    return jsonify(count=counter['count'])

# 16. Greet user by name
@app.route('/greet/<name>')
def greet(name):
    """Greet the user by name."""
    return f'Hello, {name}!'

# 17. List all routes
@app.route('/routes')
def list_routes():
    """List all available routes."""
    output = []
    for rule in app.url_map.iter_rules():
        output.append(str(rule))
    return jsonify(routes=output)

# 18. Check if number is even or odd
@app.route('/evenodd/<int:num>')
def even_odd(num):
    """Check if a number is even or odd."""
    return 'Even' if num % 2 == 0 else 'Odd'

# 19. Square a number
@app.route('/square/<int:num>')
def square(num):
    """Return the square of a number."""
    return jsonify(result=num * num)

# 20. Cube a number
@app.route('/cube/<int:num>')
def cube(num):
    """Return the cube of a number."""
    return jsonify(result=num ** 3)

# 21. Palindrome check
@app.route('/palindrome', methods=['GET'])
def palindrome():
    """Check if 'text' is a palindrome."""
    text = request.args.get('text', '')
    is_palindrome = text == text[::-1]
    return jsonify(palindrome=is_palindrome)

# 22. List all quotes
@app.route('/quotes', methods=['GET'])
def all_quotes():
    """Return all quotes."""
    return jsonify(quotes=QUOTES)

# 23. Add a new quote
@app.route('/quotes', methods=['POST'])
def add_quote():
    """Add a new quote to the list."""
    data = request.json
    quote = data.get('quote') if data else None
    if quote:
        QUOTES.append(quote)
        return jsonify(message='Quote added!')
    return jsonify(error='No quote provided'), 400

# 24. Remove a quote by index
@app.route('/quotes/<int:index>', methods=['DELETE'])
def remove_quote(index):
    """Remove a quote by its index."""
    if 0 <= index < len(QUOTES):
        removed = QUOTES.pop(index)
        return jsonify(removed=removed)
    return jsonify(error='Invalid index'), 400

# 25. List all dictionary words
@app.route('/dictionary', methods=['GET'])
def list_dictionary():
    """List all words in the dictionary."""
    return jsonify(words=list(DICTIONARY.keys()))

# 26. Add a word to dictionary
@app.route('/dictionary', methods=['POST'])
def add_word():
    """Add a new word and meaning to the dictionary."""
    data = request.json
    word = data.get('word') if data else None
    meaning = data.get('meaning') if data else None
    if word and meaning:
        DICTIONARY[word.lower()] = meaning
        return jsonify(message='Word added!')
    return jsonify(error='Word or meaning missing'), 400

# 27. Remove a word from dictionary
@app.route('/dictionary/<word>', methods=['DELETE'])
def remove_word(word):
    """Remove a word from the dictionary."""
    if word.lower() in DICTIONARY:
        del DICTIONARY[word.lower()]
        return jsonify(message='Word removed!')
    return jsonify(error='Word not found'), 404

# 28. Get length of a string
@app.route('/length', methods=['GET'])
def length():
    """Return the length of 'text'."""
    text = request.args.get('text', '')
    return jsonify(length=len(text))

# 29. Repeat a string n times
@app.route('/repeat', methods=['GET'])
def repeat():
    """Repeat 'text' n times."""
    text = request.args.get('text', '')
    n = request.args.get('n', type=int, default=1)
    return text * n

# 30. Get ASCII value of a character
@app.route('/ascii', methods=['GET'])
def ascii_value():
    """Return ASCII value of 'char'."""
    char = request.args.get('char', '')
    if len(char) != 1:
        return jsonify(error='Provide a single character'), 400
    return jsonify(ascii=ord(char))

# 31. Get character from ASCII value
@app.route('/char', methods=['GET'])
def char_from_ascii():
    """Return character for ASCII value 'code'."""
    code = request.args.get('code', type=int)
    if code is None or not (0 <= code <= 127):
        return jsonify(error='Invalid ASCII code'), 400
    return chr(code)

# 32. Get day of the week
@app.route('/weekday', methods=['GET'])
def weekday():
    """Return the current day of the week."""
    return datetime.now().strftime('%A')

# 33. Get month name
@app.route('/month', methods=['GET'])
def month():
    """Return the current month name."""
    return datetime.now().strftime('%B')

# 34. Get year
@app.route('/year', methods=['GET'])
def year():
    """Return the current year."""
    return datetime.now().strftime('%Y')

# 35. Check if a year is leap year
@app.route('/isleap/<int:year>')
def is_leap(year):
    """Check if a year is a leap year."""
    is_leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
    return jsonify(leap=is_leap)

# 36. Get list of numbers from 1 to n
@app.route('/numbers/<int:n>')
def numbers(n):
    """Return a list of numbers from 1 to n."""
    return jsonify(numbers=list(range(1, n+1)))

# 37. Sum of numbers from 1 to n
@app.route('/sum/<int:n>')
def sum_n(n):
    """Return the sum of numbers from 1 to n."""
    return jsonify(sum=sum(range(1, n+1)))

# 38. Factorial of a number
@app.route('/factorial/<int:n>')
def factorial(n):
    """Return the factorial of n."""
    if n < 0:
        return jsonify(error='Negative number'), 400
    result = 1
    for i in range(1, n+1):
        result *= i
    return jsonify(factorial=result)

# 39. Fibonacci sequence up to n terms
@app.route('/fibonacci/<int:n>')
def fibonacci(n):
    """Return the first n Fibonacci numbers."""
    if n <= 0:
        return jsonify(error='n must be positive'), 400
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return jsonify(fibonacci=seq[:n])

# 40. Prime check
@app.route('/isprime/<int:n>')
def is_prime(n):
    """Check if n is a prime number."""
    if n < 2:
        return jsonify(prime=False)
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return jsonify(prime=False)
    return jsonify(prime=True)

# 41. List all primes up to n
@app.route('/primes/<int:n>')
def primes(n):
    """Return all prime numbers up to n."""
    def is_p(x):
        if x < 2:
            return False
        for i in range(2, int(x ** 0.5) + 1):
            if x % i == 0:
                return False
        return True
    return jsonify(primes=[x for x in range(2, n+1) if is_p(x)])

# 42. Random number between a and b
@app.route('/random', methods=['GET'])
def random_number():
    """Return a random integer between 'a' and 'b'."""
    a = request.args.get('a', type=int, default=0)
    b = request.args.get('b', type=int, default=100)
    if a > b:
        return jsonify(error='a must be <= b'), 400
    return jsonify(random=random.randint(a, b))

# 43. Capitalize a string
@app.route('/capitalize', methods=['GET'])
def capitalize():
    """Capitalize the first letter of 'text'."""
    text = request.args.get('text', '')
    return text.capitalize()

# 44. Swap case of a string
@app.route('/swapcase', methods=['GET'])
def swapcase():
    """Swap case of 'text'."""
    text = request.args.get('text', '')
    return text.swapcase()

# 45. Remove spaces from a string
@app.route('/removespaces', methods=['GET'])
def remove_spaces():
    """Remove all spaces from 'text'."""
    text = request.args.get('text', '')
    return text.replace(' ', '')

# 46. Count vowels in a string
@app.route('/vowels', methods=['GET'])
def count_vowels():
    """Count vowels in 'text'."""
    text = request.args.get('text', '').lower()
    count = sum(1 for c in text if c in 'aeiou')
    return jsonify(vowels=count)

# 47. Count words in a string
@app.route('/wordcount', methods=['GET'])
def word_count():
    """Count words in 'text'."""
    text = request.args.get('text', '')
    count = len(text.split())
    return jsonify(words=count)

# 48. Get initials from a name
@app.route('/initials', methods=['GET'])
def initials():
    """Return initials from 'name'."""
    name = request.args.get('name', '')
    initials = ''.join([part[0].upper() for part in name.split() if part])
    return initials

# 49. Check if string contains a substring
@app.route('/contains', methods=['GET'])
def contains():
    """Check if 'text' contains 'substr'."""
    text = request.args.get('text', '')
    substr = request.args.get('substr', '')
    return jsonify(contains=substr in text)

# 50. Replace substring in a string
@app.route('/replace', methods=['GET'])
def replace():
    """Replace 'old' with 'new' in 'text'."""
    text = request.args.get('text', '')
    old = request.args.get('old', '')
    new = request.args.get('new', '')
    return text.replace(old, new)

if __name__ == '__main__':
    app.run(debug=True) 