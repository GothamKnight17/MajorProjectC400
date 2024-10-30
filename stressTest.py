import os
import smtplib
import psutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from dotenv import load_dotenv
import logging
import subprocess

# Configure logging
logging.basicConfig(filename='stressTestLogs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Retrieve sensitive data from environment variables
sqlpass = os.environ.get('sqlpass')

def memory_stress_test():
    logging.info("Running memory stress test...")
    os.system("stress-ng --vm 1 --vm-bytes 80% --timeout 30s")
    memory_usage = psutil.virtual_memory().percent
    logging.info(f"Memory usage after test: {memory_usage}%")

def disk_stress_test():
    logging.info("Running disk stress test...")
    os.system("stress-ng --hdd 1 --hdd-bytes 80% --timeout 30s")
    disk_usage = psutil.disk_usage('/').percent
    logging.info(f"Disk usage after test: {disk_usage}%")

def cpu_stress_test():
    logging.info("Running CPU stress test...")
    os.system("stress-ng --cpu 1 --cpu-load 80 --timeout 30s")
    cpu_usage = psutil.cpu_percent(interval=1)
    logging.info(f"CPU usage after test: {cpu_usage}%")

def network_stress_test():
    logging.info("Running network stress test...")
    server_process = subprocess.Popen(["iperf3", "-s"])
    time.sleep(1)
    os.system("iperf3 -c 127.0.0.1 -t 30 -P 10")
    net_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    server_process.terminate()
    logging.info(f"Network data transferred (in bytes): {net_usage}")

def mysql_stress_test():
    logging.info("Running MySQL stress test...")
    os.system(f"sysbench --db-driver=mysql --mysql-host=192.168.1.4 --mysql-user=remote --mysql-password={sqlpass} --mysql-db=stressTest --table-size=1000 --tables=1 oltp_read_only prepare")
    os.system(f"sysbench --db-driver=mysql --mysql-host=192.168.1.4 --mysql-user=remote --mysql-password={sqlpass} --mysql-db=stressTest --table-size=1000 --tables=1 --threads=4 --time=60 oltp_read_only run")
    os.system(f"sysbench --db-driver=mysql --mysql-host=192.168.1.4 --mysql-user=remote --mysql-password={sqlpass} --mysql-db=stressTest oltp_read_only cleanup")
    mysql_cpu_usage = psutil.cpu_percent(interval=1)
    logging.info(f"MySQL CPU usage during test: {mysql_cpu_usage}%")

def main():
    # Start node_exporter and mysqld_exporter using subprocess.Popen
    node_exp = subprocess.Popen(["/root/node_exporter-1.8.2.linux-amd64/node_exporter"])
    mysqld_exp = subprocess.Popen(["/root/mysqld_exporter-0.15.1.linux-amd64/mysqld_exporter", "--config.my-cnf=/root/.my.cnf"])

    try:
        while True:
            print("\nStress Testing Menu:")
            print("1. Memory Stress Testing")
            print("2. Disk Stress Testing")
            print("3. Network Stress Testing")
            print("4. CPU Stress Testing")
            print("5. MySQL Stress Testing")
            print("6. Exit")
            choice = input("Enter choice: ")
            logging.info(f"User selected option: {choice}")

            if choice == '1':
                memory_stress_test()
            elif choice == '2':
                disk_stress_test()
            elif choice == '3':
                network_stress_test()
            elif choice == '4':
                cpu_stress_test()
            elif choice == '5':
                mysql_stress_test()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        # Stop exporters when exiting
        print("Stopping exporters...")
        node_exp.terminate()
        mysqld_exp.terminate()
        node_exp.wait()
        mysqld_exp.wait()
        print("Exporters stopped.")


if __name__ == "__main__":
    main()
#Changing to check 1
