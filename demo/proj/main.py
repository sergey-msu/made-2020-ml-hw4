from flask import jsonify, render_template, request, redirect, url_for
from flask_login import login_required, logout_user, login_user
from core.server import DemoServer
from forms.login_form import LoginForm


server = DemoServer()
app = server.create()


@app.route("/")
@login_required
def welcome():
    return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():  # POST
        user = server.get_user_by_name(form.name.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            next_uri = request.args.get("next") or url_for("welcome")
            return redirect(next_uri)

    # GET
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("login")


@app.route("/register")
def register():
    # TODO
    return render_template("register.html")


@app.route("/classify", methods=["GET"])
@login_required
def classify():
    if request.method == "GET":
        return render_template("classify.html")


@app.route("/classify_ajax", methods=["POST"])
@login_required
def classify_ajax():
    if "img" not in request.files:
        raise Exception('ERROR: no image')

    image = request.files["img"]
    result = server.classify(image)

    return jsonify(result=result)


if __name__ == "__main__":
    server.run()
