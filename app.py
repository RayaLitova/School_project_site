from flask import Flask, render_template, request
import os
from flask import request
from flask import jsonify
import json

app = Flask(__name__)

projects_file = 'data.txt'
ip_file = 'ip.txt'

projects = []
name = ''


def get_projects(projects, name):
    projects_in_file = read_file(projects_file)
    for project in projects_in_file:
        if '\n' == project:
            if name in projects:
                name = ''
            else:
                projects.append(name)
                name = ''
        else:
            name += project

    return projects, name


def if_ip_is_used():
    f = open(ip_file, 'r')
    data = f.read()
    f.close()
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr) in data


def write_in_file(ffile, data):
    f = open(ffile, 'a')
    f.write(data)
    f.close()


def read_file(ffile):
    f = open(ffile, 'r')
    data = f.read()
    f.close()

    return data


projects, name = get_projects(projects, name)

poll_data = {
    'question': 'Vote for your favourite team ^^',
    'fields': projects
}


# -----------start-----------------


@app.route('/')
def root():
    return render_template('settings.html')


# -------------add.html-----------


@app.route('/add_temp')
def add_temp():
    return render_template('add.html')

# ------------settings.html--------


@app.route('/home')
def home():
    return render_template('poll.html', data=poll_data, if_used=if_ip_is_used())

# -----------vote----------------


@app.route('/poll')
def poll():
    vote = request.args.get('field')

    if vote is None:
        return render_template('poll.html', data=poll_data)

    write_in_file(projects_file, vote + '\n')

    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr + '\n')
    write_in_file(ip_file, user_ip)

    return render_template('thankyou.html', data=vote)

# -----------------results----------------------


@app.route('/results')
def show_results():
    votes = {}

    for pproject in poll_data['fields']:
        votes[pproject] = -1

    f = open(projects_file, 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] += 1

    f.close()

    return render_template('results.html', data=poll_data, votes=votes)

# -------------add------------------------------------------


@app.route('/add_new', methods=["POST"])
def add_new():

    data = read_file(projects_file)
    project_name = request.form['addnew']

    if project_name in data:
        return render_template('poll.html', data=poll_data)

    poll_data['fields'].append(request.form['addnew'])

    write_in_file(projects_file, request.form['addnew']+'\n')

    return render_template('poll.html', data=poll_data)


# ----------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0')
