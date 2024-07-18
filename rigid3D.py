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

def generate_ruler_positions(num_points, rigidity, stretch_factor):
    center = num_points // 2
    positions = np.zeros(num_points)
    for i in range(center, num_points):
        distance_from_center = i - center
        positions[i] = positions[i-1] + np.log1p(distance_from_center) * rigidity[distance_from_center]
    for i in range(center-1, -1, -1):
        distance_from_center = center - i
        positions[i] = positions[i+1] - np.log1p(distance_from_center) * rigidity[distance_from_center]
    
    positions = positions * stretch_factor
    return positions

def apply_resizing(original_mesh, positions_x, positions_y, positions_z):
    new_mesh = Mesh(np.copy(original_mesh.data), remove_empty_areas=False)
    
    x_min, y_min, z_min = np.min(new_mesh.vectors, axis=(0,1))
    x_max, y_max, z_max = np.max(new_mesh.vectors, axis=(0,1))
    
    for vertex in new_mesh.vectors.reshape(-1, 3):
        x_index = int((vertex[0] - x_min) / (x_max - x_min) * (len(positions_x) - 1))
        y_index = int((vertex[1] - y_min) / (y_max - y_min) * (len(positions_y) - 1))
        z_index = int((vertex[2] - z_min) / (z_max - z_min) * (len(positions_z) - 1))
        
        vertex[0] = positions_x[x_index]
        vertex[1] = positions_y[y_index]
        vertex[2] = positions_z[z_index]
    
    return new_mesh

def create_3d_plotly(stl_mesh, title="3D Object with Nonlinear Rigidity"):
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
            aspectmode='data'
        ),
    )
    return fig

def visualize_rigidity_profiles(rigidities_x, rigidities_y, rigidities_z):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(y=rigidities_x, mode='lines', name='X-axis Rigidity'))
    fig.add_trace(go.Scatter(y=rigidities_y, mode='lines', name='Y-axis Rigidity'))
    fig.add_trace(go.Scatter(y=rigidities_z, mode='lines', name='Z-axis Rigidity'))
    
    fig.update_layout(title="Rigidity Profiles",
                      xaxis_title="Position",
                      yaxis_title="Rigidity")
    
    return fig

def create_2d_grid_deformation(positions_x, positions_y, original_length):
    num_points = 10  # Adjust this for more or fewer arrows
    x = np.linspace(0, original_length, num_points)
    y = np.linspace(0, original_length, num_points)
    X, Y = np.meshgrid(x, y)
    
    U = np.interp(X.flatten(), np.linspace(0, original_length, len(positions_x)), positions_x) - X.flatten()
    V = np.interp(Y.flatten(), np.linspace(0, original_length, len(positions_y)), positions_y) - Y.flatten()
    
    fig = go.Figure()

    # Add scatter plot for grid points
    fig.add_trace(go.Scatter(
        x=X.flatten(),
        y=Y.flatten(),
        mode='markers',
        marker=dict(size=5, color='blue'),
        name='Grid Points'
    ))

    # Add arrows
    for i in range(len(X.flatten())):
        fig.add_trace(go.Scatter(
            x=[X.flatten()[i], X.flatten()[i] + U[i]],
            y=[Y.flatten()[i], Y.flatten()[i] + V[i]],
            mode='lines',
            line=dict(color='red', width=1),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[X.flatten()[i] + U[i]],
            y=[Y.flatten()[i] + V[i]],
            mode='markers',
            marker=dict(symbol='triangle-up', size=8, color='red', angle=np.arctan2(V[i], U[i])*180/np.pi - 90),
            showlegend=False
        ))

    fig.update_layout(
        title="2D Grid Deformation",
        xaxis_title="X",
        yaxis_title="Y",
        xaxis=dict(range=[0, original_length]),
        yaxis=dict(range=[0, original_length]),
        showlegend=False
    )

    return fig

def create_1d_deformation_plot(original_positions, new_positions):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=original_positions, y=new_positions, mode='lines', name='Deformation'))
    fig.add_trace(go.Scatter(x=original_positions, y=original_positions, mode='lines', name='Original', line=dict(dash='dash')))
    fig.update_layout(title="1D Deformation", xaxis_title="Original Position", yaxis_title="New Position")
    return fig

def create_3d_vector_field(positions_x, positions_y, positions_z, original_length):
    num_points = 4  # Increase this for more arrows, but it may slow down the visualization
    x = np.linspace(0, original_length, num_points)
    y = np.linspace(0, original_length, num_points)
    z = np.linspace(0, original_length, num_points)
    X, Y, Z = np.meshgrid(x, y, z)

    U = np.interp(X.flatten(), np.linspace(0, original_length, len(positions_x)), positions_x) - X.flatten()
    V = np.interp(Y.flatten(), np.linspace(0, original_length, len(positions_y)), positions_y) - Y.flatten()
    W = np.interp(Z.flatten(), np.linspace(0, original_length, len(positions_z)), positions_z) - Z.flatten()

    # Scale up the deformation vectors to make them more visible
    scale_factor = original_length / 5  # Adjust this value to change the size of the arrows
    U *= scale_factor
    V *= scale_factor
    W *= scale_factor

    fig = go.Figure()

    # Add scatter points for the grid
    fig.add_trace(go.Scatter3d(
        x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
        mode='markers',
        marker=dict(size=2, color='blue'),
        name='Grid Points'
    ))

    # Add arrows to show deformation
    for i in range(len(X.flatten())):
        fig.add_trace(go.Scatter3d(
            x=[X.flatten()[i], X.flatten()[i] + U[i]],
            y=[Y.flatten()[i], Y.flatten()[i] + V[i]],
            z=[Z.flatten()[i], Z.flatten()[i] + W[i]],
            mode='lines',
            line=dict(color='red', width=3),
            showlegend=False
        ))

    # Add a wireframe cube to represent the original object boundaries
    cube_edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # bottom face
        [4, 5], [5, 6], [6, 7], [7, 4],  # top face
        [0, 4], [1, 5], [2, 6], [3, 7]   # vertical edges
    ]
    
    for edge in cube_edges:
        fig.add_trace(go.Scatter3d(
            x=[0, original_length] if edge[0] % 4 == edge[1] % 4 else [0, 0] if edge[0] < 4 else [original_length, original_length],
            y=[0, original_length] if abs(edge[0] - edge[1]) == 1 else [0, 0] if edge[0] % 2 == 0 else [original_length, original_length],
            z=[0, 0] if edge[0] < 4 else [original_length, original_length],
            mode='lines',
            line=dict(color='rgb(70,70,70)', width=2),
            showlegend=False
        ))

    fig.update_layout(
        title="3D Deformation Vector Field",
        scene=dict(
            aspectmode='cube',
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        )
    )

    return fig

