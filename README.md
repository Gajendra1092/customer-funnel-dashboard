<div align="center">

<h1><b>E-commerce Checkout Funnel Analysis & Dashboard</b></h1>
Synthetic funnel analysis + Streamlit dashboard showing conversion drops and AOV.

<p>
<a href="https://www.python.org/downloads/">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3.9%252B-blue.svg" alt="Python Version">
</a>
<a href="https://streamlit.io">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Streamlit-1.25%252B-brightgreen.svg" alt="Streamlit Version">
</a>
<a href="https://opensource.org/licenses/MIT">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</a>
</p>
</div>

<h2><b>📊 Dashboard Preview</b></h2>
(Add a screenshot or GIF of the dashboard here)

<div align="center">
<img src="https://www.google.com/search?q=https://placehold.co/800x400/2d3748/ffffff%3Ftext%3DDashboard%2BPreview" alt="Dashboard Screenshot">
</div>

<h2><b>✨ Features</b></h2>
<table>
<tr>
<td width="50%">
<p><b>Key Metrics</b></p>
<p>At-a-glance view of total visitors, carts created, purchases, and total revenue.</p>
</td>
<td width="50%">
<p><b>Interactive Funnel Chart</b></p>
<p>Visualize the user journey from visit to purchase and identify drop-off points.</p>
</td>
</tr>
<tr>
<td width="50%">
<p><b>Revenue Trend Analysis</b></p>
<p>A line chart showing revenue performance over any selected period.</p>
</td>
<td width="50%">
<p><b>Dynamic Filtering</b></p>
<p>Filter the entire dashboard by date range and city tier for granular insights.</p>
</td>
</tr>
</table>

<h2><b>🚀 Run</b></h2>
Follow these instructions to get a copy of the project up and running on your local machine.

<h4><b>Prerequisites</b></h4>

Python 3.9 or higher

pip and venv

<h4><b>Installation</b></h4>
<ol>
<li><p><b>Clone the repository:</b></p>
<pre><code>git clone https://www.google.com/search?q=https://github.com/your-username/customer-funnel-dashboard.git
cd customer-funnel-dashboard</code></pre>
</li>
<li><p><b>Create and activate the virtual environment:</b></p>
<pre><code>python -m venv venv && source venv/bin/activate</code></pre>
</li>
<li><p><b>Install the required dependencies:</b></p>
<pre><code>pip install -r requirements.txt</code></pre>
</li>
<li><p><b>Generate the synthetic dataset:</b></p>
<pre><code>python generate_data.py</code></pre>
</li>
<li><p><b>Run the Streamlit application:</b></p>
<pre><code>streamlit run app.py</code></pre>
</li>
</ol>

<h2><b>📂 What's Inside</b></h2>
<pre>
.
├── app.py                      # Interactive dashboard
├── data/
│   └── events.csv              # Synthetic events
│   └── sample_ecommerce_data.csv              # Synthetic events
├── notebooks/
│   └── funnel_analysis.ipynb   # Analysis & insights
└── docs/
│   └──BRD.md                  # BA artifacts
├── generate_data.py           # Generates Data
├── requirements.txt           # Required Packages
</pre>