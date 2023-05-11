from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.debug = True
toolbar = DebugToolbarExtension(app)
boggle_game = Boggle()

@app.route('/')
def index():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('board.html', board=board)



@app.route('/check-word', methods=['POST'])
def check_word():
    guess = request.form.get('word', '').strip()
    board = session['board']
    result = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': result})

@app.route('/update-stats', methods=['POST'])
def update_stats():
    score = request.json['score']
    if 'highest_score' not in session or score > session['highest_score']:
        session['highest_score'] = score

    session['games_played'] = session.get('games_played', 0) + 1

    return jsonify({
        'highest_score': session['highest_score'],
        'games_played': session['games_played']
    })