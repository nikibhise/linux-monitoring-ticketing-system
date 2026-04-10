from ticket_manager import create_ticket

def analyze_logs():
    try:
        file_path = "/var/log/syslog"   # ✅ real Linux log

        with open(file_path, "r") as file:
            lines = file.readlines()

        error_count = 0

        for line in lines[-50:]:   # check last 50 lines
            if "error" in line.lower() or "failed" in line.lower():
                print("Log issue:", line.strip())
                error_count += 1

        print("Total issues found:", error_count)

        if error_count >= 3:
            create_ticket("Multiple system-level errors detected", "High")

    except Exception as e:
        print("Log read error:", e)