import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string

def plot_optimized_boxplots(data_path, output_image_path):
    # Load the dataset
    data = pd.read_csv(data_path)
    
    # List of variables to plot, excluding 'No' and 'Type'
    plot_vars = data.columns[2:]
    
    # Calculate number of rows (each row will have three plots)
    n_vars = len(plot_vars)
    n_rows = (n_vars + 2) // 3  # ensure there's an extra row if number of variables mod 3 isn't 0
    
    # Generate column labels like Excel columns
    def generate_column_labels(n):
        labels = []
        letters = string.ascii_lowercase
        for i in range(n):
            label = ""
            base, rem = divmod(i, 26)
            if base > 0:
                label += letters[base - 1]
            label += letters[rem]
            labels.append(label)
        return labels

    column_labels = generate_column_labels(n_vars)

    # Initialize a figure with subplots arranged in 3 columns
    fig, axs = plt.subplots(n_rows, 3, figsize=(12, n_rows * 1.2), sharex=False)
    axs = axs.ravel()  # flatten the 2D array of axes into 1D for easier iteration
    
    # Loop through variables to create a boxplot for each
    for i, var in enumerate(plot_vars):
        # LaTeX for subscript if 'N' is present in the variable name
        
        if var in plot_vars[-4:]:
            var_display = var.replace('$_N$', '$_\\mathrm{N}$')
        else:
            var_display = var
        
        sns.boxplot(x=var, y='Type', data=data, orient='h', ax=axs[i], palette={'S': 'skyblue', 'A': 'lightgreen'})
        var_title = f"({column_labels[i]}) {var_display}"
        axs[i].set_title(var_title, loc='left', fontdict={'fontsize': 10, 'fontweight': 'bold', 'fontname': 'Times New Roman'})
        axs[i].set_xlabel('')
        axs[i].set_ylabel('')
        axs[i].set_yticklabels(['物源', '风沙'], fontdict={'fontsize': 10, 'fontname': 'SimSun'})
        for label in axs[i].get_xticklabels():
            label.set_fontname('Times New Roman')
            label.set_fontsize(10)
    
    # If the number of variables doesn't fill all subplots, remove the extras
    for j in range(i+1, len(axs)):
        fig.delaxes(axs[j])
    
    # Adjust layout and add a legend
    plt.tight_layout()
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, ['物源', '风沙'], loc='upper right', fontsize=8)
    
    # Save the plot to the specified output path
    plt.savefig(output_image_path, dpi=600)
    plt.close()

# Execute the updated function and save the image to a new path
plot_optimized_boxplots('Data1_Zonal.csv', 'Zonal.png')
plot_optimized_boxplots('Data2_Sedimental.csv', 'Sedimental.png')