import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("POD has started.")
    logging.info("Remeber that this container is not doing nothing.")
    logging.info("All the job is done by cronjob containers.")

    # Keep the pod running indefinitely
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()