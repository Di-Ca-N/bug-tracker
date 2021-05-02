from flask import Flask, render_template, request, abort, redirect
from flask.helpers import make_response, url_for
from flask_security import login_required, current_user, user_registered

from pathlib import Path
from injection import configure_injection
from datetime import datetime

from tickets.application import use_cases

from .forms import OpenTicketForm, MyRegisterForm
from .models import db, security, user_datastore, migrate


app = Flask("web")
BASE_DIR = Path(__file__).resolve().parent
app.root_path = BASE_DIR

app.config.update({
    "SECRET_KEY": "NADA",
    "SECURITY_PASSWORD_SALT": "secure-salt",
    "SECURITY_REGISTERABLE": True,
    "SECURITY_SEND_REGISTER_EMAIL": False,
    "SECURITY_LOGIN_URL": '/login/',
    "SECURITY_REGISTER_URL": '/register/',
    "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(BASE_DIR / "sqlite.db"),
    "SQLALCHEMY_ENGINE_OPTIONS": {"pool_pre_ping": True},
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
})

db.init_app(app)
security.init_app(app, user_datastore, register_form=MyRegisterForm)
migrate.init_app(app, directory=BASE_DIR / 'migrations')

@app.before_first_request
def setup():
    configure_injection()
    db.create_all()

@app.template_filter()
def dateformat(date, format="%d/%m/%Y %H:%M"):
    return datetime.strftime(date, format)

@user_registered.connect
def create_account(sender, user, confirm_token):
    use_cases.register_account(
        user.username,
        user.email
    )


@app.route("/")
def index():
    tickets = use_cases.list_all_tickets()
    return render_template('ticket_index.html', tickets=tickets)


@app.route("/tickets/<uuid:ticket_code>/")
def detail_ticket(ticket_code):
    ticket = use_cases.get_ticket(ticket_code)
    if ticket is None:
        abort(404)
    return render_template('detail_ticket.html', ticket=ticket)


@app.route("/tickets/<uuid:ticket_code>/assign/", methods=["POST"])
def assign_ticket_to_user(ticket_code):
    ticket = use_cases.get_ticket(ticket_code)
    if ticket is None:
        abort(404)

    username = request.form["username"]
    account = use_cases.get_account_by_username(username)

    use_cases.assign_ticket(ticket, account)
    response = make_response(None, 200)
    return response


@app.route("/tickets/open/", methods=["GET", "POST"])
@login_required
def open_ticket():
    form = OpenTicketForm()
    if form.validate_on_submit():
        account = use_cases.get_account_by_username(current_user.username)
        use_cases.open_ticket(
            author=account,
            title=form.title.data, 
            description=form.description.data, 
            ticket_type=form.type.data
        )
        return redirect(url_for('index'))

    return render_template('open_ticket.html', form=form)
