# Load Balancer Project

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

## Project Structure

- `Load_balancer.py`: The main application file for the load balancer.
- `docker-compose.yml`: Docker Compose file to set up the load balancer and backend servers.
- `consistent_hash.py`: A module implementing the consistent hashing algorithm (not provided, assumed to be part of the project).

## Requirements

- Docker
- Docker Compose
- Python 3.x
- Flask
- docker (Python library)
- consistent_hash (Python library)

## Setup

### Clone the repository

```sh
git clone https://github.com/bogonkoEd/Distributed_Project.git
to run: docker-compose up --build
