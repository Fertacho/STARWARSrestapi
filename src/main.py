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
from models import db, User, People, Planets, Fav_people, Fav_planets
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


@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    array_people = list(map(lambda x : x.serialize(), all_people))
    return jsonify({"mensaje":array_people})
# this only runs if `$ python src/main.py` is executed

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id():
    one_people = People.query.get(people_id)
    if one_people:
        return jsonify({"personaje": one_people.serialize()})
    else:
        return "ha ocurrido un error"
@app.route('/planets', methods = ['GET'])
def get_planets():
    all_planets = Planets.query.all()
    array_planets = list(map(lambda x : x.serialize(), all_planets))
    return jsonify({"mensaje": array_planets})

@app.route('/planets/<int:planets_id>', methods = ['GET'])
def get_planets_id():
    one_planet = Planets.query.get(planets_id)
    if one_planet:
        return jsonify({"personaje": one_people.serialize()})
    else:
        return "ha ocurrido un error"

@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.query.all()
    array_users = list(map(lambda x: x.serialize(), all_users))
    return jsonify({"users":array_users})
"""
@app.route('/user/favorite/people', methods=['GET'])
def get_favorite_people():
    all_fav_people = Fav_people.query.all()
    array_fav_people = list(map(lambda x : x.serialize(), all_fav_people))
    return jsonify({"mensaje":array_fav_people})
@app.route('/user/favorite/planets', methods=['GET'])
def get_favorite_planets():
    all_fav_planets = Fav_planets.query.all()
    array_fav_planets = list(map(lambda x : x.serialize(), all_fav_planets))
    return jsonify({"mensaje":array_fav_planets})
"""
@app.route('/user/favorites', methods = ['GET'])
def get_favorites():
    all_fav_people = Fav_people.query.all()
    all_fav_planets = Fav_planets.query.all()
    array_fav_people = list(map(lambda x : x.serialize(), all_fav_people))
    array_fav_planets = list(map(lambda x : x.serialize(), all_fav_planets))
    array_people_and_planets = array_fav_people + array_fav_planets
    print(array_people_and_planets)
    #return jsonify({"favorites": array_people_and_planets})
    return jsonify({"favorites":array_people_and_planets})

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planets(planet_id):
    user = request.get_json()
    checkuser = User.query.get(user['id'])
    if checkuser:
        new_fav = Fav_planets()
        new_fav.id_user = user['id']
        new_fav.id_planet = planet_id
        db.session.add(new_fav)
        db.session.commit()
        return("todo bien")
    else:
        return ("el usuario no existe")    

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user = request.get_json()
    checkuser = User.query.get(user['id'])
    if checkuser:
        new_fav = Fav_people()
        new_fav.id_user = user['id']
        new_fav.uid_people = people_id
        db.session.add(new_fav)
        db.session.commit()
        return("todo bien")
    else:
        return ("el usuario no existe")

@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_fav_planets(planet_id):
    user = request.get_json()
    all_favs = Fav_planets.query.filter_by(id_user=user['id'], id_planets = planet_id).all()
    for i in all_favs:
        db.session.delete(i)
    db.session.commit()
    return ("ok")

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    user = request.get_json()
    all_favs = Fav_people.query.filter_by(id_user=user['id'], uid_people = people_id).all()
    for i in all_favs:
        db.session.delete(i)
    db.session.commit()
    return ("ok")
    
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)