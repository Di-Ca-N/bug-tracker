from use_cases import open_ticket, list_all_tickets


def run_console_interface():
    while True:
        print("O que deseja fazer?")
        print("1. Cadastrar um ticket")
        print("2. Listar Tickets cadastrados")

        opt = input("Opção desejada: ")
        
        if opt == '1':
            author = input("Autor: ")
            title = input("Título: ")
            description = input("Descrição: ")
            ticket_type = input("Tipo: ")
            ticket = open_ticket(author=author, title=title, description=description, ticket_type=ticket_type)
            print(f"Ticket criado! Código: {ticket.code}")
        if opt == '2':
            tickets = list_all_tickets()
            for ticket in tickets:
                print(ticket)
