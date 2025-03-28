from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://keto-diet.p.rapidapi.com/"
API_KEY = "db8b36227cmsh36904c604d3a623p128502jsn3760ceaa8a89"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "keto-diet.p.rapidapi.com"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/findrecipe_ingre')
def findrecipe_ingre():
    return render_template('findrecipe_ingre.html')

@app.route('/findrecipe_nutri')
def findrecipe_nutri():
    return render_template('findrecipe_nutri.html')

@app.route('/search_by_ingredient', methods=['POST'])
def search_by_ingredient():
    ingredient = request.form['ingredient'].lower()  
    querystring = {}  

    response = requests.get(API_URL, headers=HEADERS, params=querystring)

    if response.status_code == 200:
        all_recipes = response.json()
        
        filtered_recipes = []
        for recipe in all_recipes:
            for key, value in recipe.items():
                if key.startswith("ingredient_") and value:  
                    if ingredient in value.lower():  
                        filtered_recipes.append(recipe)
                        break  
        
        return jsonify(filtered_recipes)
    else:
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), response.status_code

@app.route('/search_by_nutrition', methods=['POST'])
def search_by_nutrition():
    protein_min = float(request.form['protein_min'])  
    protein_max = float(request.form['protein_max'])

    response = requests.get(API_URL, headers=HEADERS)
    
    if response.status_code == 200:
        all_recipes = response.json()

        filtered_recipes = [
            recipe for recipe in all_recipes
            if "protein_in_grams" in recipe and isinstance(recipe["protein_in_grams"], (int, float))
            and protein_min <= recipe["protein_in_grams"] <= protein_max
        ]

        print("Filtered Recipes:", filtered_recipes)  

        return jsonify(filtered_recipes)
    else:
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
