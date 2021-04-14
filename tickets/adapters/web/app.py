from flask import Flask, render_template, request, abort, redirect
from pathlib import Path

from flask.helpers import make_response, url_for
from injection import configure_injection
from datetime import datetime

from tickets.application import use_cases

from .forms import OpenTicketForm


app = Flask("web")
app.root_path = Path(__file__).resolve().parent
app.before_first_request(configure_injection)
app.secret_key = "NADA"


@app.template_filter()
def dateformat(date, format="%d/%m/%Y %H:%M"):
    return datetime.strftime(date, format)


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
def open_ticket():
    form = OpenTicketForm()
    if form.validate_on_submit():
        account = use_cases.get_account_by_username(form.author)
        use_cases.open_ticket(
            author=account, 
            title=form.title, 
            description=form.description, 
            ticket_type=form.type
        )
        return redirect(url_for('index'))

    return render_template('open_ticket.html', form=form)
