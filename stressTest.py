import os
import time
import logging
import subprocess
import psutil
import mysql.connector
from dotenv import load_dotenv

logging.basicConfig(
    filename='stressTestLogs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()
sqlpass = os.environ.get('Sqlpass')

# Stress test functions with improved logging
def memory_stress_test():
    try:
        logging.info("Starting memory stress test.")
        os.system("stress-ng --vm 10 --vm-bytes 90% --timeout 30s")
        memory_usage = psutil.virtual_memory().percent
        logging.info(f"Memory usage after test: {memory_usage}%")
    except Exception as e:
        logging.error(f"Memory stress test failed: {e}")

def disk_stress_test():
    try:
        logging.info("Starting disk stress test.")
        os.system("stress-ng --hdd 10 --hdd-bytes 95% --timeout 30s")
        disk_usage = psutil.disk_usage('/').percent
        logging.info(f"Disk usage after test: {disk_usage}%")
    except Exception as e:
        logging.error(f"Disk stress test failed: {e}")

def cpu_stress_test():
    try:
        logging.info("Starting CPU stress test.")
        os.system("stress-ng --cpu 1 --cpu-load 80 --timeout 30s")
        cpu_usage = psutil.cpu_percent(interval=1)
        logging.info(f"CPU usage after test: {cpu_usage}%")
    except Exception as e:
        logging.error(f"CPU stress test failed: {e}")

def network_stress_test():
    try:
        logging.info("Starting network stress test.")
        server_process = subprocess.Popen(["iperf3", "-s"])
        time.sleep(1)
        os.system("iperf3 -c 127.0.0.1 -t 30 -P 10")
        net_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        logging.info(f"Network data transferred (in bytes): {net_usage}")
        server_process.terminate()
    except Exception as e:
        logging.error(f"Network stress test failed: {e}")

def mysql_stress_test():
    logging.info("Starting MySQL stress test.")
    try:
        os.system(f"sysbench --db-driver=mysql --mysql-host=192.168.1.22 --mysql-user=remote --mysql-password={Sqlpass} --mysql-db=stressTest --table-size=1000 --tables=1 oltp_read_only prepare")
        os.system(f"sysbench --db-driver=mysql --mysql-host=192.168.1.22 --mysql-user=remote --mysql-password={Sqlpass} --mysql-db=stressTest --table-size=1000 --tables=1 --threads=4 --time=60 oltp_read_only run")

        # Calculate QPS
        connection = mysql.connector.connect(
            host="192.168.1.22",
            user="remote",
            password=sqlpass,
            database="stressTest"
        )
        cursor = connection.cursor()
        cursor.execute("SHOW GLOBAL STATUS LIKE 'Questions';")
        initial_queries = int(cursor.fetchone()[1])
        time.sleep(1)
        cursor.execute("SHOW GLOBAL STATUS LIKE 'Questions';")
        final_queries = int(cursor.fetchone()[1])
        qps = final_queries - initial_queries
        logging.info(f"MySQL QPS during test: {qps}")

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        logging.error(f"MySQL stress test failed: {err}")
    except Exception as e:
        logging.error(f"MySQL stress test encountered an unexpected error: {e}")
    finally:
        os.system(f"sysbench --db-driver=mysql --mysql-host=192.168.1.22 --mysql-user=remote --mysql-password={Sqlpass} --mysql-db=stressTest oltp_read_only cleanup")


def main():
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
                logging.warning("Invalid choice entered by user.")
                print("Invalid choice. Please try again.")
    finally:
        print("Stopping exporters...")
        node_exp.terminate()
        mysqld_exp.terminate()
        node_exp.wait()
        mysqld_exp.wait()
        logging.info("Exporters stopped.")

if __name__ == "__main__":
    main()
