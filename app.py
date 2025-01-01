import os
from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('healthcare_dataset.csv')

# Ensure Billing Amount column is numeric
df['Billing Amount'] = df['Billing Amount'].str.replace('$', '', regex=False).astype(float)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get filter values from user input
    min_value = float(request.args.get('min_value', 0))
    max_value = float(request.args.get('max_value', df['Billing Amount'].max()))

    # Filter the dataset based on user input
    filtered_df = df[(df['Billing Amount'] >= min_value) & (df['Billing Amount'] <= max_value)]

    # Create the histogram with formatted axis labels
    fig = px.histogram(
        filtered_df, 
        x='Billing Amount', 
        title="Healthcare Costs Distribution", 
        nbins=50
    )
    fig.update_layout(
        xaxis_title='Billing Amount ($)',  # Add dollar sign to axis label
        yaxis_title='Count',
        xaxis_tickformat='$'  # Format x-axis tick labels with a dollar sign
    )

    # Convert the Plotly figure to HTML
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Ensure app listens on port 10000 for Render
    app.run(host='0.0.0.0', port=port, debug=True)
