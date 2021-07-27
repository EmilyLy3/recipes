from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to view this page")
        return redirect('/')

    recipes = Recipe.get_all_recipes()

    return render_template('dashboard.html', recipes = recipes)


@app.route('/recipes/new')
def add_new_recipe():
    return render_template('add_new_recipe.html')


@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    # validate data first
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under': request.form['under'],
        'user_id': session['user_id']
    }

    # insert data into database
    Recipe.insert_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def view_instructions(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('view_instructions.html', recipe = recipe)

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }

    recipe = Recipe.get_recipe_by_id(data)
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/update_recipe/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
        # return redirect(f'/recipes/edit/{recipe_id}')

    data = {
        'id': recipe_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under': request.form['under'],
    }

    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }

    Recipe.delete_recipe(data)
    return redirect('/dashboard')