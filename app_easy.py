from flask import Flask, jsonify
from crossword import get_crossword, get_rand_word
from flask_cors import CORS, cross_origin     
app = Flask(__name__)
CORS = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/<string:main_word>')
@cross_origin()
def index(main_word):
    return jsonify(get_crossword(main_word))

@app.route('/rand')
@cross_origin()
def rand():
    return jsonify(get_rand_word())

app.run(port='2137', debug=True)