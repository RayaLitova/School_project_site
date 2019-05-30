from flask import Flask, request, render_template
import json
from flask import Markup
app = Flask(__name__)


# -----------start---------------
@app.route('/')
def index():
    with open("names.json", "r") as read_file:
        data = json.load(read_file)
    return render_template('voting.html', projects=data['projects'])

# -----------go to add_new.html----------


@app.route('/add_new', methods=['POST'])
def add_new():
    return render_template('add_new.html')

# ----------add new project-----------


@app.route('/add', methods=['POST'])
def add_newName():

    with open("names.json", "r") as read_file:
        data = json.load(read_file)

    if request.form['name'] in data:
        return '''<h1>imeto e zaeto, a ti si pedal</h1>'''
    else:
        name = request.form['name']
        data['projects'].append({
            'name': name,
            'description': '',
            'value': 0
        })

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

    return render_template('voting.html', name=name, projects=data['projects'])


# ----------------------------------
if __name__ == '__main__':
    app.run()
