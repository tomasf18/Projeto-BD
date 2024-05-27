from flask import Flask, make_response, render_template, render_template_string, request  # type: ignore

from persistence import establishment, schedule, effective, intern, employee, speciality, client, review, contract, person, appointment
from persistence.employee import EmployeeDetails
from persistence.client import ClientDetails
from persistence.establishment import EstablishmentDetails
from persistence.speciality import SpecialitySummary
from persistence.contract import ContractDetails
from persistence.effective import EffectiveDetails
from persistence.intern import InternDetails
from persistence.appointment import AppointmentDetails



app = Flask(__name__) # create a Flask application instance


@app.route('/') # when 'methods' is not specified, it defaults to GET, so this function is called when user goes to /
def index():
    return render_template('index.html')


# ----------------- Admin -----------------


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

@app.route('/admin-sch')
def admin_sch():
    return render_template('admin_sch.html')


# ----------------- Employee -----------------

@app.route('/employee-appointments')
def employee_appointments():
    return render_template('employee_appointments.html')

@app.route('/employee-review')
def employee_review():
    return render_template('employee_review.html')
    


# ----------------- Client -----------------

@app.route('/client-review')
def client_review():
    return render_template('client_review.html')

@app.route('/client-appointments')
def client_appointments():
    return render_template('client_appointments.html')


# ----------------- Employees -----------------


@app.route("/employees-list", methods=["GET"])
def get_employees_list():
    employeesData = employee.list_employees()
    return render_template("employees_list.html", employees=employeesData)


@app.route("/search-employee", methods=["POST"])
def search_employee_by_name():
    name = request.form.get("name")
    employeesData = employee.list_employees_by_name(name)
    return render_template("employees_list.html", employees=employeesData)


@app.route("/employees", methods=["GET"])
def create_employee_form():
    establishment_list = establishment.list_establishments_id_locality()
    schedule_list = schedule.list_schedules()
    speciality_list = speciality.list_specialities()
    return render_template("employee_details_form.html", establishments=establishment_list, schedules=schedule_list, specialities=speciality_list)


@app.route("/employees", methods=["POST"])
def create_employee():
    try:
        nif = request.form.get("nif")
        print(request.form)
        if request.form.get("employee_type") == "E":
            print("Effective")
            contract_details = ContractDetails(request.form.get("nif"), request.form.get("contract_salary"), request.form.get("contract_description"), request.form.get("contract_start_date"), request.form.get("contract_end_date"))
            specialities_list = []
            if request.form.get("specialities_ids"):
                for spc in request.form.getlist("specialities_ids"):
                    if spc != "new":
                        specialities_list.append(spc)
            if request.form.get("new_speciality") != "":
                for spc in request.form.get("new_speciality").split(","):
                    specialities_list.append(spc)

            effective_details = EffectiveDetails(
                fname=request.form.get("fname"),
                lname=request.form.get("lname"),
                zip=request.form.get("zip"),
                locality=request.form.get("locality"),
                street=request.form.get("street"),
                number=request.form.get("number"),
                birth_date=request.form.get("birth_date"),
                sex=request.form.get("sex"),
                establishment_number=request.form.get("establishment_number"),
                schedule_id=request.form.get("schedule_id"),
                private_phone=request.form.get("private_phone"),
                company_phone=request.form.get("company_phone"),
                specialities=specialities_list,
                manager=False,
                contract=contract_details
            )
            effective.create(nif, effective_details)
        else:
            intern_details = InternDetails(
                fname=request.form.get("fname"),
                lname=request.form.get("lname"),
                zip=request.form.get("zip"),
                locality=request.form.get("locality"),
                street=request.form.get("street"),
                number=request.form.get("number"),
                birth_date=request.form.get("birth_date"),
                sex=request.form.get("sex"),
                establishment_number=request.form.get("establishment_number"),
                schedule_id=request.form.get("schedule_id"),
                private_phone=request.form.get("private_phone"),
                company_phone=request.form.get("company_phone"),
                internship_end_date=request.form.get("internship_end_date")
            )
            intern.create(nif, intern_details)
        
        response = make_response(render_template_string(f"Employee {nif} created successfully!"))
        response.headers["HX-Trigger"] = "refreshEmployeesList"
        return response
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response


