# Database Project - StylistData

Simple Flask webapp project backed by SQL Server.

Distributed for learning purposes.


## Dependencies

- Python3.8+ and SQL Server.
- Poetry (for dependency management)
- Libraries
  - [Flask](https://flask.palletsprojects.com)
  - Pyodbc
  - [htmx](https://htmx.org) (included in index.html)

Dependencies can be managed using [Poetry](https://python-poetry.org/). 
To install Poetry, follow the [installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer).
Make sure you add Poetry to your path (section 3 of the guide).

Then install the project dependencies with: `poetry install`.

You can then use: `poetry run ....` or open `poetry shell` to run your project.
If you use poetry shell, then run `python app.py` to execute the app.


## Running

If not on a virtual environemnt open one with: `poetry shell`

To run the application, use the following command: `flask run --debug`, if your application is in
a file named 'app', 'application', 'create_app', or 'make_app'. 
Otherwise you can use: `flask --app [python_app_file_name] run --debug` 

`--debug` is used to make errors easier to see and debug, but it's not necessary.

If port 5000 is already occupied (that is, if an ''Address already in use error occurs), you 
can use `flask run --port 5001` to use a different port.

### Use `flask --help` and `flask run --help` for more useful information.


## Recommended resources
See Flask Documentation, where you can find very important information about Database-Website connection or Flask instalation:
  - [Flask](https://flask.palletsprojects.com)

Visit Poetry Documentation, if you have any question related with dependencies or Poetry instalation:
  - [Poetry](https://python-poetry.org/)

For detailed information on HTMX, visit:
  - [htmx](https://htmx.org)


  