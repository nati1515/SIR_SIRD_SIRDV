#-----------------------------------------------------------------------------------------------------------------------
# Name: Natnael Kassahun
# Date: 04/30/2025
# BIOS 584 Assignment 4 Application 2 (VIBE codig)
#-----------------------------------------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import mplcursors  # For hover-based interactivity
import subprocess  # For managing command-line calls


#comment 1:  This function establishes the layout of the main window. It creates input fields for parameters like beta, gamma, days, death rate,
# and vaccination rate on the left side, a dropdown menu for model selection, and a button to trigger the simulation. On the right side, it sets up
# a Matplotlib plot area for displaying simulation results, along with a navigation toolbar for interactivity.
#Changes made:
# 1. **Class Removed**: Replaced the class-based design with standalone functions (`create_simulation_window`, `create_label_and_entry`, `run_simulation`, etc.).
# 2. **Separation of Concerns**: Each function focuses on a single responsibility (e.g., creating the plot area, retrieving inputs, or running simulations).
# 3. **Matplotlib Integration**: The `ax` and `canvas` are passed between functions to update the plot efficiently.


def create_simulation_window(root):
    """
    Create the main window layout and widgets for the epidemic simulation.
    """
    root.title("Epidemic Simulation")

    # --- Parameter Input Fields ---
    frame_params = tk.LabelFrame(root, text="Simulation Parameters", padx=10, pady=10)
    frame_params.grid(row=0, column=0, padx=10, pady=10)

    beta_entry = create_label_and_entry(frame_params, "BETA:", 0)
    gamma_entry = create_label_and_entry(frame_params, "GAMMA:", 1)
    days_entry = create_label_and_entry(frame_params, "Days:", 2)
    mu_entry = create_label_and_entry(frame_params, "Death rate:", 3)
    vac_rate_entry = create_label_and_entry(frame_params, "Vaccination rate:", 4)
    s_0_entry = create_label_and_entry(frame_params, "Initial Susceptible:", 5)
    i_0_entry = create_label_and_entry(frame_params, "Initial Infected:", 6)
    r_0_entry = create_label_and_entry(frame_params, "Initial Recovered:", 7)
    # --- Model Selection ---
    tk.Label(frame_params, text="Model:").grid(row=8, column=0, sticky="w")
    model_selection = ttk.Combobox(frame_params, values=["SIR", "SIRD", "SIRDV"])
    model_selection.grid(row=9, column=1)
    model_selection.current(0)  # Default to the first model

    # --- Run Simulation Button ---
    tk.Button(frame_params, text="Run Simulation", command=lambda: run_simulation(
        beta_entry, gamma_entry, days_entry, mu_entry, vac_rate_entry, s_0_entry, i_0_entry, r_0_entry, model_selection,
        ax, canvas
    )).grid(row=10, column=0, columnspan=2, pady=10)



    # --- Plot Area ---
    frame_plot = tk.LabelFrame(root, text="Simulation Results", padx=10, pady=10)
    frame_plot.grid(row=0, column=1, padx=10, pady=10)

    fig, ax, canvas = create_interactive_plot_area(frame_plot)

    return ax, canvas

# Comment2:  This utility function simplifies the creation of labels and corresponding input fields. It takes a frame, label text, and row number
# as inputs, then positions the label and entry widget neatly in the layout using a grid.
def create_label_and_entry(frame, label_text, row):
    """
    Create a label and an entry widget in the specified frame.
    """
    tk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w")
    entry = tk.Entry(frame)
    entry.grid(row=row, column=1)
    return entry

# Comment 3:  Responsible for setting up the Matplotlib plot area for displaying simulation results. It initializes the figure and axes, embeds
# the plot into the Tkinter interface using `FigureCanvasTkAgg`, and adds the navigation toolbar for zooming, panning, and resetting the figure

