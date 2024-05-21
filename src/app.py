from flask import Flask, make_response, render_template, render_template_string, request

from persistence import establishment, schedule, effective, intern, employee, speciality, client
from persistence.employee import EmployeeDetails
from persistence.client import ClientDetails
from persistence.establishment import EstablishmentDetails
from persistence.speciality import SpecialitySummary


app = Flask(__name__) # create a Flask application instance


@app.route('/') # when 'methods' is not specified, it defaults to GET, so this function is called when user goes to /
def index():
    return render_template('index.html')


@app.route('/admin-emp')
def admin_emp():
    return render_template('admin_emp.html')

@app.route('/admin-cli')
def admin_cli():
    return render_template('admin_cli.html')

@app.route('/admin-est')
def admin_est():
    return render_template('admin_est.html')

@app.route('/admin-spc')
def admin_spc():
    return render_template('admin_spc.html')



# ----------------- Employees -----------------



@app.route("/employees-list", methods=["GET"])
def get_employees_list():
    effective_employeesData = effective.list_effectives()
    intern_employeesData = intern.list_interns()
    employeesData = sorted(effective_employeesData + intern_employeesData)
    return render_template("employees_list.html", employees=employeesData)


@app.route("/employees/<emp_num>", methods=["GET"])
def employee_details(emp_num: int):
    isEffective = effective.isEffective(emp_num)
    if isEffective:
        emp_nif, emp_num, employee_details = effective.read(emp_num)
        employee_type = "E"
    else:
        emp_nif, emp_num, employee_details = intern.read(emp_num)
        employee_type = "I"

    template = "employee_details_view.html" if not request.args.get("edit") else "employee_details_form.html"
    return render_template(template, employee_nif=emp_nif, employee_number=emp_num, employee=employee_details, emp_type=employee_type) 


@app.route("/employees/<emp_num>/schedule", methods=["GET"])
def employee_schedule(emp_num: int):
    change = True if request.args.get("change") else False
    print(change)
    if change:
        schedules_list = schedule.list_schedules()
        return render_template("schedules_list.html", sch_change=True, employee_number=emp_num, schedules=schedules_list)
    else:
        schedule_details = schedule.get_schedule_of_emp(emp_num)
        start_time = schedule_details.start_time.split(":")[0] + ":" + schedule_details.start_time.split(":")[1]
        end_time = schedule_details.end_time.split(":")[0] + ":" + schedule_details.end_time.split(":")[1]
        day_off = schedule_details.day_off
        return render_template("schedule_details_view.html", schedule_id=schedule_details.id, start_time=start_time, end_time=end_time, day_off=day_off, employee_number=emp_num)
    

@app.route("/employees/<emp_num>/schedule/<sch_id>", methods=["PUT"])
def update_schedule(emp_num: int, sch_id: int):
    emp_nif, emp_num, emp_details = employee.read(emp_num)
    emp_details = EmployeeDetails(emp_details.fname, emp_details.lname, emp_details.zip, emp_details.locality, emp_details.street, emp_details.number, emp_details.birth_date, emp_details.sex, emp_details.establishment_number, sch_id)
    employee.update(emp_nif, emp_details)
    
    response = make_response(render_template_string(f"Employee {emp_num} schedule updated successfully!"))
    response.headers["HX-Trigger"] = "refreshSchedule"

    return response


@app.route("/search-employee", methods=["POST"])
def search_employee_by_name():
    name = request.form.get("name")
    effective_employeesData = effective.list_effectives_by_name(name)
    intern_employeesData = intern.list_interns_by_name(name)
    employeesData = sorted(effective_employeesData + intern_employeesData)
    return render_template("employees_list.html", employees=employeesData)



# ----------------- Clients -----------------



@app.route("/clients-list", methods=["GET"])
def get_clients_list():
    clientsData = sorted(client.list_clients())
    return render_template("clients_list.html", clients=clientsData)

@app.route("/clients/<acc_num>", methods=["GET"])
def client_details(acc_num: int):
    nif, acc_num, client_details = client.read(acc_num)
    template = "client_details_view.html" if not request.args.get("edit") else "client_details_form.html"
    return render_template(template, client_nif=nif, account_number=acc_num, client=client_details)

