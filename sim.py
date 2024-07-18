import requests
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor

LOAD_BALANCER_URL = "http://localhost/" 
NUM_REQUESTS = 1000
PATHS = ["/"]  

# Function to generate request data (optional)
# Function to send a single request
def send_request(thread_id):
    full_url = LOAD_BALANCER_URL
    method = "GET"

    try:
        response = requests.request(method, full_url, allow_redirects=True)
        response.raise_for_status()
        print(f"Thread {thread_id}: {method} to '{full_url}' successful ({response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Thread {thread_id}: {method} to '{full_url}' failed: {e}")

# Load testing function (with improvements)
def load_test():
    with ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
        # Use list comprehension for clarity and potential efficiency
        futures = [executor.submit(send_request, i) for i in range(NUM_REQUESTS)]

        # Optionally, process results as they come in (for real-time monitoring)
        for future in futures:
            future.result()  # This will block until the request completes

if __name__ == "__main__":
    start_time = time.time()
    load_test()
    end_time = time.time()
    print(f"\nLoad test completed in {end_time - start_time:.2f} seconds")
