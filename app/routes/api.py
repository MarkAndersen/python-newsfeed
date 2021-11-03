from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
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

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])

        return jsonify(message = 'Incorrect credentials'), 400
    
    if user.verify_password(data['password'])== False:
        return jsonify(message = 'Incorrect credentials'), 400

    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return jsonify(id = user.id)

@bp.route('/comments', methods=['POST'])
def comment():
    # connect to db and capture the posted json data.
    data = request.get_json()
    db = get_db

    try:
        # create a new comment
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newComment)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Comment failed'), 500
    
    return jsonify(id = newComment.id)

@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
    # connect to db and capture the posted json data
    data = request.get_json()
    db = get_db()

    try:
        # create a new vote with incoming id and session id
        newVote = Vote(
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Upvote failed'), 500
    
    return '', 204
    