import json
from collections import Counter
import plotly.graph_objects as go

def read_log_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def parse_log(log_lines):
    servers = []
    for line in log_lines:
        log_data = json.loads(line)
        if "message" in log_data:
            nested_data = json.loads(log_data["message"])
            servers.append(nested_data["server"]) 

    return servers

def generate_graph(servers):
    server_counts = Counter(servers)
    total_requests = sum(server_counts.values())

    server_names = list(server_counts.keys())
    request_counts = list(server_counts.values())
    percentages = [(count / total_requests) * 100 for count in request_counts]

    # Create Pie Chart
    fig = go.Figure(data=[go.Pie(labels=server_names, values=request_counts, textinfo='percent+label')])
    fig.update_layout(title_text='Request Distribution Among Servers')

    # Show the chart
    fig.show()

if __name__ == "__main__":
    log_file = read_log_file("logs/requests.log")
    servers = parse_log(log_file)
    generate_graph(servers)
