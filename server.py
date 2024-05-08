"""A simple Flask app to demonstrate the use of make_response and error handling."""

from flask import Flask, make_response, request
app = Flask(__name__)
data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]


@app.route("/")
def index():
    """Return a friendly HTTP greeting."""
    return "hello world"

@app.route("/no_content")
def no_content():
    """Return a no content response. with status code 204"""
    return "", 204

@app.route("/exp")
def index_explicit():
    """Uses make_response to return 'Hello World!' with a 200 status code"""
    resp = make_response('Hello World!')
    resp.status_code = 200
    return resp

@app.route("/data")
def get_data():
    """Return the data as JSON"""
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

@app.route("/name_search")
def name_search():
    """find a person in the database
        Returns:
        json: person if found, with status of 200
        404: if not found
        422: if argument q is missing
    """
    q = request.args.get('q')
    if not q:
        return {"message": "Invalid input parameter"}, 422

    for person in data:
        if q.lower()  in person['first_name'].lower():
            return person, 200

    return {"message": "Person not found"}, 404

@app.get("/count")
def count():
    """Return the count of data"""
    try:
        return {"data count": len(data)}
    except NameError:
        return {"message": "Data not found"}, 404
    
@app.route("/person/<uuid>")
def find_by_uuid(uuid):
    """find a person in the database
        Returns:
        json: person if found, with status of 200
        404: if not found
    """
    for person in data:
        if person['id'] == str(uuid):
            return person, 200

    return {"message": "Person not found"}, 404

@app.route("/person/<uuid>", methods=["DELETE"])
def delete_by_uuid(uuid):
    """Delete a person in the database
        Returns:
        json: person if found, with status of 200
        404: if not found
    """
    for person in data:
        if person['id'] == str(uuid):
            data.remove(person)
            return {"message":f'User with id: {person["id"]} sucessfully deleted.'}, 200

    return {"message": "Person not found"}, 404

@app.route("/person/<uuid>", methods=["POST"])
def add_by_uuid(uuid):
    """Add a person in the database
        Returns:
        json: person if found, with status of 200
        404: if not found
    """
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
        # Validate the input data
    if not new_person.get('first_name') or not new_person.get('last_name'):
        return {"message": "Invalid input parameter"}, 422
    for person in data:
        if person['id'] == str(uuid):
            return {"message": "Person already exists"}, 400
    try:
        data.append(new_person)
        return {"message": "Person added"}, 200
    except NameError:
        return {"message": "Error adding person"}, 500

# Create update_by_uuid route here
@app.route("/person/<uuid>", methods=["PUT"])
def update_by_uuid(uuid):
    """Update a person in the database
        Returns:
        json: person if found, with status of 200
        404: if not found
    """
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
        # Validate the input data
    if not new_person.get('first_name') or not new_person.get('last_name'):
        return {"message": "Invalid input parameter"}, 422
    for person in data:
        if person['id'] == str(uuid):
            person.update(new_person)
            return {"message": "Person updated"}, 200

    return {"message": "Person not found"}, 404



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return {"message": "Page not found"}, 404
