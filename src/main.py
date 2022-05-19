"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.filter_by(id=people_id)
    person_serialized = person.serialize() 

    # print(person)
    return jsonify(person_serialized), 200

@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    users_serialized = [all_users.serialize() for user in all_users]
    return jsonify(users_serialized), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_all_favorites(user_id):
    user = User.query.get(id=users_id)
    favorite_people = user.people
    favorite_planets = user.planets
    all_favorites = favorite_people + favorite_planets
    favorites_serialized = [all_favorites.serialize() for favorite in all_favorites]
    return jsonify(favorites_serialized), 200


@app.route('/people', methods=['GET'])
def get_all_people():
    all_people_list = People.query.all()
    people_serialized = [people.serialize() for people in all_people_list]


    return jsonify(people_serialized), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets_list = planets.query.all()
    planets_serialized = [planets.serialize() for planets in all_planets_list]


    return jsonify(planets_serialized), 200



@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    planet = Planets.query.get(id=planets_id)
    planet_serialized = planet.serialize() 


    return jsonify(planet_serialized), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
