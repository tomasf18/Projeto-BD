# Database Project - StylistData - Help document


## Commands order for running an applications
1. `poetry install`
2. `poetry shell`
3. `flask run --debug`   

## Better undarstanding of GET and POST

```txt
For better understanding of GET and POST, observe the request data on terminal when trying to press a button or insert data:  
127.0.0.1 - - [15/May/2024 21:45:15] "GET /establishments/2 HTTP/1.1" 404 -
127.0.0.1 - - [15/May/2024 21:46:11] "GET /establishments HTTP/1.1" 404 -
127.0.0.1 - - [15/May/2024 21:46:11] "GET /establishments HTTP/1.1" 404 -
127.0.0.1 - - [15/May/2024 21:46:12] "GET /establishments HTTP/1.1" 404 -
127.0.0.1 - - [15/May/2024 21:46:12] "GET /establishments HTTP/1.1" 404 -
127.0.0.1 - - [15/May/2024 21:46:37] "GET /establishments/4 HTTP/1.1" 404 -
```

## Named Tuples

```txt
Named Tuples are immutable, that is, it is not possible to change the values ​​of attributes after instantiation, it is as if they were objects
of a class with read-only attributes. We will create named tuples as we need. For example, to represent
a customer, we can create a named tuple called Customer, with the attributes id, name, email and phone. But we might want a div
where the customer elements that appear there are the id, name and email. In this case, we can create a named tuple called
CustomerSummary, which has the attributes id, name and email. So, we can create named tuples with whatever attributes we want, according to
with the needs of our program.
```


## Externally Visible Server

If you run the server you will notice that the server is only accessible from your own computer, not from any other in the network. 
This is the default because in debugging mode a user of the application can execute arbitrary Python code on your computer.
If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding --host=0.0.0.0 to the command line:

```powershell
    $ flask run --host=0.0.0.0
```

This tells your operating system to listen on all public IPs.


## Routing

Modern web applications use meaningful URLs to help users. Users are more likely to like a page and come back if the page uses a meaningful 
URL they can remember and use to directly visit a page. 
Use the `route()` decorator to bind a function to a URL.

```python
    @app.route('/')
    def index():
        return 'Index Page'

    @app.route('/hello')
    def hello():
        return 'Hello, World'
```

You can make parts of the URL dynamic and attach multiple rules to a function.

```python
    @app.route('/user/<username>')
    def show_user_profile(username):
        # show the user profile for that user (that is, we have the directory 'user' that have tons of files, each one is a user profile)
        return f'User {username}
```


### HTTP Methods

Web applications use different HTTP methods when accessing URLs. You should familiarize yourself with the HTTP methods as you work with Flask. By default, a route only answers to `GET` requests.  
You can use the methods argument of the `route()` decorator to handle different HTTP methods.

```python
    from flask import request

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            return do_the_login()
        else:
            return show_the_login_form()
```

The example above keeps all methods for the route within one function, which can be useful if each part uses some common data.

You can also separate views for different methods into different functions. Flask provides a shortcut for decorating such routes with get(), post(), etc. for each common HTTP method.

```python
    @app.route('/login', methods=['GET'])
    def login_get():
        return show_the_login_form()

    @app.route('/login', methods=['POST'])
    def login_post():
        return do_the_login()
```

1. `@app.route('/login', methods=['GET'])`: This line is a decorator in Python. It tells Flask to associate the function 
login_get() with the URL /login and only respond to HTTP GET requests. **So when a user visits the `/login` URL in their web browser, 
Flask will call the `login_get()` function.**

2. `def login_get():`: This is the definition of the `login_get()` function. **It's a Python function that will be executed when the 
`/login` URL is requested using the GET method**.

3. `return show_the_login_form()`: Inside the `login_get()` function, this line returns the result of calling another function 
named `show_the_login_form()`. Presumably, `show_the_login_form()` is a separate function defined elsewhere in the code that 
generates and displays the login form to the user (html page).

