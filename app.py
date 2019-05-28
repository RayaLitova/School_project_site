from flask import Flask, request, render_template
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('voting.html')

@app.route('/add_new', methods=['POST'])
def add_new():
    return render_template('add_new.html')

@app.route('/add', methods=['POST'])
def add_newName():
    f=open('names.txt','r')
    if request.form['name'] in f.read():
        f.close()
        request.form['name']='zaeto ime pedal'
        add_new()
    else:
        f.close()
        name=request.form['name']
        f=open('names.txt','a')
        new={name: 0}
        f.write(json.dumps(new))
        f.close()
        
    
    
if __name__=='__main__':
    app.run()
