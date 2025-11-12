from flask import Flask, render_template, request
import joblib
import re

app = Flask(__name__)
model = joblib.load("password_model.pkl")

def password_features(password):
    length = len(password)
    digits = len(re.findall(r'\d', password))
    upper = len(re.findall(r'[A-Z]', password))
    lower = len(re.findall(r'[a-z]', password))
    symbols = len(re.findall(r'[^A-Za-z0-9]', password))
    return [length, digits, upper, lower, symbols]

@app.route("/", methods=["GET", "POST"])
def index():
    strength = None
    if request.method == "POST":
        password = request.form["password"]
        features = [password_features(password)]
        pred = model.predict(features)[0]
        if pred == 0:
            strength = ("Weak", "danger")
        elif pred == 1:
            strength = ("Medium", "warning")
        else:
            strength = ("Strong", "success")
    return render_template("index.html", strength=strength)

if __name__ == "__main__":
    app.run(debug=True)
