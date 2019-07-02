from flask import Flask, render_template, request

from hangman.game import Game


app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcomepage.html')


@app.route('/hangman', methods=['GET', 'POST'])
def hangman():
    if request.method == 'GET':
        global game
        game = Game()
        kwargs = {
            'hidden_word': str(game.hidden_answer),
            'gallows': str(game.gallows),
            'history': str(game.history)
        }
        return render_template('gamepage.html', **kwargs)

    elif request.method == 'POST':
        user_guess = request.form['guess']
        user_guess = user_guess.strip()
        guess = game.guess_letter(user_guess)
        if guess is False:
            return render_template('invalidguesspage.html', guess=user_guess)
        kwargs = {
            'hidden_word': str(game.hidden_answer),
            'history': str(game.history),
            'gallows': str(game.gallows)
        }

        if game.won:
            return render_template('resultpage.html', result='Won', word=game.correct_answer)
        elif game.lost:
            return render_template('resultpage.html', result='Lost', word=game.correct_answer)

        return render_template('gamepage.html', **kwargs)


@app.route('/scores')
def scores():
    with open('hangman/scores.txt', 'r') as fp:
        score_lines = fp.readlines()
    return render_template('scorepage.html', scores=score_lines)
