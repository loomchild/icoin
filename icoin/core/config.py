import subprocess, re, os
from icoin.util.homer import HOME
from icoin import app


class DefaultConfig:
    SECRET_KEY = 'B0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    HOST = "0.0.0.0"
    PORT = 8080
    THREADS = 1

    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "icoin"
    DB_USER = ""
    DB_PASSWORD = ""


def init():
    app.config.from_object("icoin.core.config.DefaultConfig")
    
    app.config.update(get_env_vars())
    
    app.config['VERSION'] = get_version()


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
            env_vars[name] = value
    return env_vars

