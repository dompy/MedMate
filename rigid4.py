import streamlit as st
import numpy as np
from stl import Mesh
import plotly.graph_objects as go
import tempfile
import matplotlib.pyplot as plt

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

def modify_stl_ruler(stl_mesh, positions, scale_factor):
    new_mesh = Mesh(np.copy(stl_mesh.data), remove_empty_areas=False)
    center = len(positions) // 2
    for vertex in new_mesh.vectors.reshape(-1, 3):
        x_original = vertex[0]
        if int(x_original) in range(len(positions)):
            distance_from_center = abs(center - x_original)
            scaling = scale_factor * np.log1p(distance_from_center) * positions[int(abs(center - x_original))]
            if x_original < center:
                vertex[0] -= scaling
            else:
                vertex[0] += scaling
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

def main():
    st.title("3D Ruler with Nonlinear Rigidity")

    # File uploader for STL file
    stl_file = st.file_uploader("Upload STL file", type=['stl'])

    if stl_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(stl_file.read())
            tmp_file_path = tmp_file.name

        stl_mesh = Mesh.from_file(tmp_file_path)

        length = 100  # Assuming ruler length to be 100 units
        rigidity_center = st.slider("Select Rigidity at Center", min_value=1.0, max_value=10.0, value=5.0)
        rigidity_end = st.slider("Select Rigidity at Ends", min_value=1.0, max_value=10.0, value=2.0)
        stretch_factor = st.slider("Select Stretch Factor", min_value=-2.0, max_value=2.0, value=0.0, step=0.1)

        rigidity = np.linspace(rigidity_center, rigidity_end, num=length//2)
        rigidity = np.concatenate((rigidity, rigidity[::-1]))

        positions = generate_ruler_positions(length, rigidity)

        modified_stl_mesh = modify_stl_ruler(stl_mesh, positions, stretch_factor)

        fig_ruler = create_3d_plotly(modified_stl_mesh, title="3D Ruler with Nonlinear Rigidity")
        st.plotly_chart(fig_ruler)

        fig_rigidities, ax_rigidities = plt.subplots()
        ax_rigidities.plot(rigidity, label='Rigidity Profile', color='g')
        ax_rigidities.set_title("Rigidity Profile of the Ruler")
        ax_rigidities.set_xlabel("Position on Ruler")
        ax_rigidities.set_ylabel("Rigidity")
        ax_rigidities.legend()
        st.pyplot(fig_rigidities)

if __name__ == "__main__":
    main()
