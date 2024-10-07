from flask import Flask,jsonify,abort,request
from flask_cors import CORS
from models import setup_db,Actor,Movie,insertInitialData,db
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_uri = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_uri=database_uri)

    # Setup cors
    CORS(app)

    '''
        Uncomment this only the first time you run this application 
        to fill your database with some data 
        for checking endpoint functionalities.
    '''
    # insertInitialData(app)

    #ROUTES

    # GET all actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors]
            }), 200
        except:
            abort(500)

    # GET a specific actor by id
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actor') 
    def get_actor(payload,actor_id):
        actor = db.session.get(Actor, actor_id)
        if actor is None:
            abort(404)
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    # GET all movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            }), 200
        except:
            abort(500)

    # GET a specific movie by id
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movie')
    def get_movie(payload,movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    # DELETE an actor by id
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload,actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        }), 200

    # DELETE a movie by id
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload,movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id
        }), 200

    # POST (create) a new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if not body or not body.get('name') or not body.get('age') or not body.get('gender'):
            abort(400)
        
        try:
            new_actor = Actor(
                name=body['name'],
                age=body['age'],
                gender=body['gender']
            )
            new_actor.insert()
            return jsonify({
                'success': True,
                'created': new_actor.id,
                'actor': new_actor.format()
            }), 201  # HTTP 201: Created
        except:
            abort(500)

    # POST (create) a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if not body or not body.get('title') or not body.get('release_date'):
            abort(400)
        
        try:
            new_movie = Movie(
                title=body['title'],
                release_date=body['release_date']
            )
            new_movie.insert()
            return jsonify({
                'success': True,
                'created': new_movie.id,
                'movie': new_movie.format()
            }), 201  # HTTP 201: Created
        except:
            abort(500)

    # PATCH (update) an existing actor by id
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload,actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        
        body = request.get_json()
        try:
            if 'name' in body:
                actor.name = body['name']
            if 'age' in body:
                actor.age = body['age']
            if 'gender' in body:
                actor.gender = body['gender']
            
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except:
            abort(500)

    # PATCH (update) an existing movie by id
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload,movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        
        body = request.get_json()
        try:
            if 'title' in body:
                movie.title = body['title']
            if 'release_date' in body:
                movie.release_date = body['release_date']
            
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
        except:
            abort(500)

    #Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request.'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found.'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity.'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error.'
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()