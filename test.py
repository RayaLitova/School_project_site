from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def test():
    return render_template('settings.html'), render_template('poll.html', data='aaa')

if __name__ == "__main__":
    app.run()
