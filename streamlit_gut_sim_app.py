# streamlit_gut_sim_app.py
# Streamlit version of the Gut-Immune Digital Twin Simulation

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
bacteria_species = ["Bacteroides", "Firmicutes", "Actinobacteria", "Proteobacteria", "Lactobacillus", "Clostridium", "Faecalibacterium"]
immune_cells = ["Treg", "Th17", "Macrophage", "Dendritic", "Cytokine_IL6", "Cytokine_TNF"]
time_steps = 100

# Initial values
def generate_initial_states():
    initial_bacteria = {sp: np.random.randint(50, 200) for sp in bacteria_species}
    initial_immune = {cell: np.random.randint(5, 30) for cell in immune_cells}
    return initial_bacteria, initial_immune

# Simulation logic
def run_simulation(apply_antibiotics, apply_probiotics, apply_diet):
    initial_bacteria, initial_immune = generate_initial_states()
    bacteria = initial_bacteria.copy()
    immune = initial_immune.copy()
    pop_history = {sp: [] for sp in bacteria_species}
    flare_index = []

    for t in range(time_steps):
        if apply_antibiotics and t == 20:
            for sp in bacteria:
                bacteria[sp] = int(bacteria[sp] * 0.5)
        if apply_probiotics and t == 50:
            bacteria["Lactobacillus"] += 50
            bacteria["Faecalibacterium"] += 30
        if apply_diet and t == 70:
            immune["Treg"] += 10
            immune["Cytokine_TNF"] = max(0, immune["Cytokine_TNF"] - 5)
            immune["Cytokine_IL6"] = max(0, immune["Cytokine_IL6"] - 5)

        for sp in bacteria:
            change = np.random.randint(-10, 10)
            bacteria[sp] = max(0, bacteria[sp] + change)
            pop_history[sp].append(bacteria[sp])

        dysbiosis_score = (
            bacteria["Proteobacteria"] * 0.01 -
            bacteria["Faecalibacterium"] * 0.005 +
            np.random.uniform(-0.5, 0.5)
        )

        for cell in immune:
            base_trigger = sum(bacteria.values()) / 1000
            fluctuation = np.random.randint(-2, 3)
            immune[cell] = max(0, immune[cell] + int(base_trigger + fluctuation + dysbiosis_score))

        flare = (immune["Cytokine_IL6"] + immune["Cytokine_TNF"]) / max(1, immune["Treg"])
        flare_index.append(flare)

    return pop_history, flare_index

# Plotting function
def plot_results(pop_history, flare_index):
    fig, axs = plt.subplots(2, 1, figsize=(12, 8))

    for sp in bacteria_species:
        axs[0].plot(pop_history[sp], label=sp)
    axs[0].set_title("Bacterial Populations Over Time")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(flare_index, color='red', label="Flare Index")
    axs[1].axhline(5, color='black', linestyle='--', label='Risk Threshold')
    axs[1].set_title("Autoimmune Flare Index Over Time")
    axs[1].legend()
    axs[1].grid(True)

    st.pyplot(fig)

# Streamlit UI
st.title("🧠 Gut-Immune Digital Twin Simulation")
st.markdown("Simulate how your gut microbiome and immune system respond to interventions.")

apply_antibiotics = st.checkbox("Apply Antibiotics", value=True)
apply_probiotics = st.checkbox("Apply Probiotics", value=True)
apply_diet = st.checkbox("Apply Anti-inflammatory Diet", value=True)

if st.button("Run Simulation"):
    pop_history, flare_index = run_simulation(apply_antibiotics, apply_probiotics, apply_diet)
    plot_results(pop_history, flare_index)
    st.success("Simulation complete!")
