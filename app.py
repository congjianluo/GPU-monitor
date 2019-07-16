import datetime, time
import json

from flask import Flask, render_template, make_response
from flask_apscheduler import APScheduler

from utils import ServerUtils

import sys

sys.path.append(".")
sys.path.append("./app/app")


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)
scheduler = APScheduler()
serverUitls = ServerUtils()

update_flag = False
machines_status = ""
temp_machines_status = json.dumps(
    {"data": [{"name": "System initting..."}],
     "update_time": int(time.mktime(datetime.datetime.now().timetuple()))})


def interval_time_quest():
    print("Start update!")
    global update_flag
    global machines_status
    global temp_machines_status
    temp_machines_status = machines_status
    update_flag = True
    status = serverUitls.gpu_status()
    machines_status = json.dumps({"data": status, "update_time": int(time.mktime(datetime.datetime.now().timetuple()))})
    update_flag = False
    print("Stop update!")


@app.route('/smile')
def index():
    return render_template("index.html")


@app.route('/get_status')
def get_result():
    global update_flag
    global machines_status
    if not update_flag:
        return make_response(machines_status)
    else:
        return make_response(temp_machines_status)


scheduler.add_job(func=interval_time_quest, id='1', trigger='interval',
                  seconds=60 * 2, replace_existing=True, next_run_time=datetime.datetime.now())
scheduler.init_app(app=app)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)
