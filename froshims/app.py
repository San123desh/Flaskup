from flask import Flask, render_template, request

app = Flask(__name__)

SPORTS = ["Football","Crickte","Badmintion"]

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html', sport=SPORTS)


@app.route('/register', methods=['POST'])
def register():
    if not request.form.get("name") or request.form.get("sport") not in SPORTS:
        return render_template('failure.html')
    return render_template('success.html')
