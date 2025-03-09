from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API Details
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
    ingredient = request.form['ingredient']
    querystring = {"ingredient": ingredient}
    
    response = requests.get(API_URL, headers=HEADERS, params=querystring)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), response.status_code

@app.route('/search_by_nutrition', methods=['POST'])
def search_by_nutrition():
    protein_min = request.form['protein_min']
    protein_max = request.form['protein_max']
    
    querystring = {
        "protein_in_grams__lt": protein_max,
        "protein_in_grams__gt": protein_min
    }
    
    response = requests.get(API_URL, headers=HEADERS, params=querystring)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
