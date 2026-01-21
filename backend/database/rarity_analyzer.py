import pandas as pd
import os

def analyze_miscrit_rarities():
    """
    Analyzes the distribution of Miscrit rarities in the database.
    Returns detailed statistics about Common, Rare, Epic, Exotic, and Legendary Miscrits.
    """
    
    # Path to the miscrit database
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    miscrit_path = os.path.join(data_dir, "miscrit_database.csv")
    
    if not os.path.exists(miscrit_path):
        print(f"Error: Database file not found at {miscrit_path}")
        return
    
    # Read the database
    df = pd.read_csv(miscrit_path)
    
    print("=" * 60)
    print("           MISCRIT RARITY DISTRIBUTION ANALYSIS")
    print("=" * 60)
    
    total_miscrits = len(df)
    print(f"Total Miscrits in Database: {total_miscrits}")
    print("-" * 60)
    
    # Count rarities
    rarity_counts = df['Rarity'].value_counts()
    
    # Define the order we want (from most common to rarest)
    rarity_order = ['Common', 'Rare', 'Epic', 'Exotic', 'Legendary']
    
    print("RARITY BREAKDOWN:")
    print("-" * 60)
    
    total_check = 0
    for rarity in rarity_order:
        if rarity in rarity_counts:
            count = rarity_counts[rarity]
            percentage = (count / total_miscrits) * 100
            total_check += count
            
            # Create visual bar
            bar_length = int(percentage / 2)  # Scale down for display
            bar = "█" * bar_length
            
            print(f"{rarity:10} | {count:3d} | {percentage:5.1f}% | {bar}")
        else:
            print(f"{rarity:10} |   0 |  0.0% | ")
    
    print("-" * 60)
    print(f"{'TOTAL':10} | {total_check:3d} | 100.0% |")
    
    # Additional statistics
    print("\n" + "=" * 60)
    print("           ADDITIONAL STATISTICS")
    print("=" * 60)
    
    # Most common rarity
    most_common = rarity_counts.idxmax()
    most_common_count = rarity_counts.max()
    
    # Least common rarity
    least_common = rarity_counts.idxmin()
    least_common_count = rarity_counts.min()
    
    print(f"Most Common Rarity: {most_common} ({most_common_count} Miscrits)")
    print(f"Least Common Rarity: {least_common} ({least_common_count} Miscrits)")
    
    # Rare+ percentage (everything above Common)
    rare_plus = total_miscrits - rarity_counts.get('Common', 0)
    rare_plus_percent = (rare_plus / total_miscrits) * 100
    print(f"Rare+ Miscrits: {rare_plus} ({rare_plus_percent:.1f}%)")
    
    # Epic+ percentage (Epic, Exotic, Legendary)
    epic_plus = (rarity_counts.get('Epic', 0) + 
                 rarity_counts.get('Exotic', 0) + 
                 rarity_counts.get('Legendary', 0))
    epic_plus_percent = (epic_plus / total_miscrits) * 100
    print(f"Epic+ Miscrits: {epic_plus} ({epic_plus_percent:.1f}%)")
    
    return rarity_counts

def get_rarity_examples(n=3):
    """
    Shows example Miscrits for each rarity category.
    """
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    miscrit_path = os.path.join(data_dir, "miscrit_database.csv")
    
    df = pd.read_csv(miscrit_path)
    
    print("\n" + "=" * 60)
    print("           EXAMPLE MISCRITS BY RARITY")
    print("=" * 60)
    
    rarity_order = ['Common', 'Rare', 'Epic', 'Exotic', 'Legendary']
    
    for rarity in rarity_order:
        miscrits_of_rarity = df[df['Rarity'] == rarity]
        if len(miscrits_of_rarity) > 0:
            print(f"\n{rarity.upper()} Examples:")
            examples = miscrits_of_rarity.sample(min(n, len(miscrits_of_rarity)))
            for _, miscrit in examples.iterrows():
                print(f"  • {miscrit['Name']} (ID: {miscrit['Miscrit_ID']})")

if __name__ == "__main__":
    # Run the analysis
    rarity_stats = analyze_miscrit_rarities()
    get_rarity_examples()
    
    print("\n" + "=" * 60)
    print("Analysis complete!")