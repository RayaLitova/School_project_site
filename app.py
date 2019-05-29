from flask import Flask, request, render_template
import json
app = Flask(__name__)

#-----------start---------------
@app.route('/')
def index():
    return render_template('voting.html')

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
    return render_template('voting.html', name=name)

#--------------print names-----------      
@app.route('/print_names')
def print_names():
    f=open('names.txt','r')
    projects=f.read()
    return render_template('voting.html', projects=json.dumps(f.read()))
    f.close()

#----------------------------------  
if __name__=='__main__':
    app.run()