4. `@app.route('/login', methods=['POST'])`: Similar to the first line, this line is also a decorator. It associates the function 
`login_post()` with the URL `/login`, but this time it responds only to HTTP POST requests. So when a user submits a form with the 
action set to `/login` using the POST method, Flask will call the `login_post()` function.

5. `def login_post():`: This is the definition of the `login_post()` function. It's a Python function that will be executed when 
the `/login` URL is requested using the POST method.

6. `return do_the_login()`: Inside the `login_post()` function, this line returns the result of calling another function named 
`do_the_login()`. Presumably, `do_the_login()` is a separate function defined elsewhere in the code that handles the actual 
login process, such as verifying the user's credentials and creating a session.

So, in summary, this code sets up two routes for the `/login` URL: 
    - one for handling GET requests (`login_get()`) to display the login form;
    - another for handling POST requests (`login_post()`) to process the submitted login credentials.


## Rendering Templates

Generating HTML from within Python is not fun.  
Templates can be used to generate any type of text file. For web applications, you’ll primarily be generating HTML pages, 
but you can also generate markdown, plain text for emails, and anything else.  

To render a template you can use the **`render_template()`** method. All you have to do is **provide the name of the template 
and the variables you want to pass to the template engine** as keyword arguments. Here’s a simple example of how to render a template:

```python
    from flask import render_template

    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)
```

Flask will look for templates in the **`templates`** `folder`. So if your application is a module, this folder is next to that module, 
if it’s a package it’s actually inside your package:

```txt
/application.py
/templates
    /hello.html
```

Here is an example template:
```html
    <!doctype html>
    <title>Hello from Flask</title>
    {% if name %}
    <h1>Hello {{ name }}!</h1>  
    {% else %}
    <h1>Hello, World!</h1>
    {% endif %}
```

### Head over to the official Jinja2 Template Documentation for more information on templates: [Jinja2 - Templates](https://jinja.palletsprojects.com/templates/)

# Important (using teacher's python example in class 7)

index.html
```html
<div class="contact-list" hx-get="/contact-list" hx-trigger="refreshContactList from:body">
    <!-- trigger means that when the HTTPS solicitation reply contains "refreshContactList" in its body, 
    that will trigger an data update in this div without having to reload the website -->
    {% include "contact_list.html" %}
</div>
```

Everytime there is a HTTP that triggers that hx, there will be a GET request for /contact-list endpoint. 
This means that the following function whill be called when it happens:

app.py
```python
# when user goes to /establishments-list, this function is called
@app.route("/contact-list", methods=["GET"])
def contact_list():
    contacts = customers.list_all()
    return render_template("contact_list.html", customers=contacts)
```

Now, where will this list be loaded to?

client_list.html
```html 
{% for customer in customers %}
    <div class="contact-list-item" hx-swap="innerHTML" hx-target="#content">
        <div class="contact-list-item-details" hx-get="/customers/{{ customer.id }}">
            <div class="contact-name">{{ customer.contact_name }}</div>
            <div class="company-name">{{ customer.company_name }}</div>
        </div>
        <div>
            <button class="edit-button" hx-get="/customers/{{ customer.id }}?edit=true">Edit</button>
            <button class="delete-button" hx-delete="/customers/{{ customer.id }}" hx-confirm="Are you sure?">Delete</button>
        </div>
    </div>
{% endfor %}  
```

index.html
```html
<div id="content" class="right-column"></div>
```

As you can see in the following explanation, the DOM is very important:

In the code provided, we have two important attributes from the HTMX library: `hx-swap` and `hx-target`. These attributes are used to control how content is updated on the page when an HTMX request is made.

### `hx-swap`

The `hx-swap` attribute specifies how the content returned by the HTMX request should be inserted into the DOM. In your code, `hx-swap` is set to `innerHTML`:

```html
<div class="contact-list-item" hx-swap="innerHTML" hx-target="#content">
```

Here, `hx-swap="innerHTML"` means that the content returned from the request will replace the inner content (inner HTML) of the target element. There are different values that `hx-swap` can have, such as `outerHTML`, `beforebegin`, `afterbegin`, `beforeend`, and `afterend`, but in your case, it is set to replace the inner content of the target element.