def main():
    st.title("3D Object with Nonlinear Rigidity")

    stl_file = st.file_uploader("Upload STL file", type=['stl'])

    if stl_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(stl_file.read())
            tmp_file_path = tmp_file.name

        original_mesh = Mesh.from_file(tmp_file_path)

        # Calculate the original length as the maximum dimension of the object
        original_length = np.max(original_mesh.vectors.max(axis=(0,1)) - original_mesh.vectors.min(axis=(0,1)))

        num_points = st.slider("Number of points for rigidity profile", min_value=10, max_value=500, value=100, step=10)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("X-axis")
            rigidity_center_x = st.slider("Rigidity at Center (X)", min_value=1.0, max_value=10.0, value=5.0, key='x_center')
            rigidity_end_x = st.slider("Rigidity at Ends (X)", min_value=1.0, max_value=10.0, value=2.0, key='x_end')
            stretch_factor_x = st.slider("Stretch Factor (X)", min_value=0.5, max_value=2.0, value=1.0, step=0.1, key='x_stretch')

        with col2:
            st.subheader("Y-axis")
            rigidity_center_y = st.slider("Rigidity at Center (Y)", min_value=1.0, max_value=10.0, value=5.0, key='y_center')
            rigidity_end_y = st.slider("Rigidity at Ends (Y)", min_value=1.0, max_value=10.0, value=2.0, key='y_end')
            stretch_factor_y = st.slider("Stretch Factor (Y)", min_value=0.5, max_value=2.0, value=1.0, step=0.1, key='y_stretch')

        with col3:
            st.subheader("Z-axis")
            rigidity_center_z = st.slider("Rigidity at Center (Z)", min_value=1.0, max_value=10.0, value=5.0, key='z_center')
            rigidity_end_z = st.slider("Rigidity at Ends (Z)", min_value=1.0, max_value=10.0, value=2.0, key='z_end')
            stretch_factor_z = st.slider("Stretch Factor (Z)", min_value=0.5, max_value=2.0, value=1.0, step=0.1, key='z_stretch')

        rigidities_x = generate_ruler_skeleton(num_points, rigidity_center_x, rigidity_end_x)
        rigidities_y = generate_ruler_skeleton(num_points, rigidity_center_y, rigidity_end_y)
        rigidities_z = generate_ruler_skeleton(num_points, rigidity_center_z, rigidity_end_z)

        original_positions = np.linspace(0, original_length, num_points)

        positions_x = generate_ruler_positions(num_points, rigidities_x, stretch_factor_x)
        positions_y = generate_ruler_positions(num_points, rigidities_y, stretch_factor_y)
        positions_z = generate_ruler_positions(num_points, rigidities_z, stretch_factor_z)

        modified_mesh = apply_resizing(original_mesh, positions_x, positions_y, positions_z)

        fig_object = create_3d_plotly(modified_mesh, title="3D Object with Nonlinear Rigidity")
        st.plotly_chart(fig_object)

        fig_rigidities = visualize_rigidity_profiles(rigidities_x, rigidities_y, rigidities_z)
        st.plotly_chart(fig_rigidities)

        # New visualizations
        st.subheader("2D Grid Deformation")
        col1, col2, col3 = st.columns(3)
        with col1:
            fig_xy = create_2d_grid_deformation(positions_x, positions_y, original_length)
            st.plotly_chart(fig_xy)
        with col2:
            fig_xz = create_2d_grid_deformation(positions_x, positions_z, original_length)
            st.plotly_chart(fig_xz)
        with col3:
            fig_yz = create_2d_grid_deformation(positions_y, positions_z, original_length)
            st.plotly_chart(fig_yz)

        st.subheader("1D Deformation")
        col1, col2, col3 = st.columns(3)
        with col1:
            fig_x = create_1d_deformation_plot(original_positions, positions_x)
            st.plotly_chart(fig_x)
        with col2:
            fig_y = create_1d_deformation_plot(original_positions, positions_y)
            st.plotly_chart(fig_y)
        with col3:
            fig_z = create_1d_deformation_plot(original_positions, positions_z)
            st.plotly_chart(fig_z)

        st.subheader("3D Deformation Vector Field")
        fig_3d_vector = create_3d_vector_field(positions_x, positions_y, positions_z, original_length)
        st.plotly_chart(fig_3d_vector)

if __name__ == "__main__":
    main()