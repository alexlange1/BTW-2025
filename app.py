import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Data
institute_2021 = {
    'allensbach': {'CDU': 25, 'SPD': 26, 'AfD': 10, 'Grüne': 16, 'FDP': 10.5, 'Linke': 5},
    'dimap': {'CDU': 22, 'SPD': 26, 'AfD': 11, 'Grüne': 15, 'FDP': 11, 'Linke': 6},
    'fg wahlen': {'CDU': 23, 'SPD': 25, 'AfD': 10, 'Grüne': 16.5, 'FDP': 11, 'Linke': 6},
    'wk': {'CDU': 22.5, 'SPD': 25.5, 'AfD': 11, 'Grüne': 14, 'FDP': 12, 'Linke': 7},
    'insa': {'CDU': 22, 'SPD': 25, 'AfD': 11, 'Grüne': 15, 'FDP': 12, 'Linke': 6.5},
    'gms': {'CDU': 23, 'SPD': 25, 'AfD': 11, 'Grüne': 16, 'FDP': 13, 'Linke': 6},
    'forsa': {'CDU': 22, 'SPD': 25, 'AfD': 10, 'Grüne': 17, 'FDP': 12, 'Linke': 6},
    'ipsos': {'CDU': 22, 'SPD': 26, 'AfD': 11, 'Grüne': 16, 'FDP': 12, 'Linke': 7},
    'yougov': {'CDU': 21, 'SPD': 25, 'AfD': 12, 'Grüne': 14, 'FDP': 11, 'Linke': 7},
    'emnid': {'CDU': 21, 'SPD': 25, 'AfD': 11, 'Grüne': 16, 'FDP': 11, 'Linke': 7}
}

institute_2025 = {
    'allensbach': {'CDU': 32, 'SPD': 15, 'AfD': 20, 'Grüne': 13, 'FDP': 5, 'Linke': 6},
    'dimap': {'CDU': 32, 'SPD': 14, 'AfD': 21, 'Grüne': 14, 'FDP': 4, 'Linke': 6},
    'fg wahlen': {'CDU': 30, 'SPD': 16, 'AfD': 20, 'Grüne': 14, 'FDP': 4, 'Linke': 7},
    'wk': {'CDU': 32, 'SPD': 12.5, 'AfD': 20, 'Grüne': 12.5, 'FDP': 4, 'Linke': 6},
    'insa': {'CDU': 30, 'SPD': 15, 'AfD': 21, 'Grüne': 13, 'FDP': 4, 'Linke': 6},
    'gms': {'CDU': 30, 'SPD': 15, 'AfD': 21, 'Grüne': 14, 'FDP': 4, 'Linke': 6},
    'forsa': {'CDU': 30, 'SPD': 16, 'AfD': 20, 'Grüne': 13, 'FDP': 5, 'Linke': 7},
    'ipsos': {'CDU': 29, 'SPD': 16, 'AfD': 21, 'Grüne': 13, 'FDP': 4, 'Linke': 4},
    'yougov': {'CDU': 27, 'SPD': 17, 'AfD': 20, 'Grüne': 12, 'FDP': 4, 'Linke': 9},
    'emnid': {'CDU': 30, 'SPD': 15, 'AfD': 20, 'Grüne': 14, 'FDP': 4, 'Linke': 4}
}

ergebnis = {'CDU': 24.2, 'SPD': 25.7, 'AfD': 10.4, 'Grüne': 14.7, 'FDP': 11.4, 'Linke': 4.9}

# Party colors
party_colors = {
    'CDU': 'black',
    'SPD': 'red',
    'Grüne': 'green',
    'FDP': 'yellow',
    'AfD': 'lightblue',
    'Linke': 'purple'
}

# Streamlit App
st.set_page_config(page_title="2025 Election Predictions", layout="wide")
st.title("📊 2025 Election Predictions Analysis")
st.write("This app adjusts the 2025 election predictions based on the 2021 results and displays the average predictions with error bars.")

# Sidebar for user interaction
st.sidebar.header("Settings")
selected_institutes = st.sidebar.multiselect(
    "Select Institutes to Include",
    options=list(institute_2021.keys()),
    default=list(institute_2021.keys())
)
alpha = st.sidebar.slider("Bias Scaling Factor (α)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
st.sidebar.write("Adjusted 2025 prediction = 2025 prediction - α * (2021 prediction - Actual 2021)")

# Initialize dictionaries to store sums and counts
party_sums = {party: 0 for party in ergebnis}
party_counts = {party: 0 for party in ergebnis}

bias_data = {party: [] for party in ergebnis}
adjusted_predictions_data = {party: [] for party in ergebnis}
adjusted_2025 = {}

# Process each institute's predictions
for inst, pred_2021 in institute_2021.items():
    if inst in selected_institutes and inst in institute_2025:
        adjusted_2025[inst] = {}
        for party, p2021 in pred_2021.items():
            if party in ergebnis and party in institute_2025[inst]:
                bias = p2021 - ergebnis[party]
                bias_data[party].append(bias)

                adjusted_pred = institute_2025[inst][party] - alpha * bias
                adjusted_pred = round(adjusted_pred, 1)
                adjusted_2025[inst][party] = adjusted_pred

                adjusted_predictions_data[party].append(adjusted_pred)
                party_sums[party] += adjusted_pred
                party_counts[party] += 1

# Compute average for each party
average_predictions = {party: round(party_sums[party] / party_counts[party], 1) for party in ergebnis}

# Display average predictions
st.subheader("📈 Average Adjusted 2025 Predictions")
st.write(average_predictions)

# Prepare data for visualization
party_labels = list(ergebnis.keys())
means = []
std_devs = []

# Calculate mean and standard deviation for error bars
for party in party_labels:
    values = adjusted_predictions_data[party]
    means.append(np.mean(values))
    std_devs.append(np.std(values))

# Create figure and bar plot
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(party_labels, means, yerr=std_devs, capsize=5, edgecolor='black', alpha=0.75)

# Color-code bars
for bar, party in zip(bars, party_labels):
    bar.set_color(party_colors[party])

# Labels and title
ax.set_xlabel("Political Party")
ax.set_ylabel("Adjusted 2025 Prediction (%)")
ax.set_title("Adjusted 2025 Election Predictions with Error Bars", fontsize=16, fontweight='bold')
ax.set_ylim(0, max(means) + max(std_devs) + 2)  # Ensure enough space for error bars
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Display the plot in Streamlit
st.pyplot(fig)

# Add a footer
st.markdown("---")
st.markdown("**Note:** This analysis is based on hypothetical adjustments to 2025 predictions using 2021 election results.")