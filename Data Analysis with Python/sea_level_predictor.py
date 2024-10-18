import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], color='blue', label='Original Data')

    # Create first line of best fit
    plot_best_fit_line(df, 'Year', 'CSIRO Adjusted Sea Level', range(1880, 2051), 'red', 'Prediction: All Data (1880-2050)')

    # Create second line of best fit
    df_recent_years = df[df['Year'] >= 2000]
    plot_best_fit_line(df_recent_years, 'Year', 'CSIRO Adjusted Sea Level', range(2000, 2051), 'green', 'Prediction: Recent Data (2000-2050)')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()


def plot_best_fit_line(df, x_col, y_col, x_range, color, label):
    # Plots a line of best fit based on the provided dataframe.

    slope, intercept, _, _, _ = linregress(df[x_col], df[y_col])
    x_values = pd.Series(x_range)
    y_values = intercept + slope * x_values
    plt.plot(x_values, y_values, color=color, label=label)