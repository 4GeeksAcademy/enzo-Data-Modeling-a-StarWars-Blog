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
from models import db, User, Planet, Character, FavoritePlanet, FavoriteCharacter

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    return jsonify([person.serialize() for person in people]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    new_planet = Planet(
        name=data['name'],
        climate=data.get('climate', 'unknown'),
        population=data.get('population', 'unknown')
    )
    db.session.add(new_planet)
    db.session.commit()
    
    return jsonify(new_planet.serialize()), 201


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
   
    current_user = User.query.first()
    if current_user is None:
        return jsonify({"error": "No users found"}), 404
    
    favorite_planets = [fp.planet.serialize() for fp in current_user.favorite_planets]
    favorite_characters = [fc.character.serialize() for fc in current_user.favorite_characters]
    
    return jsonify({
        "favorite_planets": favorite_planets,
        "favorite_characters": favorite_characters
    }), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user = User.query.first()
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    

    existing_favorite = FavoritePlanet.query.filter_by(
        user_id=current_user.id, 
        planet_id=planet_id
    ).first()
    
    if existing_favorite:
        return jsonify({"error": "Planet already in favorites"}), 400
    
    new_favorite = FavoritePlanet(user_id=current_user.id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"msg": "Planet added to favorites"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    current_user = User.query.first()
    character = Character.query.get(people_id)
    
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    

    existing_favorite = FavoriteCharacter.query.filter_by(
        user_id=current_user.id, 
        character_id=people_id
    ).first()
    
    if existing_favorite:
        return jsonify({"error": "Character already in favorites"}), 400
    
    new_favorite = FavoriteCharacter(user_id=current_user.id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"msg": "Character added to favorites"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user = User.query.first()
    favorite = FavoritePlanet.query.filter_by(
        user_id=current_user.id, 
        planet_id=planet_id
    ).first()
    
    if favorite is None:
        return jsonify({"error": "Favorite planet not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Planet removed from favorites"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    current_user = User.query.first()
    favorite = FavoriteCharacter.query.filter_by(
        user_id=current_user.id, 
        character_id=people_id
    ).first()
    
    if favorite is None:
        return jsonify({"error": "Favorite character not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Character removed from favorites"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)