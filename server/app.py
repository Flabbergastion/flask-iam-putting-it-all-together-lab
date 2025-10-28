#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe, UserSchema, RecipeSchema

class Signup(Resource):
    def post(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')
        image_url = json.get('image_url')
        bio = json.get('bio')
        
        if username:
            try:
                user = User(
                    username=username,
                    image_url=image_url,
                    bio=bio
                )
                user.password_hash = password
                
                db.session.add(user)
                db.session.commit()
                
                session['user_id'] = user.id
                
                return user.to_dict(), 201
            
            except IntegrityError:
                db.session.rollback()
                return {'error': 'Username must be unique'}, 422
        else:
            return {'error': 'Username is required'}, 422

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session.get('user_id')).first()
            if user:
                return user.to_dict(), 200
        return {'error': 'No active session'}, 401

class Login(Resource):
    def post(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')
        
        user = User.query.filter(User.username == username).first()
        
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return '', 204
        else:
            return {'error': 'No active session'}, 401

class RecipeIndex(Resource):
    def get(self):
        if session.get('user_id'):
            recipes = Recipe.query.all()
            return [recipe.to_dict() for recipe in recipes], 200
        else:
            return {'error': 'Must be logged in to view recipes'}, 401
    
    def post(self):
        if not session.get('user_id'):
            return {'error': 'Must be logged in to create recipes'}, 401
        
        json = request.get_json()
        title = json.get('title')
        instructions = json.get('instructions')
        minutes_to_complete = json.get('minutes_to_complete')
        
        try:
            recipe = Recipe(
                title=title,
                instructions=instructions,
                minutes_to_complete=minutes_to_complete,
                user_id=session['user_id']
            )
            
            db.session.add(recipe)
            db.session.commit()
            
            return recipe.to_dict(), 201
        
        except (IntegrityError, ValueError) as e:
            db.session.rollback()
            return {'error': str(e)}, 422

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)