import pandas as pd
import matplotlib.pyplot as plt

def generate_performance_chart(csv_path="results/eval_report_v1.csv"):
    # 1. Load the data using Pandas
    df = pd.read_csv(csv_path)
    
    # 2. Calculate the mean (percentage of True values) for our metrics
    metrics = ['is_schema_ok', 'is_category_ok', 'is_length_ok']
    passing_rates = [df[metric].mean() * 100 for metric in metrics]
    
    # 3. Create the bar chart layout
    plt.figure(figsize=(8, 5))
    colors = ['#4CAF50', '#2196F3', '#FF9800'] # Green, Blue, Orange
    
    bars = plt.bar(metrics, passing_rates, color=colors, edgecolor='black')
    
    # 4. Stylize the chart
    plt.title("Gemini Prompt Performance Metrics (%)", fontsize=14, fontweight='bold')
    plt.ylabel("Passing Rate (%)", fontsize=12)
    plt.ylim(0, 110) # Give room at the top for labels
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 5. Add exact value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 2, f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    # 6. Save the chart as an image file
    output_image = "results/performance_chart.png"
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"📊 Chart successfully generated and saved to {output_image}")

if __name__ == "__main__":
    generate_performance_chart()