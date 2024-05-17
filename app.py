from flask import Flask, make_response, render_template, render_template_string, request

from persistence import establishments
from persistence.establishments import EstablishmentsDetails

app = Flask(__name__)

@app.route('/') # when 'methods' is not specified, it defaults to GET, so this function is called when user goes to /
def index():
    establishmentsData = establishments.list_establishments()
    return render_template('index.html', establishments=establishmentsData)

@app.route("/establishments-list", methods=["GET"]) # when user goes to /establishments-list, this function is called
def get_establishments_list():
    establishmentsData = establishments.list_establishments()
    return render_template("establishments_list.html", establishments=establishmentsData)

@app.route("/establishments/<est_id>", methods=["GET"]) # when user goes to /establishments/<est_id> (that is, user selects a establishment), this function is called
def establishment_details(est_id: int):
    establishment = establishments.read(est_id)
    template = "establishment_details_view.html" if not request.args.get("edit") else "establishment_details_form.html"
    return render_template(template, establishment=establishment)

@app.route("/establishments/<est_id>", methods=["POST"]) # when user submits a form in /establishments/<est_id>, this function is called
def create_establishment(est_id: int):
    establishment = EstablishmentsDetails(**request.form)
    establishments.create(establishment)
    return render_template("establishment_details_view.html", establishment=establishment)