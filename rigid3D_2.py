import streamlit as st
import numpy as np
from stl import mesh
import plotly.graph_objects as go
import tempfile

def generate_ruler_skeleton(num_points, rigidity_center, rigidity_end):
    center = num_points // 2
    rigidities = np.concatenate((
        np.linspace(rigidity_center, rigidity_end, num=center),
        np.linspace(rigidity_end, rigidity_center, num=num_points-center)
    ))
    return rigidities

def generate_ruler_positions(length, rigidity):
    center = length // 2
    positions = np.zeros(length)
    for i in range(center, length):
        distance_from_center = i - center
        positions[i] = positions[i-1] + np.log1p(distance_from_center) * rigidity[i]
    for i in range(center-1, -1, -1):
        distance_from_center = center - i
        positions[i] = positions[i+1] - np.log1p(distance_from_center) * rigidity[i]
    return positions

def apply_deformation(original_mesh, rigidities_x, rigidities_y, rigidities_z, stretch_factor_x, stretch_factor_y, stretch_factor_z):
    new_mesh = mesh.Mesh(np.copy(original_mesh.data), remove_empty_areas=False)
    
    x_min, y_min, z_min = np.min(new_mesh.vectors, axis=(0,1))
    x_max, y_max, z_max = np.max(new_mesh.vectors, axis=(0,1))
    
    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min
    
    for i in range(len(new_mesh.vectors)):
        for j in range(3):
            x = (new_mesh.vectors[i][j][0] - x_min) / x_range
            y = (new_mesh.vectors[i][j][1] - y_min) / y_range
            z = (new_mesh.vectors[i][j][2] - z_min) / z_range
            
            new_x = np.interp(x, np.linspace(0, 1, len(rigidities_x)), rigidities_x) * stretch_factor_x
            new_y = np.interp(y, np.linspace(0, 1, len(rigidities_y)), rigidities_y) * stretch_factor_y
            new_z = np.interp(z, np.linspace(0, 1, len(rigidities_z)), rigidities_z) * stretch_factor_z
            
            new_mesh.vectors[i][j][0] = new_x * x_range + x_min
            new_mesh.vectors[i][j][1] = new_y * y_range + y_min
            new_mesh.vectors[i][j][2] = new_z * z_range + z_min
    
    return new_mesh

def create_3d_plotly(original_mesh, modified_mesh, title="3D Object Deformation"):
    # Original mesh
    x1, y1, z1 = original_mesh.vectors.reshape(-1, 3).T
    i1, j1, k1 = np.arange(len(x1)).reshape(-1, 3).T

    # Modified mesh
    x2, y2, z2 = modified_mesh.vectors.reshape(-1, 3).T
    i2, j2, k2 = np.arange(len(x2)).reshape(-1, 3).T

    fig = go.Figure()

    # Add original mesh
    fig.add_trace(go.Mesh3d(x=x1, y=y1, z=z1, i=i1, j=j1, k=k1, opacity=0.5, color='blue', name='Original'))

    # Add modified mesh
    fig.add_trace(go.Mesh3d(x=x2, y=y2, z=z2, i=i2, j=j2, k=k2, opacity=0.5, color='red', name='Deformed'))

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
    )
    return fig

def main():
    st.title("3D Object with Nonlinear Rigidity")

    stl_file = st.file_uploader("Upload STL file", type=['stl'])

    if stl_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(stl_file.read())
            tmp_file_path = tmp_file.name

        original_mesh = mesh.Mesh.from_file(tmp_file_path)

        num_points = st.slider("Number of points for rigidity profile", min_value=10, max_value=500, value=100, step=10)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("X-axis")
            rigidity_center_x = st.slider("Rigidity at Center (X)", min_value=0.1, max_value=10.0, value=5.0, key='x_center')
            rigidity_end_x = st.slider("Rigidity at Ends (X)", min_value=0.1, max_value=10.0, value=2.0, key='x_end')
            stretch_factor_x = st.slider("Stretch Factor (X)", min_value=0.5, max_value=2.0, value=1.5, step=0.1, key='x_stretch')

        with col2:
            st.subheader("Y-axis")
            rigidity_center_y = st.slider("Rigidity at Center (Y)", min_value=0.1, max_value=10.0, value=5.0, key='y_center')
            rigidity_end_y = st.slider("Rigidity at Ends (Y)", min_value=0.1, max_value=10.0, value=2.0, key='y_end')
            stretch_factor_y = st.slider("Stretch Factor (Y)", min_value=0.5, max_value=2.0, value=1.5, step=0.1, key='y_stretch')

        with col3:
            st.subheader("Z-axis")
            rigidity_center_z = st.slider("Rigidity at Center (Z)", min_value=0.1, max_value=10.0, value=5.0, key='z_center')
            rigidity_end_z = st.slider("Rigidity at Ends (Z)", min_value=0.1, max_value=10.0, value=2.0, key='z_end')
            stretch_factor_z = st.slider("Stretch Factor (Z)", min_value=0.5, max_value=2.0, value=1.5, step=0.1, key='z_stretch')

        if st.button("Apply Deformation"):
            rigidities_x = generate_ruler_skeleton(num_points, rigidity_center_x, rigidity_end_x)
            rigidities_y = generate_ruler_skeleton(num_points, rigidity_center_y, rigidity_end_y)
            rigidities_z = generate_ruler_skeleton(num_points, rigidity_center_z, rigidity_end_z)

            modified_mesh = apply_deformation(original_mesh, rigidities_x, rigidities_y, rigidities_z, stretch_factor_x, stretch_factor_y, stretch_factor_z)

            fig_object = create_3d_plotly(original_mesh, modified_mesh, title="3D Object Deformation")
            st.plotly_chart(fig_object)

if __name__ == "__main__":
    main()
