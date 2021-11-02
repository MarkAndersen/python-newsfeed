from flask import Blueprint, request, jsonify
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    # snag json data, access db
    data = request.get_json()
    db = get_db()
    
   
     # use bracket notation instead of dot notation because USER is not an object in python, it is a 'library', it is only an object when creating class and attaching methods to it
     # this creates a new instance of a 'User'
    newUser = User(
        username = data['username'],
        email = data['email'],
        password = data['password']
    )

    # save in db
    db.add(newUser)
    db.commit()

    return jsonify(id = newUser.id)