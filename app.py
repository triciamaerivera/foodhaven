from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import unquote
import datetime
import random

app = Flask(__name__)

# 1af25e77af284f1c82c2350f7f373935


# Spoonacular API Key
API_KEY = '1af25e77af284f1c82c2350f7f373935'



# Sample list of meal types
MEAL_TYPES = ["breakfast", "lunch", "dinner"]

def get_random_recipes(meal_type, calories):
    url = f"https://api.spoonacular.com/recipes/random?apiKey={API_KEY}&number=1&type={meal_type}&maxCalories={calories}"
    response = requests.get(url)
    data = response.json()
    return data['recipes'][0]

@app.route('/meal_plan', methods=['GET', 'POST'])
def meal_plan():
    meal_plan = {}
    
    if request.method == 'POST':
        preferred_calories = request.form.get('calories')
        for meal_type in MEAL_TYPES:
            meal_plan[meal_type] = get_random_recipes(meal_type, preferred_calories)
    else:
        preferred_calories = None
    
    return render_template('meal-plan.html', meal_plan=meal_plan, preferred_calories=preferred_calories)




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If a search form is submitted
        query = request.form.get('search_query', '')
        
        # Perform a search from the query given
        recipes = search_recipes(query)
        return render_template('index.html', recipes=recipes, search_query=query)
    
    # If no form submitted
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    
    # Search for recipe with the decoded version of seach query
    recipes = search_recipes(decoded_search_query)
    
    print("Debug: Recipes:", recipes)
    return render_template('index.html', recipes=recipes, search_query=decoded_search_query)


# Function for search query
def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query' : query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation' : True,
        'fillIngredients': True,
        'includeNutrition': True,
    }
    
    # Send GET request to Spoonacular
    response = requests.get(url, params=params)
    
    # If API call is successful
    if response.status_code == 200:
        data = response.json()
        # Return the list of recipe results
        return data['results']
    
    # If not successful
    return []

# View a specific recipe
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Get the search query
    search_query = request.args.get('search_query', '')
    
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey' : API_KEY,
    }
    
    # Get the recipe info from the API
    response = requests.get(url, params=params)
    
    # If succesful
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query= search_query)
    return "Recipe not found", 404




if __name__ == '__main__':
    app.run(debug=True)
    
    