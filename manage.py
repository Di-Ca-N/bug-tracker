import argparse
import sys
import subprocess
import os

def setup_flask_env(env):
    env.update({"FLASK_APP": "tickets.adapters.web.app"})
    if env["ENV"] == "dev":
        env.update({"FLASK_DEBUG": "1"})

def run_server(env):
    setup_flask_env(env)
    subprocess.run(["flask", "run"], env=env)

def run_tests(env):
    subprocess.run(["python", "-m", "unittest"], env=env)

def run_makemigrations(env):
    setup_flask_env(env)
    subprocess.run(['flask', 'db', 'migrate'], env=env)

def run_migrate(env):
    setup_flask_env(env)
    subprocess.run(['flask', 'db', 'upgrade'], env=env)

def run_init_db(env):
    setup_flask_env(env)
    subprocess.run(['flask', 'db', 'init'], env=env)

commands = {
    'test': run_tests,
    "web": {
        "run": run_server,
        'migrate': run_migrate,
        'makemigrations': run_makemigrations,
        'initdb': run_init_db,
    }
}

parser = argparse.ArgumentParser()
parser.add_argument("cmds", nargs="+")
parser.add_argument("--env", choices=["dev", "prod"], default="dev")
data = parser.parse_args(sys.argv[1:])


try:
    env = os.environ.copy()
    env.update({"ENV": data.env})
    step = commands
    for cmd in data.cmds:
        step = step.get(cmd)
        if step is None:
            print(f"Unknown action '{cmd}'")
            break
    else:
        if not callable(step):
            options = ' '.join(step.keys())
            print(f"Available actions for {cmd}: {options}")
        else:
            step(env)
    
except KeyboardInterrupt:
    pass