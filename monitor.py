import psutil
import requests
import time
import subprocess
from ticket_manager import create_ticket


# ✅ CPU check
def check_cpu():
    cpu = psutil.cpu_percent(interval=1)
    if cpu > 80:
        create_ticket("High CPU Usage", "High")
    return cpu


# ✅ Memory check
def check_memory():
    memory = psutil.virtual_memory().percent
    if memory > 80:
        create_ticket("High Memory Usage", "Medium")
    return memory


# ✅ API check
def check_api():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)
        if response.status_code != 200:
            create_ticket("API Down", "High")
    except:
        create_ticket("API Not Reachable", "High")


# ✅ Disk check (Linux command)
def check_disk():
    try:
        import subprocess

        output = subprocess.check_output(["df", "-h"]).decode()
        print("\nDisk Usage:\n", output)

        lines = output.split("\n")

        for line in lines[1:]:
            parts = line.split()

            if len(parts) > 5:
                mount_point = parts[5]
                usage = parts[4]

                # ❌ Ignore Windows drives and temp systems
                if "/mnt/c" in mount_point or "/mnt/d" in mount_point:
                    continue
                if "tmpfs" in parts[0] or "none" in parts[0]:
                    continue

                if "%" in usage:
                    value = int(usage.replace("%", ""))

                    if value > 80:
                        print("High Disk Usage Detected:", mount_point, usage)
                        create_ticket("High Disk Usage", "High")

    except Exception as e:
        print("Disk check error:", e)


# ✅ Process check
def check_process():
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 50:
                print("High CPU Process:", proc.info['name'])
                create_ticket("Process consuming high CPU", "Medium")
        except:
            pass


# ✅ Main monitoring loop
def run_monitor():
    while True:
        print("\n===== Monitoring Started =====")

        cpu = check_cpu()
        memory = check_memory()
        check_api()
        check_disk()
        check_process()

        print("CPU:", cpu, "%")
        print("Memory:", memory, "%")

        time.sleep(10)


# ✅ Entry point
if __name__ == "__main__":
    run_monitor()