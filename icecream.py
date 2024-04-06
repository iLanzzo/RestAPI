from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data - list of ice creams
icecreams = [
    {'id': 1, 'flavor': 'Strawberry', 'milky': False},
    {'id': 2, 'flavor': 'Vanilla', 'milky': True},
    {'id': 3, 'flavor': 'Chocolate', 'milky': True}
]

# Function to generate a unique ID for new ice cream entries
def generate_id():
    return max(ice['id'] for ice in icecreams) + 1

@app.route("/")
def home():
    icecream_flavors = [f"Icecream flavor: {icecream['flavor']}" for icecream in icecreams]
    return jsonify(icecream_flavors), 200

@app.route("/id")
def get_id():
    icecream_id = [f"Icecream ID: {icecream['id']} is {icecream['flavor']}" for icecream in icecreams]
    return jsonify(icecream_id), 200

# Define kosher & not kosher
def get_kosher():
    kosher = []
    not_kosher = []
    for icecream in icecreams:
        if icecream['milky'] == False:
            kosher.append(icecream)
        else:
            not_kosher.append(icecream)
    return {'kosher': kosher, 'not_kosher': not_kosher}

@app.route("/kosher")
def kosher():
    return jsonify(get_kosher()['kosher']), 200

@app.route("/notkosher")
def not_kosher():
    return jsonify(get_kosher()['not_kosher']), 200

@app.route("/<int:icecream_id>", methods=["GET"])
def get_icecream_by_id(icecream_id):
    for icecream in icecreams:
        if icecream['id'] == icecream_id:
            return jsonify(icecream), 200
    return jsonify({'error': 'Ice cream not found'}), 404

# POST method
@app.route("/new", methods=["POST"])
def add_icecream():
    data = request.get_json()
    if "flavor" not in data or "milky" not in data:
        return jsonify({"error": "Missing flavor or milky request"}), 400

    new_icecream = {
        "id": generate_id(),
        "flavor": data["flavor"],
        "milky": data["milky"]
    }
    icecreams.append(new_icecream)
    return jsonify(data), 201

# PUT method
@app.route("/<int:icecream_id>", methods=["PUT"])
def update_icecream(icecream_id):
    data = request.json
    for icecream in icecreams:
        if icecream['id'] == icecream_id:
            if 'flavor' in data:
                icecream['flavor'] = data['flavor']
            if 'milky' in data:
                icecream['milky'] = data['milky']
            return jsonify(icecreams), 200  # Return the updated list of ice creams
    return jsonify({'error': 'Ice cream not found'}), 404

# DELETE method
@app.route("/icecream/<int:icecream_id>", methods=["DELETE"])
def delete_icecream(icecream_id):
    global icecreams
    icecreams = [ice for ice in icecreams if ice['id'] != icecream_id]
    return jsonify({'message': 'Ice cream deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)