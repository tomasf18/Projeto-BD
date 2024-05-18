from flask import Flask, make_response, render_template, render_template_string, request

from persistence import establishments
from persistence.establishments import EstablishmentDetails

app = Flask(__name__) # create a Flask application instance


@app.route('/') # when 'methods' is not specified, it defaults to GET, so this function is called when user goes to /
def index():
    return render_template('index.html')


@app.route('/admin_est')
def admin_est():
    return render_template('admin_est.html')


@app.route("/establishments-list", methods=["GET"]) # when user goes to /establishments-list, this function is called
def get_establishments_list():
    establishmentsData = establishments.list_establishments()
    return render_template("establishments_list.html", establishments=establishmentsData)


@app.route("/establishments/<est_id>", methods=["GET"]) # when user goes to /establishments/<est_id> (that is, user selects a establishment), this function is called
def establishment_details(est_id: int):
    est_id, establishment_details = establishments.read(est_id)
    template = "establishment_details_view.html" if not request.args.get("edit") else "establishment_details_form.html"
    return render_template(template, establishment_id=est_id, establishment=establishment_details)

@app.route("/establishments/<est_id>", methods=["POST"]) 
def update_establishment(est_id: int):
    establishment = EstablishmentDetails(**request.form)
    establishments.update(est_id, establishment)

    response = make_response(render_template_string(f"Establishment {est_id} updated successfully!"))
    response.headers["HX-Trigger"] = "refreshEstablishmentList"

    return response

@app.route("/establishments", methods=["GET"])
def create_establishment_form():
    return render_template("establishment_details_form.html")


@app.route("/establishments", methods=["POST"]) # when user submits a form in /establishments/<est_id>, this function is called
def create_establishment():
    # print(request.form) # uncomment this to see the data in console: ImmutableMultiDict([('specification', 'Barbeiro'), ('zip', '4100-367'), ('locality', 'Ramalde'), ('street', 'Rua O 1º de Janeiro'), ('number', '30'), ('manager_nif', '539287461'), ('manager_init_date', '2020-03-02')])
    new_establishment = EstablishmentDetails(**request.form)
    # print(establishment) # uncomment this to see the data in console: EstablishmentDetails(specification='Barbeiro', zip='4100-367', locality='Ramalde', street='Rua O 1º de Janeiro', number='30', manager_nif='539287461', manager_init_date='2020-03-02')
    new_est_id = establishments.create(new_establishment)

    response = make_response(render_template_string(f"Establishment {new_est_id} created successfully!"))
    response.headers["HX-Trigger"] = "refreshEstablishmentList"

    return response


@app.route("/establishments/<est_id>", methods=["DELETE"])
def delete_establishment(est_id: int):
    try:
        establishments.delete(est_id)

        response = make_response(render_template_string(f"Establishment {est_id} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshEstablishmentList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/search-establishment", methods=["POST"])
def search_establishment():
    local = request.form.get("locality")
    print(local)
    establishmentsData = establishments.list_establishments_by_locality(local)
    return render_template("establishments_list.html", establishments=establishmentsData)



if __name__ == '__main__':
    app.run(debug=True) # start the Flask application in debug mode