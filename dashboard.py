import sqlite3

def show_dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'")
    open_tickets = cursor.fetchone()[0]

    print("\n===== DASHBOARD =====")
    print("Total Tickets:", total)
    print("Open Tickets:", open_tickets)

    cursor.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()

    print("\nRecent Tickets:")
    for r in rows:
        print(r)

    conn.close()


# 👉 THIS IS IMPORTANT
if __name__ == "__main__":
    show_dashboard()