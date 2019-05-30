from flask import Flask, request, render_template
import json
from flask import Markup
app = Flask(__name__)

#-----------start---------------
@app.route('/')
def index():
    f=open('names.txt', 'r')
    return render_template('voting.html', projects=f.read())
    f.close()

#-----------go to add_new.html----------
@app.route('/add_new', methods=['POST'])
def add_new():
    return render_template('add_new.html')

#----------add new project-----------
@app.route('/add', methods=['POST'])
def add_newName():
    f=open('names.txt','r')
    if request.form['name'] in f.read():
        f.close()
        return '''<h1>imeto e zaeto, a ti si pedal</h1>'''
    else:
        f.close()
        name=request.form['name']
        f=open('names.txt','a')
        new={name: 0}
        f.write(json.dumps(new))
        f.close()
    f=open('names.txt', 'r')
    return render_template('voting.html', name=name, projects=f.read())
    f.close()

#----------------------------------  
if __name__=='__main__':
    app.run()
