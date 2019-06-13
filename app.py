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
f = open(projects_file, 'r')
for item in f.read():
    if '\n' == item:
        if name in projects:
            name = ''
        else:
            projects.append(name)
            name = ''
    else:
        name += item
f.close()

poll_data = {
    'question': 'Vote for your favourite team ^^',
    'fields': projects
}


def if_ip_is_used():
    f = open(ip_file, 'r')
    data = f.read()
    f.close()
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr) in data


# -----------start-----------------
@app.route('/')
def root():
    f = open(ip, 'r')
    if request.environ.get('HTTP_X_REAL_IP', request.remote_addr) in f.read():
        f.close()
    else:
        f.close()
        return render_template('settings.html')

# -------------add.html-----------


@app.route('/add_temp')
def add_temp():
    return render_template('add.html')

#------------poll.html--------
@app.route('/home')
def home():
    return render_template('poll.html', data=poll_data, if_used=if_ip_is_used())


# -----------vote----------------


@app.route('/poll')
def poll():
    vote = request.args.get('field')

    if vote is None:
        return render_template('poll.html', data=poll_data)

    out = open(projects_file, 'a')
    out.write(vote + '\n')
    out.close()

    f = open(ip_file, 'a')
    f.write(request.environ.get('HTTP_X_REAL_IP', request.remote_addr + '\n'))
    f.close()

    return render_template('thankyou.html', data=vote)

# -----------------results----------------------


@app.route('/results')
def show_results():
    votes = {}
    for f in poll_data['fields']:
        votes[f] = -1

    f = open(projects_file, 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] += 1

    return render_template('results.html', data=poll_data, votes=votes)

# -------------add------------------------------------------


@app.route('/add_new', methods=["POST"])
def add_new():
    f = open(projects_file, 'r')
    project_name = request.form['addnew']
    data = f.read()
    f.close()

    if project_name in data:
        return render_template('poll.html', data=poll_data)

    poll_data['fields'].append(request.form['addnew'])

    f = open(projects_file, 'a')
    f.write(request.form['addnew']+'\n')
    f.close()


# ----------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0')