def create_interactive_plot_area(parent_frame):
    """
    Create the Matplotlib plot area to display simulation results.
    Add interactivity to hover over data points.
    """
    # Create the Matplotlib figure and axes
    fig, ax = plt.subplots()

    # Embed the Matplotlib figure into the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.get_tk_widget().pack()

    # Add Navigation Toolbar for interactivity (pan, zoom, etc.)
    toolbar = NavigationToolbar2Tk(canvas, parent_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

    return fig, ax, canvas

# Comment4: This function retrieves user inputs from the entry fields, executes the respective epidemiological models (`SIR`, `SIRD`, or `SIRDV`) based
# on the user-selected option, and plots the results. It also adds hover interactivity to the plots using the `mplcursors` library, enabling users
# to view precise `(x, y)` coordinate values when hovering over data points.
def run_simulation(beta_entry, gamma_entry, days_entry, mu_entry, vac_rate_entry,s_0_entry, i_0_entry, r_0_entry, model_selection, ax, canvas):
    """
    Execute the epidemic simulation based on user input and plot the results.
    """
    # --- Retrieve user inputs ---
    beta = float(beta_entry.get() or 0.2)
    gamma = float(gamma_entry.get() or 0.1)
    days = int(days_entry.get() or 100)
    death_rate = float(mu_entry.get() or 0.01)
    vaccination_rate = float(vac_rate_entry.get() or 0.01)
    s_0 = int(s_0_entry.get() or 997)
    i_0 = int(i_0_entry.get() or 3)
    r_0 = int(r_0_entry.get() or 0)
    model = model_selection.get()

    # --- Run the selected epidemic model ---
    t = np.linspace(0, days, days)
    ax.clear()
    lines = []  # Store the lines for hover interaction
    if model == "SIR":
        S, I, R = sir_model(beta, gamma, days,s_0, r_0, i_0)
        lines.append(ax.plot(t, S, label="Susceptible")[0])
        lines.append(ax.plot(t, I, label="Infected")[0])
        lines.append(ax.plot(t, R, label="Recovered")[0])
    elif model == "SIRD":
        S, I, R, D = sird_model(beta, gamma, death_rate, days,s_0, r_0, i_0)
        lines.append(ax.plot(t, S, label="Susceptible")[0])
        lines.append(ax.plot(t, I, label="Infected")[0])
        lines.append(ax.plot(t, R, label="Recovered")[0])
        lines.append(ax.plot(t, D, label="Dead")[0])
    elif model == "SIRDV":
        S, I, R, D, V = sirdv_model(beta, gamma, death_rate, vaccination_rate, days,s_0, i_0, r_0)
        lines.append(ax.plot(t, S, label="Susceptible")[0])
        lines.append(ax.plot(t, I, label="Infected")[0])
        lines.append(ax.plot(t, R, label="Recovered")[0])
        lines.append(ax.plot(t, D, label="Dead")[0])
        lines.append(ax.plot(t, V, label="Vaccinated")[0])

    # --- Add hover interactivity ---
    mplcursors.cursor(lines, hover=True)

    # --- Update Plot ---
    ax.set_title(f"Simulation Results ({model} Model)")
    ax.set_xlabel("Days")
    ax.set_ylabel("Population")
    ax.legend()
    canvas.draw()

# Comment 5:1. These functions simulate the mathematical models for the epidemic (SIR, SIRD, and SIRDV). Each function computes population changes over
# a specified duration, returning arrays for categories like Susceptible, Infected, Recovered, Dead, and Vaccinated as applicable for the respective model.
#The followingg changes were made from the initial :
# - Initial values for `S`, `I`, `R`, `D`, and `V` are explicitly set in each function.
#- The total population is calculated dynamically based on these initial values.
#- The equations for `S`, `I`, `R`, `D`, and `V` are adjusted using these values to ensure accurate simulations.

def sir_model(beta, gamma, days, s_0, r_0, i_0):
    """
    Simple SIR model simulation with specified initial values.
    """
    S, I, R = [s_0], [i_0], [r_0]  # Initial values: S = 997, I = 3, R = 0
    total_population = S[-1] + I[-1] + R[-1]  # Total population
    for _ in range(days - 1):
        s = S[-1] - beta * S[-1] * I[-1] / total_population
        i = I[-1] + beta * S[-1] * I[-1] / total_population - gamma * I[-1]
        r = R[-1] + gamma * I[-1]
        S.append(s)
        I.append(i)
        R.append(r)
    return S, I, R

def sird_model(beta, gamma, mu, days, s_0, r_0, i_0):
    """
    SIRD model simulation with specified initial values.
    """
    S, I, R, D = [s_0], [i_0], [r_0], [0]  # Initial values: S = 997, I = 3, R = 0, D = 0
    total_population = S[-1] + I[-1] + R[-1] + D[-1]
    for _ in range(days - 1):
        s = S[-1] - beta * S[-1] * I[-1] / total_population
        i = I[-1] + beta * S[-1] * I[-1] / total_population - gamma * I[-1] - mu * I[-1]
        r = R[-1] + gamma * I[-1]
        d = D[-1] + mu * I[-1]
        S.append(s)
        I.append(i)
        R.append(r)
        D.append(d)
    return S, I, R, D



def sirdv_model(beta, gamma, mu, vac_rate, days,s_0,i_0, r_0 ):
    """
    SIRDV model simulation with specified initial values.
    """
    S, I, R, D, V = [s_0], [i_0], [r_0], [0], [0]  # Initial values: S = 997, I = 3, R = 0, D = 0, V = 0
    total_population = S[-1] + I[-1] + R[-1] + D[-1] + V[-1]
    for _ in range(days - 1):
        s = S[-1] - beta * S[-1] * I[-1] / total_population - vac_rate * S[-1]
        i = I[-1] + beta * S[-1] * I[-1] / total_population - gamma * I[-1] - mu * I[-1]
        r = R[-1] + gamma * I[-1]
        d = D[-1] + mu * I[-1]
        v = V[-1] + vac_rate * S[-1]
        S.append(s)
        I.append(i)
        R.append(r)
        D.append(d)
        V.append(v)
    return S, I, R, D, V


# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    ax, canvas = create_simulation_window(root)
    root.mainloop()

    import os

    # Initialize Git repository
    os.system("git init")

    # Create .gitignore for excluding Python-related files
    with open(".gitignore", "w") as gitignore:
        gitignore.write(
            "# Byte-compiled / optimized / DLL files\n"
            "__pycache__/\n"
            "*.py[cod]\n"
            "*$py.class\n"
            "\n"
            "# C extensions\n"
            "*.so\n"
            "\n"
            "# Distribution / packaging\n"
            "build/\n"
            "dist/\n"
            "*.egg-info/\n"
            "\n"
            "# MacOS files\n"
            ".DS_Store\n"
            "\n"
            "# Jupyter Notebook checkpoints\n"
            ".ipynb_checkpoints/\n"
        )

    # Add README.md
    with open("README.md", "w") as readme:
        readme.write(
            "# Epidemic Simulation\n"
            "This project simulates epidemic progression using SIR, SIRD, and SIRDV models. \n"
            "Developed with Python and Matplotlib; Tkinter used for user interface.\n"
        )

    # Make initial commit
    os.system("git add .")
    os.system("git commit -m 'Initial commit with project setup, README.md, and .gitignore'")