@app.route("/employees/<emp_num>", methods=["GET"])
def employee_details(emp_num: int):
    isEffective = effective.isEffective(emp_num)
    establishments_list = establishment.list_establishments_id_locality()
    schedules_list = schedule.list_schedules()
    specialities_list = speciality.list_specialities()
    if isEffective:
        emp_nif, emp_num, employee_details = effective.read(emp_num)
        employee_type = "E"
    else:
        emp_nif, emp_num, employee_details = intern.read(emp_num)
        employee_type = "I"
    print(employee_details)
    template = "employee_details_view.html" if not request.args.get("edit") else "employee_details_form.html"
    return render_template(template, employee_nif=emp_nif, employee_number=emp_num, employee=employee_details, emp_type=employee_type, establishments=establishments_list, schedules=schedules_list, specialities=specialities_list) 


@app.route("/employees/<emp_num>", methods=["DELETE"])
def delete_employee(emp_num: int):
    try:
        emp_nif, emp_num, employee_details = employee.read(emp_num)
        employee.delete(emp_nif)

        response = make_response(render_template_string(f"Employee {emp_num} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshEmployeesList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response


@app.route("/employees/<emp_num>", methods=["POST"])
def update_employee(emp_num: int):
    print(request.form)
    emp_nif, emp_num, emp_details = employee.read(emp_num)
    if request.form.get("internship_end_date") == "": 
        contract_details = ContractDetails(emp_nif, request.form.get("contract_salary"), request.form.get("contract_description"), request.form.get("contract_start_date"), request.form.get("contract_end_date"))
        specialities_list = []
        if request.form.get("specialities_ids"):
            for spc in request.form.getlist("specialities_ids"):
                if spc != "new":
                    specialities_list.append(spc)
        if request.form.get("new_speciality") != "":
            for spc in request.form.get("new_speciality").split(","):
                specialities_list.append(spc)

        effective_details = EffectiveDetails(
            fname=request.form.get("fname"),
            lname=request.form.get("lname"),
            zip=request.form.get("zip"),
            locality=request.form.get("locality"),
            street=request.form.get("street"),
            number=request.form.get("number"),
            birth_date=request.form.get("birth_date"),
            sex=request.form.get("sex"),
            establishment_number=request.form.get("establishment_number"),
            schedule_id=request.form.get("schedule_id"),
            private_phone=request.form.get("private_phone"),
            company_phone=request.form.get("company_phone"),
            specialities=specialities_list,
            manager=False,
            contract=contract_details
        )
        effective.update(emp_nif, effective_details)
    else:
        intern_details = InternDetails(
            fname=request.form.get("fname"),
            lname=request.form.get("lname"),
            zip=request.form.get("zip"),
            locality=request.form.get("locality"),
            street=request.form.get("street"),
            number=request.form.get("number"),
            birth_date=request.form.get("birth_date"),
            sex=request.form.get("sex"),
            establishment_number=request.form.get("establishment_number"),
            schedule_id=request.form.get("schedule_id"),
            private_phone=request.form.get("private_phone"),
            company_phone=request.form.get("company_phone"),
            internship_end_date=request.form.get("internship_end_date")
        )
        intern.update(emp_nif, intern_details)

    response = make_response(render_template_string(f"Employee {emp_num} updated successfully!"))
    response.headers["HX-Trigger"] = "refreshEmployeesList"
    return response



@app.route("/employees/<emp_num>/schedule", methods=["GET"])
def employee_schedule(emp_num: int):
    change = True if request.args.get("change") else False
    # print(change)
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
    emp_details = EmployeeDetails(emp_details.fname, emp_details.lname, emp_details.zip, emp_details.locality, emp_details.street, emp_details.number, emp_details.birth_date, emp_details.sex, emp_details.establishment_number, sch_id, emp_details.private_phone, emp_details.company_phone)
    employee.update(emp_nif, emp_details)
    
    response = make_response(render_template_string(f"Employee {emp_num} schedule updated successfully!"))
    response.headers["HX-Trigger"] = "refreshSchedule"

    return response

@app.route("/employees/<emp_num>/contract", methods=["GET", "POST"])
def employee_contract(emp_num: int):
    emp_nif, emp_num, employee_details = effective.read(emp_num)
    contract_details = employee_details.contract
    if request.method == "GET":
        edit = True if request.args.get("edit") else False
        if edit:
            return render_template("contract_details_form.html", contract=contract_details, employee=employee_details, employee_number=emp_num)
        else:
            return render_template("contract_details_view.html", contract=contract_details, employee=employee_details, employee_number=emp_num)
    else:
        salary = request.form.get("salary")
        end_date = request.form.get("end_date")
        description = request.form.get("description")
        new_contract_details = ContractDetails(emp_nif, salary, description, contract_details.start_date, end_date)
        contract.update(new_contract_details)
        return render_template("contract_details_view.html", contract=new_contract_details, employee=employee_details, employee_number=emp_num)
        


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
    try:

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
        response.headers["HX-Trigger"] = "refreshClientsList"
    
        return response
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/clients/<acc_num>", methods=["DELETE"])
def delete_client(acc_num: int):
    try:
        client.delete(acc_num)

        response = make_response(render_template_string(f"Client {acc_num} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshClientsList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/clients", methods=["GET"])
def create_client_form():
    return render_template("client_details_form_create.html")

@app.route("/clients", methods=["POST"])
def create_client():
    try:
        new_client = ClientDetails(**request.form)
        nif = new_client.nif
        new_acc_num = client.create(nif, new_client)

        response = make_response(render_template_string(f"Client {new_acc_num} created successfully!"))
        response.headers["HX-Trigger"] = "refreshClientsList"

        return response
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/search-client", methods=["POST"])
def search_client_by_name():
    name = request.form.get("name")
    clientsData = sorted(client.list_clients_by_name(name))
    return render_template("clients_list.html", clients=clientsData)



# ----------------- Establishments -----------------



@app.route("/establishments-list", methods=["GET"]) # when user goes to /establishments-list, this function is called
def get_establishments_list():
    toSelect = True if request.args.get("select") else False
    establishmentsData = establishment.list_establishments()
    return render_template("establishments_list.html", toSelect=toSelect, establishments=establishmentsData)


@app.route("/establishments/<est_id>", methods=["GET"]) # when user goes to /establishments/<est_id> (that is, user selects a establishment), this function is called
def establishment_details(est_id: int):
    est_id, establishment_details = establishment.read(est_id)
    template = "establishment_details_view.html" if not request.args.get("edit") else "establishment_details_form.html"
    return render_template(template, establishment_id=est_id, establishment=establishment_details)


@app.route("/establishments/<est_id>", methods=["POST"]) 
def update_establishment(est_id: int):
    try:
        establishmentDetails = EstablishmentDetails(**request.form)
        establishment.update(est_id, establishmentDetails)

        response = make_response(render_template_string(f"Establishment {est_id} updated successfully!"))
        response.headers["HX-Trigger"] = "refreshEstablishmentsList"

        return response
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response


@app.route("/establishments", methods=["GET"])
def create_establishment_form():
    return render_template("establishment_details_form.html")


@app.route("/establishments", methods=["POST"]) # when user submits a form in /establishments/<est_id>, this function is called
def create_establishment():
    try:
        # print(request.form) # uncomment this to see the data in console: ImmutableMultiDict([('specification', 'Barbeiro'), ('zip', '4100-367'), ('locality', 'Ramalde'), ('street', 'Rua O 1º de Janeiro'), ('number', '30'), ('manager_nif', '539287461'), ('manager_init_date', '2020-03-02')])
        new_establishment = EstablishmentDetails(**request.form)
        # print(establishment) # uncomment this to see the data in console: EstablishmentDetails(specification='Barbeiro', zip='4100-367', locality='Ramalde', street='Rua O 1º de Janeiro', number='30', manager_nif='539287461', manager_init_date='2020-03-02')
        new_est_id = establishment.create(new_establishment)

        response = make_response(render_template_string(f"Establishment {new_est_id} created successfully!"))
        response.headers["HX-Trigger"] = "refreshEstablishmentsList"

        return response
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response


@app.route("/establishments/<est_id>", methods=["DELETE"])
def delete_establishment(est_id: int):
    try:
        establishment.delete(est_id)

        response = make_response(render_template_string(f"Establishment {est_id} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshEstablishmentsList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/search-establishment", methods=["POST"])
def search_establishment():
    local = request.form.get("locality")
    establishmentsData = establishment.list_establishments_by_locality(local)
    return render_template("establishments_list.html", establishments=establishmentsData)



# ----------------- Schedules -----------------

@app.route("/schedules-list", methods=["GET"]) # when user goes to /schedules-list, this function is called
def get_schedules_list():
    schedulesData = schedule.list_schedules()
    return render_template("schedules_list_admin.html", schedules=schedulesData)

@app.route("/schedule/<sch_id>", methods=["GET"])
def schedule_details(sch_id: int):
    schedule_details = schedule.read(sch_id)
    start_time = schedule_details.start_time.split(":")[0] + ":" + schedule_details.start_time.split(":")[1]
    end_time = schedule_details.end_time.split(":")[0] + ":" + schedule_details.end_time.split(":")[1]
    template = "schedule_details_view_admin.html"
    return render_template(template, schedule_id=sch_id, start_time=start_time, end_time=end_time, schedule=schedule_details)

@app.route("/schedules/<sch_id>", methods=["DELETE"])
def delete_schedule(sch_id: int):
    try:
        schedule.delete(sch_id)

        response = make_response(render_template_string(f"Schedule {sch_id} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshSchedulesList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/search-schedule", methods=["POST"])
def search_schedule():
    day_off = request.form.get("day_off")
    schedulesData = schedule.list_schedules_by_day_off(day_off)
    return render_template("schedules_list_admin.html", schedules=schedulesData)

@app.route("/schedules", methods=["GET"])
def create_schedule_form():
    return render_template("schedule_details_form_admin.html")

@app.route("/schedules", methods=["POST"])
def create_schedule():
    day_off = request.form.get("day_off")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    schedule_id = schedule.create(day_off, start_time, end_time)

    response = make_response(render_template_string(f"Schedule {schedule_id} created successfully!"))
    response.headers["HX-Trigger"] = "refreshSchedulesList"

    return response

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
    response.headers["HX-Trigger"] = "refreshSpecialitiesList"

    return response

@app.route("/specialities/<spc_designation>", methods=["DELETE"])
def delete_speciality(spc_designation: str):
    try:
        speciality.delete(spc_designation)

        response = make_response(render_template_string(f"Speciality {spc_designation} deleted successfully!"))
        response.headers["HX-Trigger"] = "refreshSpecialitiesList"
        
        return response
    
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response

@app.route("/search-speciality", methods=["POST"])
def search_speciality():
    designation = request.form.get("designation")
    specialitiesData = speciality.list_specialities_by_designation(designation)
    return render_template("specialities_list.html", specialities=specialitiesData)


# ----------------- ReviewsEmployee -----------------

@app.route("/search-review-emp-num", methods=["POST"])
def search_review_employee_by_nif():
    func_num = request.form.get("num")
    employee_reviews = review.list_reviews_by_num_emp(func_num)
    average_rating = review.average_rating_by_num_emp(func_num)
    performance = review.performance_by_num_emp(func_num)
    return render_template("employee_reviews_list.html", reviews=employee_reviews, average_rating=average_rating, performance=performance)

@app.route("/reviews", methods=["GET"])
def get_reviews():
    nif_emp = request.args.get('nif_emp', type=int)
    nif_cli = request.args.get('nif_cli', type=int)
    date = request.args.get('date', type=str)
    reviewDetails = review.read(nif_emp, nif_cli, date)
    return render_template("review_details_view.html", review=reviewDetails)


# ----------------- AppointmentsEmployee -----------------

@app.route("/search-appointments-emp-num", methods=["POST"])
def search_appointments_employee_by_nif():
    func_number = request.form.get("num")
    employee_appointments = appointment.list_appointments_by_acc_emp(func_number, 'nif')
    return render_template("employee_appointments_list.html", appointments=employee_appointments)

@app.route("/appointments", methods=["GET"])
def get_appointments():
    nif_emp = request.args.get('nif_emp', type=int)
    nif_cli = request.args.get('nif_cli', type=int)
    date = request.args.get('date', type=str)
    hour = request.args.get('hour', type=str)
    appointmentDetails = appointment.read(nif_emp, nif_cli, date, hour)
    return render_template("appointment_details_view_employee.html", appointment=appointmentDetails)


# ----------------- ReviewsClient -----------------

@app.route("/employees-list-client", methods=["GET"])
def get_employees_list_client():
    employeesData = employee.list_employees()
    return render_template("employees_list_client.html", employees=employeesData)

@app.route("/search-employee-client", methods=["POST"])
def search_employee_by_name_client():
    name = request.form.get("name")
    employeesData = employee.list_employees_by_name(name)
    return render_template("employees_list_client.html", employees=employeesData)

@app.route("/employees/<emp_num>/client", methods=["GET"])
def employee_details_client(emp_num: int):
    isEffective = effective.isEffective(emp_num)
    if isEffective:
        emp_nif, emp_num, employee_details = effective.read(emp_num)
        employee_type = "E"
    else:
        emp_nif, emp_num, employee_details = intern.read(emp_num)
        employee_type = "I"

    template = "employee_details_view_client.html" if not request.args.get("review") else "review_details_form_client.html"
    return render_template(template, employee_nif=emp_nif, employee_number=emp_num, employee=employee_details, emp_type=employee_type)

@app.route("/review/<emp_nif>", methods=["POST"])
def create_review(emp_nif: int):
    try:
        cli_acc = request.form.get("cli_acc")
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        review.create(emp_nif, cli_acc, rating, comment)

        response = make_response(render_template_string(f"Review for employee {emp_nif} created successfully!"))
        response.headers["HX-Trigger"] = "refreshEmployeesList"

        return response
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response
    

# ----------------- AppointmentsClient -----------------

@app.route("/search-appointments-cli-acc", methods=["POST"])
def search_appointments_client_by_acc():
    cli_acc = request.form.get("acc")
    client_appointments = appointment.list_appointments_by_acc_cli(cli_acc)
    return render_template("client_appointments_list.html", appointments=client_appointments)

@app.route("/create-appointments", methods=["GET"])
def create_appointment_form():
    establishment_list = establishment.list_establishments_id_locality()
    return render_template("appointment_details_form_client.html", establishments=establishment_list)

@app.route("/create-appointments", methods=["POST"])
def create_appointment():
    try:
        nif_emp = request.form.get("nif_emp")
        nif_cli = request.form.get("nif_cli")
        date = request.form.get("date")
        hour = request.form.get("hour")
        appointment.create(nif_emp, nif_cli, date, hour)

        response = make_response(render_template_string(f"Appointment for employee {nif_emp} and client {nif_cli} created successfully!"))
        response.headers["HX-Trigger"] = "refreshEmployeesList"

        return response
    except Exception as e:
        response = make_response(render_template_string(f"{e}"))
        return response
    
@app.route("/get_employees_by_establishment", methods=["GET"])
def get_employees_by_establishment():
    num_estabelecimento = request.args.get('establishment_number')
    if num_estabelecimento is not None:
        num_estabelecimento = int(num_estabelecimento)
        employees = employee.list_employees_by_establishment(num_estabelecimento)
        services = [] # fazer depois !!!!!!!!
        return render_template('employees_list_by_establishment.html', employees=employees, services=services)
    else:
        return render_template('employees_list_by_establishment.html', employees=[], services=[])


if __name__ == '__main__':
    app.run(debug=True) # start the Flask application in debug mode