# Load Balancer Project

This project implements a simple load balancer using Flask and Docker. The load balancer distributes incoming requests to a pool of backend servers based on a consistent hashing algorithm.

## Project Structure

- `Load_balancer.py`: The main application file for the load balancer.
- `docker-compose.yml`: Docker Compose file to set up the load balancer and backend servers.

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
git clone https://github.com/your-repo/load-balancer.git
cd load-balancer
