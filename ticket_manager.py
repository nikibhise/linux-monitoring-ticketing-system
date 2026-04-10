import sqlite3
import datetime


# Check if ticket already exists
def ticket_exists(issue):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM tickets WHERE issue=? AND status IN ('Open', 'In Progress')",
    (issue,)
    )


    result = cursor.fetchone()
    conn.close()
    return result is not None


# Create new ticket
def create_ticket(issue, priority):
    conn = None
    try:
        if ticket_exists(issue):
            print("Ticket already exists:", issue)
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # SLA logic
        if priority == "High":
            sla = "2 hours"
        elif priority == "Medium":
            sla = "6 hours"
        else:
            sla = "24 hours"

        cursor.execute(
            "INSERT INTO tickets (issue, priority, status, sla, root_cause) VALUES (?, ?, ?, ?, ?)",
            (issue, priority, "Open", sla, "Pending")
        )

        conn.commit()
        print("Ticket created:", issue)

    except Exception as e:
        print("Error:", e)

    finally:
        if conn:
            conn.close()

# View all tickets
def view_tickets():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    print("\n--- ALL TICKETS ---")
    for t in tickets:
        print(t)

    conn.close()

def update_ticket(ticket_id, status, root_cause):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tickets SET status=?, root_cause=? WHERE id=?",
        (status, root_cause, ticket_id)
    )

    conn.commit()
    conn.close()

    print("Ticket updated:", ticket_id)