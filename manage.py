import argparse
import sys
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["migrate", "runserver", "test"])
parser.add_argument("--env", choices=["dev", "prod"], default="dev")
data = parser.parse_args(sys.argv[1:])


def run_server(env):
    env.update({"FLASK_APP": "tickets.adapters.web.app"})
    if env["ENV"] == "dev":
        env.update({"FLASK_DEBUG": "1"})
    subprocess.run(["flask", "run"], env=env)

try:
    env = os.environ.copy()
    env.update({"ENV": data.env})

    if data.action == "runserver":
        run_server(env)
    elif data.action == "test":
        print("Tests not configured yet")
    elif data.action == "migrate":
        print("Database not configured yet")
    else:
        print(f"Unknown action: '{data.action}'")
except KeyboardInterrupt:
    pass