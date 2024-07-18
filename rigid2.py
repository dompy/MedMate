import streamlit as st
import numpy as np
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

def main():
    st.title("Logarithmic Resizable Ruler with Centimeter Markings")

    # Slider for ruler length
    length = st.slider("Select Ruler Length (in cm)", min_value=10, max_value=100, value=50, step=10)

    # Sliders for rigidity
    rigidity_center = st.slider("Select Rigidity at Center", min_value=1.0, max_value=10.0, value=5.0)
    rigidity_end = st.slider("Select Rigidity at Ends", min_value=1.0, max_value=10.0, value=2.0)

    rigidity = np.linspace(rigidity_center, rigidity_end, num=length//2)
    rigidity = np.concatenate((rigidity, rigidity[::-1]))

    positions = generate_ruler_positions(length, rigidity)

    # Plotting the ruler with centimeter markings
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.plot(positions, np.zeros(length), 'bo-')  # Ruler as a line with points
    for i in range(length):
        ax.text(positions[i], 0.1, str(i - length//2), ha='center', va='bottom', fontsize=8)

    ax.set_title("Logarithmic Resizable Ruler")
    ax.set_xlabel("Position on Ruler")
    ax.set_yticks([])
    ax.axvline(x=positions[length//2], color='r', linestyle='--', label='Center')
    ax.legend()

    st.pyplot(fig)

    # Visualization of flexibility
    fig_flex, ax_flex = plt.subplots()
    ax_flex.plot(rigidity, label='Rigidity Profile', color='g')
    ax_flex.set_title("Rigidity Profile of the Ruler")
    ax_flex.set_xlabel("Position on Ruler")
    ax_flex.set_ylabel("Rigidity")
    ax_flex.legend()

    st.pyplot(fig_flex)

if __name__ == "__main__":
    main()
