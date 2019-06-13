from flask import Flask, render_template, request
import os
from flask import request
from flask import jsonify
import json

app = Flask(__name__)
filename = 'data.txt'
ip = 'ip.txt'
x = []
name = ''
f = open(filename, 'r')
for item in f.read():
    if '\n' == item:
        if name in x:
            name = ''
        else:
            x.append(name)
            name = ''
    else:
        name += item
f.close()

poll_data = {
    'question': 'Vote for your favourite team ^^',
    'fields': x
}

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

#------------settings.html--------
@app.route('/home')
def home():
    f = open(ip, 'r')
    if request.environ.get('HTTP_X_REAL_IP', request.remote_addr) in f.read():
        f.close()
        return "You can't vote two times form one device!!"
    else:
        f.close()
        return render_template('poll.html', data=poll_data)


# -----------vote----------------


@app.route('/poll')
def poll():
    vote = request.args.get('field')

    if vote is None:
        return render_template('poll.html', data=poll_data)

    out = open(filename, 'a')
    out.write(vote + '\n')
    out.close()
    f = open(ip, 'r')
    f.close()
    f = open(ip, 'a')
    f.write(request.environ.get('HTTP_X_REAL_IP', request.remote_addr + '\n'))
    f.close()
    return render_template('thankyou.html', data=vote)

# -----------------results----------------------


@app.route('/results')
def show_results():
    votes = {}
    for f in poll_data['fields']:
        votes[f] = -1

    f = open(filename, 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] += 1

    return render_template('results.html', data=poll_data, votes=votes)

# -------------add------------------------------------------


@app.route('/add_new', methods=["POST"])
def add_new():
    f = open(filename, 'r')
    a = request.form['addnew']
    data = f.read()
    f.close()
    if a in data:
        return render_template('poll.html', data=poll_data)

    poll_data['fields'].append(request.form['addnew'])
    f = open(filename, 'a')
    f.write(request.form['addnew']+'\n')
    f.close()
    f = open('ip.txt', 'r')
    if request.environ.get('HTTP_X_REAL_IP', request.remote_addr) in f.read():
        f.close()
        return "You can't vote two times from one device!!"
    else:
        return render_template('poll.html', data=poll_data)


# ----------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0')
