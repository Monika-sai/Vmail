from flask import Flask, render_template, request, jsonify
import language_tool_python

app = Flask(__name__)
tool = language_tool_python.LanguageTool('en-US')

def get_matched_word(text, offset, length):
    return text[offset:offset + length]

@app.route('/')
def index():
    return render_template('errorandgrammar.html')

@app.route('/check', methods=['POST'])
def check_text():
    data = request.get_json()
    text = data['text']

    # Perform error and grammar checking
    matches = tool.check(text)

    suggestions = [{'type': 'red' if match.category == 'TYPO' else 'blue',
                    'suggestion': match.replacements[0] if match.replacements else match.message,
                    'word': get_matched_word(text, match.offset, match.errorLength)}
                   for match in matches]

    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
