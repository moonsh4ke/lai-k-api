from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return '<h1>Lai-K</h1>'

if __name__ == "__main__":
    app.run(debug=True)
