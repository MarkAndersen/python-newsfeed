from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    # snag json data, access db
    data = request.get_json()
    db = get_db()
    
   
     # use bracket notation instead of dot notation because USER is not an object in python, it is a 'library', it is only an object when creating class and attaching methods to it
     # this creates a new instance of a 'User'
     # use a try .. except statement (like try-catch block in JS) for error handling, be very careful abount indentation
    try:
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

    # save in db
        db.add(newUser)
        db.commit()
    except:
        print(sys.exc_info()[0])

        # insert failed, rollback and then send error to front end - helps prevent crashes with pending db connections
        db.rollback()
        return jsonify(message = 'signup failed'), 500

    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True
    return jsonify(id = newUser.id)