@app.route("/clients/<nif>", methods=["POST"])
def update_client(nif: int):

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    zip_code = request.form.get("zip")
    locality = request.form.get("locality")
    street = request.form.get("street")
    number = request.form.get("number")
    birth_date = request.form.get("birth_date")
    sex = request.form.get("sex")
    phone_number = request.form.get("phone_number")

    client_details = ClientDetails(
        nif=nif,  # Include nif from the route URL
        fname=fname,
        lname=lname,
        zip=zip_code,
        locality=locality,
        street=street,
        number=number,
        birth_date=birth_date,
        sex=sex,
        phone_number=phone_number
    )
    client.update(nif, client_details)

    response = make_response(render_template_string(f"Client {nif} updated successfully!"))
    response.headers["HX-Trigger"] = "refreshClientList"

    return response

@app.route("/clients/<acc_num>", methods=["DELETE"])
def delete_client(acc_num: int):
    try:
        client.delete(acc_num)

        response = make_response(render_template_string(f"Client {acc_num} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshClientList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/clients", methods=["GET"])
def create_client_form():
    return render_template("client_details_form_create.html")

@app.route("/clients", methods=["POST"])
def create_client():
    new_client = ClientDetails(**request.form)
    nif = new_client.nif
    new_acc_num = client.create(nif, new_client)

    response = make_response(render_template_string(f"Client {new_acc_num} created successfully!"))
    response.headers["HX-Trigger"] = "refreshClientList"

    return response

@app.route("/search-client", methods=["POST"])
def search_client_by_name():
    name = request.form.get("name")
    clientsData = sorted(client.list_clients_by_name(name))
    return render_template("clients_list.html", clients=clientsData)



# ----------------- Establishments -----------------



@app.route("/establishments-list", methods=["GET"]) # when user goes to /establishments-list, this function is called
def get_establishments_list():
    establishmentsData = establishment.list_establishments()
    return render_template("establishments_list.html", establishments=establishmentsData)


@app.route("/establishments/<est_id>", methods=["GET"]) # when user goes to /establishments/<est_id> (that is, user selects a establishment), this function is called
def establishment_details(est_id: int):
    est_id, establishment_details = establishment.read(est_id)
    template = "establishment_details_view.html" if not request.args.get("edit") else "establishment_details_form.html"
    return render_template(template, establishment_id=est_id, establishment=establishment_details)


@app.route("/establishments/<est_id>", methods=["POST"]) 
def update_establishment(est_id: int):
    establishment = EstablishmentDetails(**request.form)
    establishment.update(est_id, establishment)

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
    new_est_id = establishment.create(new_establishment)

    response = make_response(render_template_string(f"Establishment {new_est_id} created successfully!"))
    response.headers["HX-Trigger"] = "refreshEstablishmentList"

    return response


@app.route("/establishments/<est_id>", methods=["DELETE"])
def delete_establishment(est_id: int):
    try:
        establishment.delete(est_id)

        response = make_response(render_template_string(f"Establishment {est_id} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshEstablishmentList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/search-establishment", methods=["POST"])
def search_establishment():
    local = request.form.get("locality")
    establishmentsData = establishment.list_establishments_by_locality(local)
    return render_template("establishments_list.html", establishments=establishmentsData)



# ----------------- Specialities -----------------



@app.route("/specialities-list", methods=["GET"]) # when user goes to /specialities-list, this function is called
def get_specialities_list():
    specialitiesData = speciality.list_specialities()
    return render_template("specialities_list.html", specialities=specialitiesData)

@app.route("/specialities", methods=["GET"])
def create_speciality_form():
    return render_template("speciality_details_form.html")

@app.route("/specialities", methods=["POST"])
def create_speciality():
    speciality_designation = request.form.get("designation")
    speciality.create(SpecialitySummary(speciality_designation))

    response = make_response(render_template_string(f"Speciality {speciality_designation} created successfully!"))
    response.headers["HX-Trigger"] = "refreshSpecialityList"

    return response

@app.route("/specialities/<spc_designation>", methods=["DELETE"])
def delete_speciality(spc_designation: str):
    try:
        speciality.delete(spc_designation)

        response = make_response(render_template_string(f"Speciality {spc_designation} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshSpecialityList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/search-speciality", methods=["POST"])
def search_speciality():
    designation = request.form.get("designation")
    specialitiesData = speciality.list_specialities_by_designation(designation)
    return render_template("specialities_list.html", specialities=specialitiesData)

if __name__ == '__main__':
    app.run(debug=True) # start the Flask application in debug mode