import subprocess, re
from icoin.util.homer import HOME
from icoin import app


def init():
    app.config.from_object("icoin.core.config")
    app.config.update(get_env_vars())
    app.config['VERSION'] = get_version()

def get_env_vars():
    return {}

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

