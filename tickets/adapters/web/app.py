from flask import Flask, render_template, request, abort
from pathlib import Path

from flask.helpers import make_response
from injection import configure_injection
from datetime import datetime

from tickets.application.use_cases import get_account_by_username, get_ticket, list_all_tickets, open_ticket, assign_ticket


app = Flask("web")
app.root_path = Path(__file__).resolve().parent
app.before_first_request(configure_injection)


@app.template_filter()
def dateformat(date, format="%d/%m/%Y %H:%M"):
    return datetime.strftime(date, format)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        author = request.form["author"]
        title = request.form["title"]
        description = request.form["description"]
        ticket_type = 'Bug'
        open_ticket(author=author, title=title, description=description, ticket_type=ticket_type)

    tickets = list_all_tickets()
    return render_template('ticket_index.html', tickets=tickets)


@app.route("/tickets/<uuid:ticket_code>/")
def detail_ticket(ticket_code):
    ticket = get_ticket(ticket_code)
    if ticket is None:
        abort(404)
    return render_template('detail_ticket.html', ticket=ticket)


@app.route("/tickets/<uuid:ticket_code>/assign/", methods=["POST"])
def assign_ticket_to_user(ticket_code):
    ticket = get_ticket(ticket_code)
    if ticket is None:
        abort(404)

    username = request.form["username"]
    account = get_account_by_username(username)

    assign_ticket(ticket, account)
    response = make_response(None, 200)
    return response
