from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/club1")
def club1():
    return render_template('club1.html')


@app.route("/club2")
def club2():
    return render_template('club2.html')


@app.route("/club3")
def club3():
    return render_template('club3.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/formOutput", methods=['POST'])
def formOutput():
    email = request.form.get("email")
    password = request.form.get("psw")
    ConfirmPassword = request.form.get("psw-repeat")
    Successfull = request.form.get("Successfull")
    return render_template('formOutput.html', email=email, password=password, ConfirmPassword=ConfirmPassword, Successfull=Successfull)


if __name__ == '__main__':
    app.run(debug=True)
