from typing import ClassVar
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models.user import User

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 3 or len(data['name']) > 255:
            flash("Name must be between 3 to 255 characters")
            is_valid = False
        if len(data['description']) < 3 or len(data['description']) > 255:
            flash("Description must be between 3 to 255 characters")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters")
            is_valid = False
        if len(data['date_made']) == 0:
            flash("Please provide a date")
            is_valid = False
        if data.get('under', default=None) == None:
            flash("Please indicate if recipe is under 30 minutes")
            is_valid = False

        return is_valid
    
    @classmethod
    def insert_recipe(self, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s, %(user_id)s);"

        result = connectToMySQL('recipes').query_db(query, data)

        new_recipe_id = result

        return new_recipe_id
    
    @classmethod
    def get_all_recipes(self):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"

        results = connectToMySQL('recipes').query_db(query)

        all_recipes = []

        for item in results:
            recipe = Recipe(item)
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            recipe.user = User(user_data)
            all_recipes.append(recipe)
        
        return all_recipes
    
    @classmethod
    def get_recipe_by_id(self, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"

        # Technically should only be getting one result back
        results = connectToMySQL('recipes').query_db(query, data)

        # Making a new instance of Recipe class
        recipe = Recipe(results[0])

        return recipe
    
    @classmethod
    def update_recipe(self, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under = %(under)s WHERE id = %(id)s;"

        connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def delete_recipe(self, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        connectToMySQL('recipes').query_db(query, data)