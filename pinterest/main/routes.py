from flask import render_template, Blueprint


from flask_login import login_required

main = Blueprint('main', __name__)


# @main.route("/")
@main.route("/home")
def home():
    return render_template('view_pins.html')


@main.route("/about")
@login_required
def about():
    return render_template('about.html', title='about')
