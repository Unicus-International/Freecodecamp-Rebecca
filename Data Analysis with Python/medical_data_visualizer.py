import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


## medical_data_visualizer

# Import the data from medical_examination.csv and assign it to the df variable
df = pd.read_csv('medical_examination.csv')

# Calculate BMI and add 'overweight' column
bmi = df['weight'] / (df['height'] / 100) ** 2
df['overweight'] = (bmi > 25).astype(int)

# Normalize 'cholesterol' and 'gluc'
df[['gluc','cholesterol']] = (df[['gluc','cholesterol']] > 1).astype(int)


# Draw the Categorical Plot in the draw_cat_plot function
def draw_cat_plot():
    
    # Select categorical features for visualization
    categorical_features = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    # Convert the data into long format
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=categorical_features)    

    # Create the catplot
    fig = sns.catplot(
        x="variable", 
        hue="value", 
        col="cardio", 
        data=df_cat, 
        kind="count", 
        height=6, 
        aspect=1
    ).fig

    # Customize the plot
    fig.axes[0].set_xlabel("variable")
    fig.axes[0].set_ylabel("total")
    fig.axes[0].set_title("Cardio: 0")
    fig.axes[1].set_title("Cardio: 1")

    # Save the figure
    fig.savefig('catplot.png')
    return fig


# Draw the Heat Map in the draw_heat_map function
def draw_heat_map():
    
    #Clean the data by filtering height and weight percentiles
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) & 
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figur
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Draw the heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,  # Display the correlation coefficients
        fmt='.1f',  # Format to 1 decimal place
        cmap='coolwarm',
        vmax=0.3,  # Set a max value for color range
        center=0,
        square=True,
        linewidths=0.5,  # Add lines between cells
        cbar_kws={"shrink": 0.5}  # Shrink the color bar
    )

    # Save the figure
    fig.savefig('heatmap.png')
    return fig
