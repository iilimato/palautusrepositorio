import pytest
from app import app, games, WINS_TO_END


@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_games():
    """Clear games dict before each test."""
    games.clear()


class TestIndex:
    def test_index_returns_html(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi-Paperi-Sakset' in response.data


class TestNewGame:
    def test_new_game_simple_ai(self, client):
        response = client.post('/api/new-game', json={'game_type': 'simple'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['game_type'] == 'simple'
        assert data['score']['player'] == 0
        assert data['score']['ai'] == 0
        assert data['score']['draws'] == 0

    def test_new_game_enhanced_ai(self, client):
        response = client.post('/api/new-game', json={'game_type': 'enhanced'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['game_type'] == 'enhanced'

    def test_new_game_defaults_to_enhanced(self, client):
        response = client.post('/api/new-game', json={})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['game_type'] == 'enhanced'


class TestPlay:
    def test_play_without_game_returns_error(self, client):
        response = client.post('/api/play', json={'move': 'k'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_play_invalid_move(self, client):
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.post('/api/play', json={'move': 'x'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_play_rock(self, client):
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.post('/api/play', json={'move': 'k'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['player_move'] == 'k'
        assert data['player_move_name'] == 'Kivi'
        assert data['ai_move'] in ['k', 'p', 's']
        assert data['result'] in ['win', 'lose', 'draw']

    def test_play_paper(self, client):
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.post('/api/play', json={'move': 'p'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['player_move'] == 'p'
        assert data['player_move_name'] == 'Paperi'

    def test_play_scissors(self, client):
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.post('/api/play', json={'move': 's'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['player_move'] == 's'
        assert data['player_move_name'] == 'Sakset'

    def test_score_updates_correctly(self, client):
        client.post('/api/new-game', json={'game_type': 'simple'})

        # Play multiple rounds and verify score updates
        total_player = 0
        total_ai = 0
        total_draws = 0

        for _ in range(4):
            response = client.post('/api/play', json={'move': 'k'})
            data = response.get_json()
            if data['result'] == 'win':
                total_player += 1
            elif data['result'] == 'lose':
                total_ai += 1
            else:
                total_draws += 1

            assert data['score']['player'] == total_player
            assert data['score']['ai'] == total_ai
            assert data['score']['draws'] == total_draws


class TestGameLogic:
    def test_rock_beats_scissors(self, client):
        """Test that rock beats scissors."""
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.post('/api/play', json={'move': 'k'})
        data = response.get_json()

        if data['ai_move'] == 's':
            assert data['result'] == 'win'

    def test_paper_beats_rock(self, client):
        """Test that paper beats rock."""
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.post('/api/play', json={'move': 'p'})
        data = response.get_json()

        if data['ai_move'] == 'k':
            assert data['result'] == 'win'

    def test_scissors_beats_paper(self, client):
        """Test that scissors beats paper."""
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.post('/api/play', json={'move': 's'})
        data = response.get_json()

        if data['ai_move'] == 'p':
            assert data['result'] == 'win'

    def test_same_moves_draw(self, client):
        """Test that same moves result in a draw."""
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.post('/api/play', json={'move': 'k'})
        data = response.get_json()

        if data['ai_move'] == 'k':
            assert data['result'] == 'draw'


class TestGetScore:
    def test_get_score_without_game(self, client):
        response = client.get('/api/score')
        assert response.status_code == 400

    def test_get_score_with_game(self, client):
        client.post('/api/new-game', json={'game_type': 'simple'})
        response = client.get('/api/score')
        assert response.status_code == 200
        data = response.get_json()
        assert 'player' in data
        assert 'ai' in data
        assert 'draws' in data
        assert 'history' in data

    def test_history_tracks_moves(self, client):
        client.post('/api/new-game', json={'game_type': 'simple'})
        client.post('/api/play', json={'move': 'k'})
        client.post('/api/play', json={'move': 'p'})

        response = client.get('/api/score')
        data = response.get_json()

        assert len(data['history']) == 2
        assert data['history'][0]['player'] == 'k'
        assert data['history'][1]['player'] == 'p'


class TestGameEnds:
    def test_game_ends_at_5_wins(self, client):
        """Test that game ends when either player or AI reaches 5 wins."""
        client.post('/api/new-game', json={'game_type': 'simple'})

        # Play until game ends
        while True:
            response = client.post('/api/play', json={'move': 'p'})
            data = response.get_json()
            if data.get('game_over'):
                break

        assert data['game_over'] is True
        assert data['game_winner'] in ['player', 'ai']
        # The winner should have exactly 5 wins
        if data['game_winner'] == 'player':
            assert data['score']['player'] == WINS_TO_END
        else:
            assert data['score']['ai'] == WINS_TO_END

    def test_cannot_play_after_game_ends(self, client):
        """Test that playing after game ends returns error."""
        client.post('/api/new-game', json={'game_type': 'simple'})

        # Play until game ends
        while True:
            response = client.post('/api/play', json={'move': 'p'})
            data = response.get_json()
            if response.status_code != 200 or data.get('game_over'):
                break

        # Try to play again
        response = client.post('/api/play', json={'move': 'k'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'over' in data['error'].lower()

    def test_game_over_false_before_5_wins(self, client):
        """Test that game_over is False when neither has 5 wins."""
        client.post('/api/new-game', json={'game_type': 'simple'})

        response = client.post('/api/play', json={'move': 'k'})
        data = response.get_json()

        # Game should not be over after just one round
        if data['score']['player'] < WINS_TO_END and data['score']['ai'] < WINS_TO_END:
            assert data['game_over'] is False
            assert data['game_winner'] is None
