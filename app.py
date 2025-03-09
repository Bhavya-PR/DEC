@app.route('/search_by_ingredient', methods=['POST'])
def search_by_ingredient():
    ingredient = request.form['ingredient']
    querystring = {"ingredient": ingredient}

    response = requests.get(API_URL + "find", headers=HEADERS, params=querystring)

    print(response.url)  # ✅ Prints the exact URL called
    print(response.status_code, response.text)  # ✅ Debug API response

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code, "details": response.text}), response.status_code
