import plotly.graph_objects as go

def generate_request_distribution_graph(server_requests):
    fig = go.Figure(data=[go.Bar(x=list(server_requests.keys()), y=list(server_requests.values()))])
    fig.update_layout(
        title="Request Distribution Among Servers",
        xaxis_title="Server Name",
        yaxis_title="Number of Requests"
    )
    return fig.to_html(full_html=False)  # Return HTML for embedding in your app