### `hx-target`

The `hx-target` attribute specifies which element in the DOM should be updated with the content returned by the HTMX request. In your code, `hx-target` is set to `#content`:

```html
<div class="contact-list-item" hx-swap="innerHTML" hx-target="#content">
```

Here, `hx-target="#content"` indicates that the content returned from the request should be inserted into the element with the ID `content`. This means that when a contact list item is clicked and an HTMX request is made, the result of the request (e.g., customer details or an edit form) will be inserted inside the `<div id="content">` element.

### Workflow

1. **Displaying Customer Details**: When a user clicks on a contact list item (`<div class="contact-list-item-details" hx-get="/customers/{{ customer.id }}">`), a GET request is made to `/customers/{{ customer.id }}`. The content returned by this request will replace the inner content of the `<div id="content">` element due to `hx-target="#content"` and `hx-swap="innerHTML"`.

2. **Editing Customer**: When the Edit button (`<button class="edit-button" hx-get="/customers/{{ customer.id }}?edit=true">Edit</button>`) is clicked, a GET request is made to `/customers/{{ customer.id }}?edit=true`. Again, the returned content (likely an edit form) will replace the inner content of the `<div id="content">` element due to `hx-target="#content"`.

3. **Deleting Customer**: When the Delete button (`<button class="delete-button" hx-delete="/customers/{{ customer.id }}" hx-confirm="Are you sure?">Delete</button>`) is clicked, a DELETE request is made to `/customers/{{ customer.id }}`. The `hx-confirm="Are you sure?"` adds a confirmation prompt before proceeding with the deletion. After deletion, the specific DOM update behavior will depend on additional server-side configuration or other HTMX response settings.

### Summary

- **`hx-swap="innerHTML"`**: Specifies that the inner content of the target element should be replaced by the content returned from the request.
- **`hx-target="#content"`**: Specifies that the element with the ID `content` should be the target for the DOM update with the returned content.

These configurations enable a more dynamic user experience where specific parts of the page are updated without the need to reload the entire page.


## SQL Exception Explanation

establishments.py
```python
except IntegrityError as e:
    if e.args[0] == '23000':
        raise ValueError("ERROR: could not delete establishment")
```
The `except` block catches `IntegrityError` exceptions that might occur during the execution of the operation in the `try` block.

- `except IntegrityError as e` catches integrity exceptions that may be raised by the database. These exceptions usually 
indicate violations of integrity constraints, such as foreign keys, primary keys (uniqueness), etc.
- `if e.args[0] == '23000':` checks if the specific error code is `'23000'`, which is the standard SQL code for referential 
integrity violations (e.g., trying to delete a row that is referenced by a foreign key in another table, or adding a row with 
an already existing primary key).

The `except IntegrityError` block can be used to catch integrity exceptions in INSERT, UPDATE, and DELETE operations. Any operation 
that violates integrity constraints defined in the database, such as primary keys, foreign keys, uniqueness, or other constraints, 
can raise an `IntegrityError`.


## Error resolution: I added 'hx-trigger="click"

The issue you are facing is due to the `hx-trigger="click"` attribute in the form. This attribute causes the form to be submitted 
on any click, regardless of where the click occurs within the form. To fix this, you should remove `hx-trigger="click"` and ensure 
that the form is only submitted when the "Save" button is clicked.

### Explanation of Changes

1. **Removal of `hx-trigger="click"`:** This prevents the form from being submitted on any click within the form. Now, the form will 
only be submitted when the "Save" button is clicked.

2. **Using `hx-post` on the form:** This ensures that the form submission uses the POST method to the correct URL with the 
establishment ID, if defined.

With these changes, the form will only be submitted when you click the "Save" button, avoiding the accidental creation of new records.

To submit the form only when the "Save" button is clicked, you can rely on the default behavior of HTML forms. When any form 
is submitted, the HTML itself initiates a POST request, so there's no need to use a trigger because the HTML DOM already has 
a default trigger. It is not necessary to use `hx-trigger` in this case, as the default behavior of a submit button within a 
form is to submit the form (POST).
