from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validate_registration(data):
        name_regex = re.compile(r"^[A-Za-z- ']{1,50}$")
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{1,50}$")
        password_regex = re.compile(r"^\S{8,255}$")

        is_valid = True
        new_user = User.get_users_by_email(data)

        # Checking that inputs are valid
        if not name_regex.match(data['first_name']):
            flash("First name must be between 1 to 50 characters")
            is_valid = False
        if not name_regex.match(data['last_name']):
            flash("Last name must be between 1 to 50 characters")
            is_valid = False
        if not email_regex.match(data['email']):
            flash("Invalid email")
            is_valid = False
        if not password_regex.match(data['password']):
            flash("Invalid password")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match")
            is_valid = False

        # Checking to see if email is unique
        if len(new_user) != 0:
            flash("Email already taken")
            is_valid = False

        return is_valid
    
    @classmethod
    def insert_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"

        new_user_id = connectToMySQL('recipes').query_db(query, data)

        return new_user_id
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"

        results = connectToMySQL('recipes').query_db(query)

        all_users = []

        for item in results:
            all_users.append(User(item))
        
        return all_users

    @classmethod
    def get_users_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        # Result should really be only returning ONE item but by returning users as a LIST, it will check if there is ONE or ZERO results without returning an error (as opposed to if I were to assign 'user = User(result[0])'
        results = connectToMySQL('recipes').query_db(query, data)

        users = []

        for item in results:
            users.append(User(item))

        return users
