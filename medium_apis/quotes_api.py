from flask import Blueprint, request, jsonify

quotes_bp = Blueprint('quotes', __name__, url_prefix='/quotes')

# In-memory list of quotes
QUOTES = [
    {'id': 1, 'text': 'The best way to get started is to quit talking and begin doing.'},
    {'id': 2, 'text': "Don't let yesterday take up too much of today."},
    {'id': 3, 'text': "It's not whether you get knocked down, it's whether you get up."}
]

@quotes_bp.route('/', methods=['GET'])
def list_quotes():
    """List all quotes."""
    return jsonify(quotes=QUOTES)

@quotes_bp.route('/<int:qid>', methods=['GET'])
def get_quote(qid):
    """Get a quote by its id."""
    for q in QUOTES:
        if q['id'] == qid:
            return jsonify(q)
    return jsonify(error='Quote not found'), 404

@quotes_bp.route('/', methods=['POST'])
def add_quote():
    """Add a new quote. Expects JSON: text."""
    data = request.json
    text = data.get('text') if data else None
    if not text:
        return jsonify(error='No text provided'), 400
    new_id = max((q['id'] for q in QUOTES), default=0) + 1
    quote = {'id': new_id, 'text': text}
    QUOTES.append(quote)
    return jsonify(quote), 201

@quotes_bp.route('/<int:qid>', methods=['PUT'])
def update_quote(qid):
    """Update a quote by id. Expects JSON: text."""
    data = request.json
    text = data.get('text') if data else None
    for q in QUOTES:
        if q['id'] == qid:
            if text:
                q['text'] = text
                return jsonify(q)
            return jsonify(error='No text provided'), 400
    return jsonify(error='Quote not found'), 404

@quotes_bp.route('/<int:qid>', methods=['DELETE'])
def delete_quote(qid):
    """Delete a quote by id."""
    for i, q in enumerate(QUOTES):
        if q['id'] == qid:
            del QUOTES[i]
            return jsonify(message='Quote deleted!')
    return jsonify(error='Quote not found'), 404 