import secrets

from flask import Flask, render_template, request, jsonify, session
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store game sessions (in production, use a proper session store)
games = {}

WINS_TO_END = 3


def get_game_state():
    """Get or create game state for current session."""
    session_id = session.get('game_id')
    if session_id and session_id in games:
        return games[session_id]
    return None


def create_game(game_type):
    """Create a new game with the specified AI type."""
    session_id = secrets.token_hex(8)
    session['game_id'] = session_id

    if game_type == 'simple':
        ai = Tekoaly()
    else:
        ai = TekoalyParannettu(10)

    games[session_id] = {
        'tuomari': Tuomari(),
        'ai': ai,
        'game_type': game_type,
        'history': []
    }
    return games[session_id]


def get_move_name(move):
    """Convert move code to Finnish name."""
    names = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}
    return names.get(move, move)


def get_move_emoji(move):
    """Get emoji for move."""
    emojis = {'k': '🪨', 'p': '📄', 's': '✂️'}
    return emojis.get(move, '')


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new game."""
    data = request.get_json()
    game_type = data.get('game_type', 'enhanced')

    game = create_game(game_type)
    tuomari = game['tuomari']

    return jsonify({
        'success': True,
        'game_type': game_type,
        'score': {
            'player': tuomari.ekan_pisteet,
            'ai': tuomari.tokan_pisteet,
            'draws': tuomari.tasapelit
        }
    })


@app.route('/api/play', methods=['POST'])
def play():
    """Play a round."""
    game = get_game_state()
    if not game:
        return jsonify({'error': 'No active game. Start a new game first.'}), 400

    tuomari = game['tuomari']

    # Check if game is already over
    if tuomari.ekan_pisteet >= WINS_TO_END or tuomari.tokan_pisteet >= WINS_TO_END:
        return jsonify({'error': 'Game is over. Start a new game.'}), 400

    data = request.get_json()
    player_move = data.get('move', '').lower()

    if player_move not in ['k', 'p', 's']:
        return jsonify({'error': 'Invalid move. Use k, p, or s.'}), 400

    ai = game['ai']

    # Get AI move
    ai_move = ai.anna_siirto()

    # Record the round
    tuomari.kirjaa_siirto(player_move, ai_move)

    # Feed player's move to AI for learning (important for enhanced AI)
    ai.aseta_siirto(player_move)

    # Determine winner
    if player_move == ai_move:
        result = 'draw'
        result_text = 'Tasapeli!'
    elif (player_move == 'k' and ai_move == 's') or \
         (player_move == 'p' and ai_move == 'k') or \
         (player_move == 's' and ai_move == 'p'):
        result = 'win'
        result_text = 'Voitit!'
    else:
        result = 'lose'
        result_text = 'Hävisit!'

    # Add to history
    game['history'].append({
        'player': player_move,
        'ai': ai_move,
        'result': result
    })

    # Check if game is over
    game_over = False
    game_winner = None
    if tuomari.ekan_pisteet >= WINS_TO_END:
        game_over = True
        game_winner = 'player'
    elif tuomari.tokan_pisteet >= WINS_TO_END:
        game_over = True
        game_winner = 'ai'

    return jsonify({
        'success': True,
        'player_move': player_move,
        'player_move_name': get_move_name(player_move),
        'player_move_emoji': get_move_emoji(player_move),
        'ai_move': ai_move,
        'ai_move_name': get_move_name(ai_move),
        'ai_move_emoji': get_move_emoji(ai_move),
        'result': result,
        'result_text': result_text,
        'score': {
            'player': tuomari.ekan_pisteet,
            'ai': tuomari.tokan_pisteet,
            'draws': tuomari.tasapelit
        },
        'game_over': game_over,
        'game_winner': game_winner
    })


@app.route('/api/score', methods=['GET'])
def get_score():
    """Get current score."""
    game = get_game_state()
    if not game:
        return jsonify({'error': 'No active game.'}), 400

    tuomari = game['tuomari']
    return jsonify({
        'player': tuomari.ekan_pisteet,
        'ai': tuomari.tokan_pisteet,
        'draws': tuomari.tasapelit,
        'history': game['history']
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
