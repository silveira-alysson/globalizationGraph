import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Mechanism Interaction Model", layout="wide")

# Center the graphs by creating 3 columns and using the middle one (approx 1/3 width)
left_space, center_col, right_space = st.columns([1, 1, 1])

with center_col:
    st.title("Mechanism Interaction")
    
    # 1. Control Slider
    x_limit = st.slider("Move Slider", 0.0, 6.0, 1.0, step=1.0)

    # 2. Data Preparation
    x_full = np.linspace(0.1, 6.0, 500)
    x_revealed = x_full[x_full <= x_limit]

    def pos_func(x): return 3.5*np.log((x+1)*0.5) + 1
    def neg_func(x): return 0.1*np.exp(x*0.7) - 0.1

    # Pre-calculate full data for static graphs
    y_pos_full = pos_func(x_full)
    y_neg_full = neg_func(x_full)
    
    # Calculate revealed data for the resultant
    y_res_revealed = pos_func(x_revealed) - neg_func(x_revealed)

    # 3. Updated Plotting Helper with y_range support
    def create_plot(x, y, title, color, show_slider=True, y_range=None):
        fig = go.Figure()
        
        # Add the line trace
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=3)))
        
        # Add the vertical 'slider' line to the first two graphs
        if show_slider:
            fig.add_vline(x=x_limit, line_width=2, line_dash="dash", line_color="black")
            
        # Define Y-Axis dictionary
        y_axis_config = dict(zeroline=True, zerolinewidth=1, zerolinecolor='LightGrey', fixedrange=True)
        if y_range:
            y_axis_config['range'] = y_range

        fig.update_layout(
            title=title,
            height=250,
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis=dict(range=[0, 6.5], fixedrange=True),
            yaxis=y_axis_config,
            showlegend=False
        )
        return fig

    # 4. Display Stacking Vertically
    # Top and Middle: Full view with the vertical tracking line
    st.plotly_chart(create_plot(x_full, y_pos_full, "Supply Chain Responsiveness (Positive Mechanism)", "#2E7D32", y_range=[0, 6]) , use_container_width=True)
    st.plotly_chart(create_plot(x_full, y_neg_full, "Operations Complexity (Negative Mechanism)", "#C62828",  y_range=[0, 6]) , use_container_width=True)
    
    # Bottom: Revealed view with fixed Y-axis [0, 4]
    st.plotly_chart(create_plot(x_revealed, y_res_revealed, "Globalization Performance (Foreign Profits)", "#1565C0", show_slider=False, y_range=[0, 6]), use_container_width=True)