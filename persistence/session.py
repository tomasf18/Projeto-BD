import configparser         # module used to work with INI configuration files such as conf.ini
import functools            # provides tools for working with invocable functions and objects
from pathlib import Path    # provides classes to represent file system paths with specific semantics for different operating systems.

import pyodbc   # a Python module that makes it easy to connect to databases using ODBC (Open Database Connectivity).
import os       # provides a way to use operating system-dependent functionality.

@functools.cache # means that the results of the function will be memorized for future calls with the same arguments (avoiding repetition of hard work)
def conn_string() -> str:
    config_file = Path("conf.ini")                          # obtain the necessary settings for connecting to the database
    assert config_file.exists(), "conf.ini file not found"  # uses configparser to read settings from the INI file.

    config = configparser.ConfigParser(os.environ)
    config.read(config_file)

    server = config["database"]["server"]
    db_name = config["database"]["name"]
    username = config["database"]["username"]
    password = config["database"]["password"]

    # with these settings, we construct a formatted connection string that will be used to connect to the SQL Server database.

    return f"DRIVER={{SQL Server}};SERVER={server};DATABASE={db_name};UID={username};PWD={password};"


def create_connection():
    my_conn_string = conn_string()          # uses the string returned by conn_string() to create a connection to the database
    return pyodbc.connect(my_conn_string)   # using the connection string, create a connection with the db and return the connection object