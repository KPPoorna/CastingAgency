import os
import unittest
import json
from dotenv import load_dotenv
from models import Actor, Movie, db
from app import create_app  
from unittest.mock import patch

class AppTestCase(unittest.TestCase):
    """This class represents the Flask app test case"""

    # Load environment variables from .env file
    load_dotenv()  

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_uri = os.getenv('TEST_DATABASE_URI')
       
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_uri
        })
        
        self.client = self.app.test_client()
        self.db = db

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.drop_all()

    # Helper function to add test data
    def add_test_data(self):
        """Add sample data to the database"""
        with self.app.app_context():
            actor1 = Actor(name='actor1', age=64, gender='Male')
            actor2 = Actor(name='actor2', age=34, gender='Female')
            movie1 = Movie(title='movie1', release_date='1994-07-06')
            movie2 = Movie(title='movie2', release_date='2005-07-06')

            actor1.insert()
            actor2.insert()
            movie1.insert()
            movie2.insert()

#######################################################################################################################################################

#   TESTING ENDPOINTS

#######################################################################################################################################################

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_get_actors_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test GET /actors for success"""
        
        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["get:actors"]} 

        self.add_test_data()
        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) == 2)

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_get_actors_when_no_actors_exist(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test GET /actors when no actors exist"""
        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["get:actors"]} 

        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) 
        self.assertTrue(data['success'])
        self.assertEqual(data['actors'], [])

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_get_actor_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test GET /actors/<id> for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["get:actor"]} 

        self.add_test_data()
        with self.app.app_context():
            actor_id = Actor.query.first().id
        
        res = self.client.get(f'/actors/{actor_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], 'actor1')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_get_actor_error(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test GET /actors/<id> for error (actor not found)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["get:actor"]} 

        res = self.client.get('/actors/999')  
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found.')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_get_movies_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test GET /movies for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["get:movies"]} 

        self.add_test_data()
        res = self.client.get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) == 2)

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_get_movies_when_no_movies_exist(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test GET /movies for error (if no movies exist)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["get:movies"]} 

        res = self.client.get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)  
        self.assertTrue(data['success'])
        self.assertEqual(data['movies'], [])

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_get_movie_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test GET /movies/<id> for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["get:movie"]} 

        self.add_test_data()
        with self.app.app_context():
            movie_id = Movie.query.first().id
        
        res = self.client.get(f'/movies/{movie_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], 'movie1')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_get_movie_error(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test GET /movies/<id> for error (movie not found)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["get:movie"]} 

        res = self.client.get('/movies/999')  
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found.')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_create_actor_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test POST /actors for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["post:actors"]} 

        new_actor = {
            'name': 'new actor',
            'age': 47,
            'gender': 'Male'
        }
        res = self.client.post('/actors', json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], 'new actor')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_create_actor_error(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test POST /actors for error (missing fields)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["post:actors"]} 

        new_actor = {
            'name': 'new actor'
            # Missing age and gender
        }
        res = self.client.post('/actors', json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad request.')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_create_movie_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test POST /movies for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["post:movies"]} 

        new_movie = {
            'title': 'new movie',
            'release_date': '2010-07-16'
        }
        res = self.client.post('/movies', json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], 'new movie')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_create_movie_error(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test POST /movies for error (missing fields)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["post:movies"]} 

        new_movie = {
            'title': 'new movie'
            # Missing release_date
        }
        res = self.client.post('/movies', json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad request.')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_delete_actor_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test DELETE /actors/<id> for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["delete:actors"]} 

        self.add_test_data()
        with self.app.app_context():
            actor_id = Actor.query.first().id
        
        res = self.client.delete(f'/actors/{actor_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], actor_id)

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_delete_actor_error(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test DELETE /actors/<id> for error (actor not found)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["delete:actors"]} 

        res = self.client.delete('/actors/999')  
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found.')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_delete_movie_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test DELETE /movies/<id> for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["delete:movies"]} 

        self.add_test_data()
        with self.app.app_context():
            movie_id = Movie.query.first().id
        
        res = self.client.delete(f'/movies/{movie_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], movie_id)

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_delete_movie_error(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test DELETE /movies/<id> for error (movie not found)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["delete:movies"]} 

        res = self.client.delete('/movies/999') 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found.')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_update_actor_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test PATCH /actors/<id> for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["patch:actors"]} 

        self.add_test_data()
        with self.app.app_context():
            actor_id = Actor.query.first().id
        
        updated_actor = {
            'name': 'new name',
        }
        res = self.client.patch(f'/actors/{actor_id}', json=updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], 'new name')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_update_actor_error(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test PATCH /actors/<id> for error (actor not found)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["patch:actors"]} 

        updated_actor = {
            'name': 'new name'
        }
        res = self.client.patch('/actors/999', json=updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found.')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_update_movie_success(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test PATCH /movies/<id> for success"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["patch:movies"]} 

        self.add_test_data()
        with self.app.app_context():
            movie_id = Movie.query.first().id
        
        updated_movie = {
            'title': 'New Movie Title',
        }
        res = self.client.patch(f'/movies/{movie_id}', json=updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], 'New Movie Title')

    @patch('auth.requires_auth')  # Mocking the requires_auth decorator
    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_update_movie_error(self,mock_verify_decode_jwt, mock_get_token_auth_header, mock_requires_auth):
        """Test PATCH /movies/<id> for error (movie not found)"""

        # Mocking the authorization functions
        mock_requires_auth.return_value = True  
        mock_get_token_auth_header.return_value = "mock_token" 
        mock_verify_decode_jwt.return_value = {"permissions": ["patch:movies"]} 

        updated_movie = {
            'title': 'New Movie Title'
        }
        res = self.client.patch('/movies/999', json=updated_movie)  
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found.')


#######################################################################################################################################################

#   TESTING RBAC Roles

#######################################################################################################################################################
    
    #Tests for Casting Assistant Role

    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_casting_assistant_for_permitted_actions(self, mock_verify_decode_jwt, mock_get_token_auth_header):
        """Test that a casting assistant can access GET endpoints for actors and movies"""

        # Mocking the token extraction and JWT payload for casting assistant
        mock_get_token_auth_header.return_value = "mock_token"  
        mock_verify_decode_jwt.return_value = {
            "permissions": ["get:actors", "get:actor", "get:movies", "get:movie"]
        }

        self.add_test_data()  # Ensure test data is added

        # Permitted actions for casting assistant (GET requests)
        res1 = self.client.get('/actors')  
        res2 = self.client.get('/actors/1')
        res3 = self.client.get('/movies')
        res4 = self.client.get('/movies/1')

        # Casting assistant is allowed to access these endpoints
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(res4.status_code, 200)

    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_casting_assistant_for_forbidden_actions(self, mock_verify_decode_jwt, mock_get_token_auth_header):
        """Test that a casting assistant cannot perform POST, PATCH, or DELETE actions on actors and movies"""

        # Mocking the token extraction and JWT payload for casting assistant
        mock_get_token_auth_header.return_value = "mock_token"  
        mock_verify_decode_jwt.return_value = {
            "permissions": ["get:actors", "get:actor", "get:movies", "get:movie"]
        }

        self.add_test_data()  # Ensure test data is added

        # Forbidden actions for casting assistant (POST, PATCH, DELETE)
        res1 = self.client.post('/actors', json={'name': 'New Actor', 'age': 30, 'gender': 'Male'})
        res2 = self.client.patch('/actors/1', json={'name': 'Updated Name'})
        res3 = self.client.delete('/actors/1')

        res4 = self.client.post('/movies', json={'title': 'New Movie', 'release_date': '2023-10-01'})
        res5 = self.client.patch('/movies/1', json={'title': 'Updated Title'})
        res6 = self.client.delete('/movies/1')

        # Casting assistant is forbidden from these actions
        self.assertEqual(res1.status_code, 403)  # Forbidden for POST actors
        self.assertEqual(res2.status_code, 403)  # Forbidden for PATCH actors
        self.assertEqual(res3.status_code, 403)  # Forbidden for DELETE actors
        self.assertEqual(res4.status_code, 403)  # Forbidden for POST movies
        self.assertEqual(res5.status_code, 403)  # Forbidden for PATCH movies
        self.assertEqual(res6.status_code, 403)  # Forbidden for DELETE movies

    #Tests for Casting Director Role

    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_casting_director_for_permitted_actions(self, mock_verify_decode_jwt, mock_get_token_auth_header):
        """Test that a casting director can perform POST, PATCH, and DELETE actions on actors, and PATCH movies"""

        # Mocking the token extraction and JWT payload for casting director
        mock_get_token_auth_header.return_value = "mock_token"  
        mock_verify_decode_jwt.return_value = {
            "permissions": [
                "delete:actors", "get:actor", "get:actors", "get:movie", "get:movies",
                "patch:actors", "patch:movies", "post:actors"
            ]
        }

        self.add_test_data()  # Ensure test data is added

        # Permitted actions for casting director
        res1 = self.client.post('/actors', json={'name': 'New Actor', 'age': 30, 'gender': 'Male'})
        res2 = self.client.patch('/actors/1', json={'name': 'Updated Name'})
        res3 = self.client.delete('/actors/1')
        res4 = self.client.patch('/movies/1', json={'title': 'Updated Movie Title'})

        # Casting director is allowed to perform these actions
        self.assertEqual(res1.status_code, 201)  # POST actors
        self.assertEqual(res2.status_code, 200)  # PATCH actors
        self.assertEqual(res3.status_code, 200)  # DELETE actors
        self.assertEqual(res4.status_code, 200)  # PATCH movies

    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_casting_director_for_forbidden_actions(self, mock_verify_decode_jwt, mock_get_token_auth_header):
        """Test that a casting director cannot POST or DELETE movies"""

        # Mocking the token extraction and JWT payload for casting director
        mock_get_token_auth_header.return_value = "mock_token"  
        mock_verify_decode_jwt.return_value = {
            "permissions": [
                "delete:actors", "get:actor", "get:actors", "get:movie", "get:movies",
                "patch:actors", "patch:movies", "post:actors"
            ]
        }

        self.add_test_data()  # Ensure test data is added

        # Forbidden actions for casting director (POST and DELETE movies)
        res1 = self.client.post('/movies', json={'title': 'New Movie', 'release_date': '2023-10-01'})
        res2 = self.client.delete('/movies/1')

        # Casting director is forbidden from these actions
        self.assertEqual(res1.status_code, 403)  # Forbidden for POST movies
        self.assertEqual(res2.status_code, 403)  # Forbidden for DELETE movies

    # Test for Executive Director

    @patch('auth.get_token_auth_header')  # Mocking the token extraction
    @patch('auth.verify_decode_jwt')  # Mocking the JWT verification
    def test_executive_producer_for_permitted_actions(self, mock_verify_decode_jwt, mock_get_token_auth_header):
        """Test that an executive producer can perform all actions on actors and movies"""

        # Mocking the token extraction and JWT payload for executive producer
        mock_get_token_auth_header.return_value = "mock_token"  
        mock_verify_decode_jwt.return_value = {
            "permissions": [
                "delete:actors", "delete:movies", "get:actor", "get:actors", "get:movie", "get:movies",
                "patch:actors", "patch:movies", "post:actors", "post:movies"
            ]
        }

        self.add_test_data()  # Ensure test data is added

        # Permitted actions for executive producer (POST, PATCH, DELETE for both actors and movies)
        res1 = self.client.post('/actors', json={'name': 'New Actor', 'age': 30, 'gender': 'Male'})
        res2 = self.client.patch('/actors/1', json={'name': 'Updated Name'})
        res3 = self.client.delete('/actors/1')
        res4 = self.client.post('/movies', json={'title': 'New Movie', 'release_date': '2023-10-01'})
        res5 = self.client.patch('/movies/1', json={'title': 'Updated Movie Title'})
        res6 = self.client.delete('/movies/1')

        # Executive producer is allowed to perform these actions
        self.assertEqual(res1.status_code, 201)  # POST actors
        self.assertEqual(res2.status_code, 200)  # PATCH actors
        self.assertEqual(res3.status_code, 200)  # DELETE actors
        self.assertEqual(res4.status_code, 201)  # POST movies
        self.assertEqual(res5.status_code, 200)  # PATCH movies
        self.assertEqual(res6.status_code, 200)  # DELETE movies

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

