import json
from collections import Counter
import plotly.graph_objects as go

def read_log_file(filename):
    """Reads log file and returns its contents as a list of lines."""
    with open(filename, 'r') as file:
        return file.readlines()

def parse_log(log_lines):
    """Parses log lines and returns a dictionary of server names to request counts."""
    server_requests = {}
    for line in log_lines:
        log_data = json.loads(line)
        server_name = log_data.get("server")
        if server_name:
            server_requests[server_name] = server_requests.get(server_name, 0) + 1 
    return server_requests

def generate_graph(server_requests):
    """Generates a bar graph from the server request data."""
    server_names = list(server_requests.keys())
    request_counts = list(server_requests.values())

    fig = go.Figure(data=[go.Bar(x=server_names, y=request_counts, text=request_counts, textposition='auto')])
    fig.update_layout(title_text='Request Distribution Among Servers', xaxis_title='Server Name', yaxis_title='Number of Requests')
    fig.show()


if __name__ == "__main__":
    log_file = read_log_file("logs/requests.log")
    server_requests = parse_log(log_file)
    generate_graph(server_requests)
