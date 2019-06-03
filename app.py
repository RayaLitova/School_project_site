from flask import Flask, render_template, request
import os
app = Flask(__name__)
filename = 'data.txt'
ip='ip.txt'
x=[]
name=''
f=open(filename,'r')
for item in f.read():
    if '\n'==item:
        if name in x:
            name=''
        else:
            x.append(name)
            name=''
    else:
        name+=item
f.close()

poll_data = {
    'question': 'Vote for your favourite team ^^',
    'fields': x
}


@app.route('/')
def root():
    f=open(ip,'r')
    if request.environ.get('HTTP_X_REAL_IP', request.remote_addr) in f.read():
        f.close
        return "You can't vote two times form one devise!!"
    else:
        f.close()
        f=open(ip,'a')
        if request.environ.get('HTTP_X_REAL_IP', request.remote_addr)=='127.0.0.1':
            return render_template('poll.html', data=poll_data)
            f.close()
        else:
            f.write(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
            f.close()
            return render_template('poll.html', data=poll_data)


@app.route('/add_temp')
def add_temp():
    return render_template('add.html')

@app.route('/poll')
def poll():
    vote = request.args.get('field')

    out = open(filename, 'a')
    out.write(vote + '\n')
    out.close()

    return render_template('thankyou.html', data=vote)
    
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

@app.route('/add_new', methods=['POST'])
def add_new():
    f = open(filename, 'r')
    if request.form['add'] in f.read():
        f.close()
        return 'imeto e zaeto a ti si pedal <3'
    else:
        f.close()
        poll_data['fields'].append(request.form['addnew'])
        f=open(filename,'a')
        f.write(request.form['addnew'])
        f.close()
        return "Successfully added ^^"



if __name__ == "__main__":
    app.run()
