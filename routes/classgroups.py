from flask import Blueprint, jsonify, request, render_template, redirect, url_for  # Blueprint: groups related routes, jsonify: converts python data to JSON HTTP responses,request: gives access to incoming HTTP request data, render template: to view html page. 
from extensions import db                      # db: SQLAlchemy database instance. 
from models import ClassGroup                  # model representing a class group(e.g. 2-6, Teens).

# These imports connect Flask's routing tools, my database layer, and the 
# ClassGroup model, so this file can act as the dedicated API surfaace for class group operations. 

classgroups_bp = Blueprint('classgroups', __name__)   # Creates a blueprint named "classgroups"

# GET all class groups.

# List all Class Groups for HTML page view.
@classgroups_bp.route('/classes/view')
def classes():
    groups = ClassGroup.query.all()
    return render_template('classes.html', groups=groups)

# Existing API route.
@classgroups_bp.route("/classgroups", methods=["GET"]) # route.
def get_classgroups():
    groups = ClassGroup.query.all()                    # fetches all class groups from the database. 
    return jsonify([g.to_dict() for g in groups])      # coverts each model instance into a serializable dict.

# New frontend route.
@classgroups_bp.route("/classes", methods=["GET"])
def index():
    groups = ClassGroup.query.all()
    return jsonify([g.to_dict() for g in groups])

# POST create class group.

# For HTML view.
@classgroups_bp.route("/classgroups/create", methods=["POST"])
def create_classgroup_html():
    data = request.form
    group = ClassGroup(name=data["name"])
    db.session.add(group)
    db.session.commit()
    return redirect(url_for('classgroups.classes'))

# For API testing. 
@classgroups_bp.route("/classgroups", methods=["POST"]) # route. 
def create_classgroup_api():
    data = request.json                                 # reads the JSON body sent by the client. 
    group = ClassGroup(name=data["name"])               # creates a new class group using the provided name. 
    db.session.add(group)                               # db.session.add(...) + db.session.commit(): persists the new group to the database. 
    db.session.commit() 
    return jsonify(group.to_dict()), 201                # returns the created group as JSON with status code 201(created).                      

# GET single class group.
@classgroups_bp.route("/classgroups/<int:id>", methods=["GET"]) # route, "<int:id>": URL parameter capturing the class group's ID as an integer.
def get_classgroup(id):
    group = ClassGroup.query.get_or_404(id)                     # "get_or_404(id)": fethces the group by ID, if noto found automatically returns a 404 response. 
    return jsonify(group.to_dict())                             # JSON representation of the specific class group.

# DELETE class group.
@classgroups_bp.route("/classgroups/<int:id>", methods=["DELETE"]) # route.
def delete_classgroup(id):
    group = ClassGroup.query.get_or_404(id)                        # ensures we only attempt to delte an existing group.
    db.session.delete(group)                                       # marks the object for deletion.
    db.session.commit()                                             # applies the deletion to the database.
    return jsonify({"message": "Deleted"})                         # Simple JSON confirmation message.