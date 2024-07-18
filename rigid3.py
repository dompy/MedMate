import streamlit as st
import numpy as np
from stl import Mesh
import plotly.graph_objects as go
import tempfile

def generate_ruler_positions(length, rigidity):
    center = length // 2
    positions = np.zeros(length)
    for i in range(center, length):
        distance_from_center = i - center
        positions[i] = positions[i-1] + np.log1p(distance_from_center) * rigidity[distance_from_center]
    for i in range(center-1, -1, -1):
        distance_from_center = center - i
        positions[i] = positions[i+1] - np.log1p(distance_from_center) * rigidity[distance_from_center]
    return positions

def modify_stl_ruler(stl_mesh, positions):
    # Assume the ruler is aligned along the x-axis and we modify only the y-axis based on positions
    new_mesh = Mesh(np.copy(stl_mesh.data), remove_empty_areas=False)
    for vertex in new_mesh.vectors.reshape(-1, 3):
        x = int(vertex[0])
        if x >= 0 and x < len(positions):
            vertex[1] += positions[x] * 0.1  # Scale the displacement to avoid extreme deformations
    return new_mesh

def create_3d_plotly(stl_mesh, title="3D Ruler with Logarithmic Rigidity"):
    # Extract the points and faces
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
            aspectratio=dict(x=0.4, y=4 , z=0.1)  # Adjust aspect ratio for better visualization
        ),
    )
    return fig

def create_vertices_plotly(stl_mesh, title="Vertices Positions"):
    # Extract the points
    x, y, z = stl_mesh.vectors.reshape(-1, 3).T

    fig = go.Figure(data=[
        go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=2, color='blue'))
    ])

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectratio=dict(x=0.4, y=4 , z=0.1)  # Adjust aspect ratio for better visualization
        ),
    )
    return fig

def main():
    st.title("3D Ruler with Logarithmic Rigidity")

    # File uploader for STL file
    stl_file = st.file_uploader("Upload STL file", type=['stl'])

    if stl_file:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(stl_file.read())
            tmp_file_path = tmp_file.name

        stl_mesh = Mesh.from_file(tmp_file_path)

        # Slider for rigidity
        length = 100  # Assuming ruler length to be 100 units
        rigidity_center = st.slider("Select Rigidity at Center", min_value=1.0, max_value=10.0, value=5.0)
        rigidity_end = st.slider("Select Rigidity at Ends", min_value=1.0, max_value=10.0, value=2.0)

        rigidity = np.linspace(rigidity_center, rigidity_end, num=length//2)
        rigidity = np.concatenate((rigidity, rigidity[::-1]))

        positions = generate_ruler_positions(length, rigidity)

        modified_stl_mesh = modify_stl_ruler(stl_mesh, positions)  # Use a new mesh for modifications

        fig_ruler = create_3d_plotly(modified_stl_mesh, title="3D Ruler with Logarithmic Rigidity")
        st.plotly_chart(fig_ruler)

        fig_vertices = create_vertices_plotly(modified_stl_mesh, title="Vertices Positions with Selected Rigidity")
        st.plotly_chart(fig_vertices)

if __name__ == "__main__":
    main()
