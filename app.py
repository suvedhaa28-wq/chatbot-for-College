from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime
from nlp_engine import ExamChatbotNLPEngine

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'faqs.json')

# Initialize NLP Engine
nlp_engine = ExamChatbotNLPEngine(DATA_FILE)

@app.route('/')
def index():
    """Renders main application template."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main Chat API Endpoint.
    Receives student query and returns NLP matched response.
    """
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({
            'success': False,
            'response': 'Please enter a valid question.',
            'suggestions': nlp_engine.default_suggestions,
            'timestamp': datetime.now().strftime('%I:%M %p')
        })

    # Process query through NLP pipeline
    result = nlp_engine.process_query(user_message)
    result['timestamp'] = datetime.now().strftime('%I:%M %p')
    return jsonify(result)

@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    """Returns all FAQs for Admin view and search."""
    search_query = request.args.get('search', '').lower().strip()
    category_filter = request.args.get('category', '').strip()

    faqs = nlp_engine.faqs

    if search_query:
        faqs = [
            f for f in faqs
            if search_query in f['question'].lower()
            or search_query in f['intent'].lower()
            or search_query in f['response'].lower()
            or any(search_query in p.lower() for p in f.get('patterns', []))
        ]

    if category_filter:
        faqs = [f for f in faqs if f.get('category') == category_filter]

    categories = list(set(f.get('category', 'General') for f in nlp_engine.faqs))

    return jsonify({
        'success': True,
        'count': len(faqs),
        'categories': categories,
        'faqs': faqs
    })

@app.route('/api/faqs', methods=['POST'])
def add_faq():
    """Admin Endpoint: Add a new FAQ."""
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    intent = data.get('intent', '').strip()
    response_text = data.get('response', '').strip()
    category = data.get('category', 'General').strip()
    patterns_raw = data.get('patterns', [])

    if not question or not intent or not response_text:
        return jsonify({
            'success': False,
            'message': 'Question, Intent, and Response are required fields.'
        }), 400

    if isinstance(patterns_raw, str):
        patterns = [p.strip() for p in patterns_raw.split(',') if p.strip()]
    else:
        patterns = [str(p).strip() for p in patterns_raw if str(p).strip()]

    # Generate new unique ID
    max_id = max([f.get('id', 0) for f in nlp_engine.faqs], default=0)
    new_faq = {
        'id': max_id + 1,
        'intent': intent.lower().replace(' ', '_'),
        'category': category,
        'question': question,
        'patterns': patterns if patterns else [question.lower()],
        'response': response_text
    }

    nlp_engine.faqs.append(new_faq)
    nlp_engine.save_faqs(nlp_engine.faqs)

    return jsonify({
        'success': True,
        'message': 'FAQ added successfully!',
        'faq': new_faq
    }), 201

@app.route('/api/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    """Admin Endpoint: Edit/Update an existing FAQ."""
    data = request.get_json() or {}
    
    faq_index = next((i for i, f in enumerate(nlp_engine.faqs) if f['id'] == faq_id), None)
    if faq_index is None:
        return jsonify({'success': False, 'message': 'FAQ not found.'}), 404

    current_faq = nlp_engine.faqs[faq_index]
    
    if 'question' in data:
        current_faq['question'] = data['question'].strip()
    if 'intent' in data:
        current_faq['intent'] = data['intent'].strip().lower().replace(' ', '_')
    if 'response' in data:
        current_faq['response'] = data['response'].strip()
    if 'category' in data:
        current_faq['category'] = data['category'].strip()
    if 'patterns' in data:
        patterns_raw = data['patterns']
        if isinstance(patterns_raw, str):
            current_faq['patterns'] = [p.strip() for p in patterns_raw.split(',') if p.strip()]
        else:
            current_faq['patterns'] = [str(p).strip() for p in patterns_raw if str(p).strip()]

    nlp_engine.faqs[faq_index] = current_faq
    nlp_engine.save_faqs(nlp_engine.faqs)

    return jsonify({
        'success': True,
        'message': 'FAQ updated successfully!',
        'faq': current_faq
    })

@app.route('/api/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    """Admin Endpoint: Delete an FAQ."""
    faq_index = next((i for i, f in enumerate(nlp_engine.faqs) if f['id'] == faq_id), None)
    if faq_index is None:
        return jsonify({'success': False, 'message': 'FAQ not found.'}), 404

    deleted = nlp_engine.faqs.pop(faq_index)
    nlp_engine.save_faqs(nlp_engine.faqs)

    return jsonify({
        'success': True,
        'message': f'FAQ "{deleted["question"]}" deleted successfully.'
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Returns analytics and database stats."""
    categories = set(f.get('category', 'General') for f in nlp_engine.faqs)
    intents = set(f.get('intent') for f in nlp_engine.faqs)
    patterns_count = sum(len(f.get('patterns', [])) for f in nlp_engine.faqs)

    return jsonify({
        'success': True,
        'total_faqs': len(nlp_engine.faqs),
        'total_categories': len(categories),
        'total_intents': len(intents),
        'total_patterns': patterns_count
    })

if __name__ == '__main__':
    print("===============================================================")
    print("   COLLEGE EXAMINATION FAQ CHATBOT SERVER STARTING           ")
    print("   Access Web Application at: http://127.0.0.1:5000         ")
    print("===============================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
