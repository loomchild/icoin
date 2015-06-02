import subprocess, re, os
from icoin.util.homer import HOME
from icoin import app


class DefaultConfig:
    HOST = "0.0.0.0"
    PORT = 8080
    THREADS = 1

    DEBUG = False
    TESTING = False

    SECRET_KEY = os.urandom(24)
    
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "icoin"
    DB_USER = ""
    DB_PASSWORD = ""

    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = "icoin <icoin@localhost>"

def init():
    app.config.from_object("icoin.core.config.DefaultConfig")
    
    app.config.update(get_env_vars())
    
    app.config['VERSION'] = get_version()

    validate()


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

def get_env_vars():
    env_vars = {}
    for name in (n for n in dir(DefaultConfig) if not n.startswith("_")):
        value = os.environ.get(name)
        if value != None:
            #TODO: cast to the same type as in DeaultConfig
            env_vars[name] = value
    return env_vars

def validate():
    if app.config["SECRET_KEY"] == DefaultConfig.SECRET_KEY:
        app.logger.warning("No SECRET_KEY provided, generated a random one. " +
                "Sessions are valid only for this instance and will expire " +
                "after restart.")

