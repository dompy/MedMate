import streamlit as st
import numpy as np
from stl import Mesh
import plotly.graph_objects as go
import tempfile

def generate_ruler_skeleton(num_points, rigidity_center, rigidity_end):
    center = num_points // 2
    rigidities = np.concatenate((
        np.linspace(rigidity_center, rigidity_end, num=center),
        np.linspace(rigidity_end, rigidity_center, num=num_points-center)
    ))
    return rigidities

def generate_ruler_positions(length, rigidity, stretch_factor):
    center = length // 2
    positions = np.zeros(length)
    for i in range(center, length):
        distance_from_center = i - center
        positions[i] = positions[i-1] + np.log1p(distance_from_center) * rigidity[distance_from_center]
    for i in range(center-1, -1, -1):
        distance_from_center = center - i
        positions[i] = positions[i+1] - np.log1p(distance_from_center) * rigidity[distance_from_center]
    
    # Apply stretch factor
    positions = positions * stretch_factor
    return positions

def apply_resizing(original_mesh, positions):
    new_mesh = Mesh(np.copy(original_mesh.data), remove_empty_areas=False)
    length = len(positions)
    
    for vertex in new_mesh.vectors.reshape(-1, 3):
        x = int(vertex[0])
        if 0 <= x < length:
            new_x = positions[x]
            vertex[0] = new_x
    
    return new_mesh

def create_3d_plotly(stl_mesh, title="3D Ruler with Nonlinear Rigidity"):
    x, y, z = stl_mesh.vectors.reshape(-1, 3).T
    I, J, K = np.arange(len(x)).reshape(-1, 3).T

    fig = go.Figure(data=[
        go.Mesh3d(x=x, y=y, z=z, i=I, j=J, k=K, opacity=0.7)
    ])

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectratio=dict(x=2, y=0.2, z=0.1)
        ),
    )
    return fig

def visualize_ruler_behavior(original_positions, new_positions):
    fig = go.Figure()
    
    # Original ruler
    fig.add_trace(go.Scatter(x=original_positions, y=np.zeros_like(original_positions),
                             mode='lines+markers', name='Original Ruler',
                             line=dict(color='blue', width=2)))
    
    # Resized ruler
    fig.add_trace(go.Scatter(x=new_positions, y=np.ones_like(new_positions),
                             mode='lines+markers', name='Resized Ruler',
                             line=dict(color='red', width=2)))
    
    # Connecting lines
    for i in range(len(original_positions)):
        fig.add_trace(go.Scatter(x=[original_positions[i], new_positions[i]], 
                                 y=[0, 1], mode='lines', 
                                 line=dict(color='gray', width=1), 
                                 showlegend=False))
    
    fig.update_layout(title="Ruler Behavior Visualization",
                      xaxis_title="Position",
                      yaxis_title="",
                      yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Original', 'Resized']),
                      height=400)
    
    return fig

def main():
    st.title("3D Ruler with Nonlinear Rigidity")

    stl_file = st.file_uploader("Upload STL file", type=['stl'])

    if stl_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(stl_file.read())
            tmp_file_path = tmp_file.name

        original_mesh = Mesh.from_file(tmp_file_path)

        length = int(original_mesh.vectors[:,:,0].max() - original_mesh.vectors[:,:,0].min())
        
        num_points = st.slider("Number of points for rigidity profile", min_value=10, max_value=500, value=100, step=10)
        rigidity_center = st.slider("Select Rigidity at Center", min_value=1.0, max_value=10.0, value=5.0)
        rigidity_end = st.slider("Select Rigidity at Ends", min_value=1.0, max_value=30.0, value=2.0)
        stretch_factor = st.slider("Select Stretch Factor", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

        rigidities = generate_ruler_skeleton(num_points, rigidity_center, rigidity_end)
        original_positions = np.linspace(0, length, num_points)
        new_positions = generate_ruler_positions(num_points, rigidities, stretch_factor)


        modified_mesh = apply_resizing(original_mesh, new_positions)

        fig_ruler = create_3d_plotly(modified_mesh, title="3D Ruler with Nonlinear Rigidity")
        st.plotly_chart(fig_ruler)

        # Visualization of rigidity profile
        fig_rigidities = go.Figure(data=[
            go.Scatter(x=np.arange(len(rigidities)), y=rigidities, mode='lines', name='Rigidity')
        ])
        fig_rigidities.update_layout(title="Rigidity Profile", xaxis_title="Position", yaxis_title="Rigidity")
        st.plotly_chart(fig_rigidities)

        # Visualization of ruler behavior
        fig_behavior = visualize_ruler_behavior(original_positions, new_positions)
        st.plotly_chart(fig_behavior)

if __name__ == "__main__":
    main()