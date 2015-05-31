import subprocess, re
from icoin.util.homer import HOME
from icoin import app


class DefaultConfig:
    SECRET_KEY = 'B0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "icoin"
    DB_USER = ""
    DB_PASSWORD = ""


def init():
    app.config.from_object("icoin.core.config.DefaultConfig")
    
    app.config.update(get_env_vars())
    
    app.config['VERSION'] = get_version()
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db()


def get_version():
    version = "Unknown"
    try:
        description = subprocess.check_output(
            ["git", "describe", "--long",  "--match", "v*"], 
            stderr=subprocess.STDOUT, cwd=HOME, universal_newlines=True)
        m = re.match(r"v([\w\.]+)-\d+-g(\w+)", description)
        if m:
            version = m.group(1) + "-" + m.group(2)
    except subprocess.CalledProcessError:
        pass 
    return version

def get_db():
    user = app.config["DB_USER"]
    password = app.config["DB_PASSWORD"]
    host = app.config["DB_HOST"]
    port = app.config["DB_PORT"]
    name = app.config["DB_NAME"]

    string = "postgresql://"
    
    if user: 
        string += user
        if password:
            string += ":" + password
        string += "@"

    if host:
        string += host

    if port:
        string += ":" + port

    if name:
        string += "/" + name

    return string

def get_env_vars():
    return {}

