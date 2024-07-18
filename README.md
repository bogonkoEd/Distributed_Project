# Load Balancer Project

## Group Members
---
- 137192 Bogonko Eddy
- 137938 Martin Mwangi 
- 146013 Amanda Karani
- 139991 Glen Musa
- 146424 Masoud Hassan

## Project Description

This project implements a load balancer using Flask and Docker. The load balancer distributes incoming requests to a pool of backend servers based on a consistent hashing algorithm. This ensures efficient distribution of requests and improves the reliability and scalability of the system.

## Objectives

### 1. Efficient Request Distribution
The primary objective of this project is to distribute incoming client requests evenly across multiple backend servers. This prevents any single server from becoming a bottleneck and helps to handle higher loads effectively.

### 2. Fault Tolerance and High Availability
By using multiple backend servers, the system can continue to function even if one or more servers fail. The load balancer can detect these failures and redirect traffic to the healthy servers, ensuring high availability of the service.

### 3. Consistent Hashing
To achieve efficient request distribution and fault tolerance, the project employs a consistent hashing algorithm. This algorithm maps requests to servers in a way that minimizes reorganization when servers are added or removed, providing a stable distribution of load.

### 4. Scalability
The architecture allows easy scaling by simply adding more backend servers. The load balancer will automatically include these new servers into its routing algorithm, making it simple to handle increasing loads.

## Setup

### Requirements

- Docker
- Python 3.x
- Flask

### Clone the repository

```bash

git clone https://github.com/bogonkoEd/Distributed_Project.git

```
    
### Create a virtual environment and install dependencies

```bash

cd Distributed_Project    
python -m venv global
source global/bin/activate
pip install -r requirements.txt

```
### Run the load balancer

```bash
docker-compose up --build
```

Expect this output:

<img width="571" alt="docker_up" src="https://github.com/user-attachments/assets/93e8d073-9048-498b-a6ff-1e75266cf40e">

<img width="741" alt="Load_balancer" src="https://github.com/user-attachments/assets/95a5237a-e85a-440f-ad0e-986baa3b5374">


### Server

Check the load balancer is active by accessing:

    http://localhost:80/

Some useful links

Get distribution of incoming requests
    
    http://localhost:80/stats 

Make sure the load balancer is active by accessing:

    http://localhost:80/healthcheck 

Make sure the server is running by accessing:

    http://localhost:{server's port}/healthcheck

Plot distribution of recent requests (last 30 minutes)

    http://localhost:59987 

    

## Consistent Hashing Implementation

This code provides a consistent hashing algorithm to distribute requests (or data) across a cluster of servers efficiently and reliably. Consistent hashing is particularly valuable in distributed systems where servers might be added or removed dynamically.

### Hash Ring:

A dictionary (hash_ring) that maps hash values to server names.
Each server is represented multiple times on the ring as "virtual nodes" to enhance distribution evenness.

### Server Management:

Tracks the actual server names in a list (server_names) for maintenance purposes.
Monitors request distribution by counting requests per server (server_requests).

### Key Functions
   - **add_server(server_name)**:
    Introduces a new server to the system.
    Creates multiple virtual nodes for the server, each hashed to a distinct location on the ring.
    <img width="275" alt="Add_server" src="https://github.com/user-attachments/assets/f0fa36dd-c5d8-4d43-ac7f-8043ee5a29dc">

   - **remove_server(server_name)**:
    Takes a server out of operation.Removes all its virtual nodes and associated request tracking.
    
- **get_server(request_id)**:
Hashes the request ID.Locates the closest server (or its virtual node) on the hash ring in a clockwise direction from the hash value.Assigns the request to that server and updates its request count.


## Load Balancer Analysis
---
### Load Test 

Bundled together with this project is a python script, **sim.py** to simulate many parallel HTTP requests to the Load Balancer, in our case we tried 1000 requests. Logs directory is created by the Load Balancer to keep track of the HTTP requests and the servers at served them.
<img width="575" alt="Load_test" src="https://github.com/user-attachments/assets/f0c8f5b0-3b11-4763-bf15-3618d7693d26">

### Load Distribution

Bundled together with this project is a python script to analysis the distribution of requests on servers in hash ring. It analyse the logs file.  
We used a browser extension, URL Loader, in order to capture the requests in the requests.log.
<img width="253" alt="Distro_test" src="https://github.com/user-attachments/assets/55b0d94d-53a7-4341-a883-f6c6e14c54c8">
The plotted results: 
![newplot](https://github.com/user-attachments/assets/f01b0f73-579e-41a0-960c-c2a19fb23fc8)



