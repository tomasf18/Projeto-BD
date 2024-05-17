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