# visualization.py

import plotly.graph_objects as go
from config.config import *

def plot_sector_returns(sector_data):

    fig = go.Figure()
    for sector_name, data in sector_data.items():
        fig.add_trace(go.Scatter(x=data["date"], y=data["Weighted Value"],
                                 mode="lines", name=sector_name))

    fig.update_layout(
        title="Crypto Sectors Performance Comparison",
        xaxis_title="Date",
        yaxis_title=f"Indexed Value (Start={WEIGHTED_PRICE_BASE})",
        template="plotly_dark"
    )
    fig.show()