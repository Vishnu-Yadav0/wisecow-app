#System Health Monitoring
import psutil
import logging
import time

#Setting up Log File
#logging.basicConfig(filename='/var/log/system_health.log', level=logging.INFO, format='%(asctime)s - %(message)s')

logging.basicConfig(filename='D:\system_health.log', level=logging.INFO, format='%(asctime)s - %(message)s')


CPU_THRESHOLD = 80
DISK_THRESHOLD = 80
MEMORY_THRESHOLD = 80

def health_check():
    cpu_usage=psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        logging.warning(f"ALERT: CPU usage is above {CPU_THRESHOLD}%! Current usage: {cpu_usage}%")
    
    mem_usage=psutil.virtual_memory().percent
    if mem_usage > MEMORY_THRESHOLD:
        logging.WARNING(f"ALERT: Memory usage is above {MEM_THRESHOLD}%! Current usage: {mem_usage}%")
    
    disk_usage=psutil.disk_usage('/').percent
    if disk_usage > DISK_THRESHOLD:
        logging.warning(f"ALERT: Disk usage is above {DISK_THRESHOLD}%! Current usage: {disk_usage}%")

    process_count=len(psutil.pids())
    logging.info(f"INFO: Current number of running processes: {process_count}")

    print("System health check complete. Check /var/log/system_health.log for details.")


while True:
    health_check()
    time.sleep(10)
