
import requests
import logging
import time

#Set up logging
logging.basicConfig(filename='/var/log/app_health.log', level=logging.INFO, format='%(asctime)s - %(message)s')

#URL of the application to check
url = "http://54.146.140.116/"

# Function to check application health
def check_health():
    try:
        response = requests.get(url,timeout=5)
        if response.status_code == 200:
            print(f'Application is UP. Status code: {response.status_code}')
            logging.info(f"Application is UP. Status code: {response.status_code}")
        else:
            print(f"Application is DOWN. Status code: {response.status_code}")
            logging.warning(f"Application is DoWN. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print("Application is DOWN. Unable to reach the server")
        logging.error(f"Application is DOWN. Exception {e}")

while True:
    check_health()
    time.sleep(10)




