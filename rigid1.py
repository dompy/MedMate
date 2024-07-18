import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def generate_ruler(length, rigidity):
    center = length // 2
    ruler = np.zeros(length)
    for i in range(length):
        distance_from_center = abs(center - i)
        if distance_from_center == 0:
            ruler[i] = 0
        else:
            ruler[i] = np.log(distance_from_center) * rigidity[distance_from_center]

    return ruler

def main():
    st.title("Logarithmic Resizable Ruler")

    # Slider for ruler length
    length = st.slider("Select Ruler Length", min_value=10, max_value=100, value=50, step=10)

    # Sliders for rigidity
    rigidity_center = st.slider("Select Rigidity at Center", min_value=1.0, max_value=10.0, value=5.0)
    rigidity_end = st.slider("Select Rigidity at Ends", min_value=1.0, max_value=10.0, value=2.0)

    rigidity = np.linspace(rigidity_center, rigidity_end, num=length//2)
    rigidity = np.concatenate((rigidity, rigidity[::-1]))

    ruler = generate_ruler(length, rigidity)

    # Plotting the ruler
    fig, ax = plt.subplots()
    ax.plot(ruler)
    ax.set_title("Logarithmic Resizable Ruler")
    ax.set_xlabel("Position on Ruler")
    ax.set_ylabel("Displacement")

    st.pyplot(fig)

if __name__ == "__main__":
    main()
