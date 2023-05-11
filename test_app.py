from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    def setUp(self):
        """Set up test client before running tests."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Check if index route is working correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Score:', response.data)
        self.assertIn(b'Time Remaining:', response.data)
    
    def test_valid_word(self):
        """Check if word is correctly recognized on board"""
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["H", "E", "L", "L", "O"], 
                            ["T", "E", "W", "T", "T"],
                            ["D", "E", "O", "G", "G"],
                            ["A", "B", "S", "G", "E"],
                            ["A", "B", "C", "T", "E"]]
        word = 'test'
        response = self.client.post('/check-word', data={'word': word})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Check if word is in the dictionary"""
        self.client.get('/')
        response = self.client.post('/check-word', data=dict(word="TESTINGINVALID"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'result': 'not-word'})

    def test_empty_word(self):
        """Check for submitting an empty word"""
        self.client.get('/')
        response = self.client.post('/check-word', data=dict(word=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'result': 'not-word'})

    def test_update_stats(self):
        """Check that high score and games played are being updated"""
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['highest_score'] = 10
                change_session['games_played'] = 1

        response = self.client.post('/update-stats', json={'score': 15})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('highest_score', data)
        self.assertIn('games_played', data)
        self.assertEqual(data['highest_score'], 15)
        self.assertEqual(data['games_played'], 2)

        response = self.client.post('/update-stats', json={'score': 5})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('highest_score', data)
        self.assertIn('games_played', data)
        self.assertEqual(data['highest_score'], 15)
        self.assertEqual(data['games_played'], 3)


    


   
