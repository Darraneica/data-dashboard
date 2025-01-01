from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('healthcare_dataset.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default filter values
    min_value = float(request.args.get('min_value', 0))  # Default min value is 0
    max_value = float(request.args.get('max_value', df['Billing Amount'].max()))  # Default max value is the highest billing amount

    # Filter the data based on the user input
    filtered_df = df[(df['Billing Amount'] >= min_value) & (df['Billing Amount'] <= max_value)]

    # Create an interactive histogram plot using Plotly
    fig = px.histogram(filtered_df, x='Billing Amount', title="Healthcare Costs Distribution", nbins=50)
    
    # Convert plot to HTML to embed in the template
    graph_html = pio.to_html(fig, full_html=False)
    
    # Return the HTML page with the plot
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
