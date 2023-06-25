from datetime import datetime

def calculate_uptime(start_time):
    # Calculate how many hours the program has been up for
    uptime = datetime.now() - start_time
    uptime = uptime.total_seconds() / 3600
    uptime = round(uptime, 2)
    return uptime