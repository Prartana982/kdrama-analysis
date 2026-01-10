import pandas as pd
import matplotlib.pyplot as plt
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# --- 1. DATA PREPARATION ---
def load_data():
    return pd.read_csv('kdrama.csv')

def get_duration_minutes(duration_str):
    if pd.isna(duration_str): return 0
    hrs = re.search(r'(\d+)\s*hr', duration_str)
    mins = re.search(r'(\d+)\s*min', duration_str)
    return (int(hrs.group(1)) * 60 if hrs else 0) + (int(mins.group(1)) if mins else 0)

# --- 2. CORE FEATURES ---

def show_top_10(df):
    top_10 = df.sort_values(by='Rating', ascending=False).head(10)
    table = Table(title="🏆 Top 10 K-Dramas", header_style="bold magenta")
    table.add_column("Rank", justify="center")
    table.add_column("Name", style="cyan")
    table.add_column("Rating", style="green")
    for i, (_, row) in enumerate(top_10.iterrows(), 1):
        table.add_row(str(i), row['Name'], str(row['Rating']))
    console.print(table)

def cast_director_search(df):
    """Searches for a person in the Cast or Director columns."""
    mode = Prompt.ask("Search in", choices=["Cast", "Director"])
    name = console.input(f"[bold cyan]Enter {mode} Name (e.g., Lee Je Hoon): [/]").strip()
    
    results = df[df[mode].str.contains(name, case=False, na=False)]
    
    if not results.empty:
        table = Table(title=f"Top 3 Projects for '{name}'", border_style="bright_blue")
        table.add_column("Drama Name", style="yellow")
        table.add_column("Rating", style="bold green")
        table.add_column("Year", style="dim")
        
        top_hits = results.sort_values(by='Rating', ascending=False).head(3)
        for _, row in top_hits.iterrows():
            table.add_row(row['Name'], str(row['Rating']), str(row['Year of release']))
        console.print(table)
    else:
        console.print(f"[red]No results found for '{name}' in {mode}.[/]")

def smart_recommender(df):
    genre_input = console.input("[bold cyan]Enter Genre (e.g. Thriller, Romance): [/]").strip()
    min_rating = float(Prompt.ask("Minimum Rating", default="8.5"))
    
    results = df[
        (df['Genre'].str.contains(genre_input, case=False, na=False)) & 
        (df['Rating'] >= min_rating)
    ]
    
    if not results.empty:
        table = Table(title=f"Top {genre_input} Recommendations")
        table.add_column("Name", style="yellow")
        table.add_column("Rating", style="green")
        for _, row in results.sort_values(by='Rating', ascending=False).head(5).iterrows():
            table.add_row(row['Name'], str(row['Rating']))
        console.print(table)
    else:
        console.print("[red]No matches found.[/]")

def binge_planner(df):
    name = console.input("[bold cyan]Enter Drama Name: [/]").strip()
    match = df[df['Name'].str.contains(name, case=False, na=False)]
    
    if not match.empty:
        drama = match.iloc[0]
        mins = get_duration_minutes(drama['Duration'])
        eps = int(drama['Number of Episodes'])
        pace = int(Prompt.ask("How many episodes per day?", default="1"))
        days = eps / pace
        total_hrs = (mins * eps) / 60
        console.print(Panel(f"🎬 [bold]{drama['Name']}[/]\n⏳ Total Time: {total_hrs:.1f} hours\n📅 Finish in: [bold green]{days:.1f} days[/]"))
    else:
        console.print("[red]Drama not found.[/]")

def network_analysis(df):
    console.print("[yellow]Saving 'network_analysis.png'...[/]")
    net_series = df['Original Network'].str.split(',').explode().str.strip()
    net_counts = net_series.value_counts().head(7)
    plt.figure(figsize=(6,6))
    net_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title('Network Market Share')
    plt.savefig('network_analysis.png')
    plt.close()
    console.print("[bold green]✅ Success![/]")

# --- 3. MASTER MENU ---

def main():
    df = load_data()
    while True:
        console.print("\n" + "─"*45)
        console.print(Panel.fit("🍿 K-DRAMA ULTIMATE TOOLBOX 🍿", style="bold white on blue"))
        console.print("1. [bold]Top 10 Rankings[/]")
        console.print("2. [bold]Cast/Director Search[/]")
        console.print("3. [bold]Genre + Rating Recommender[/]")
        console.print("4. [bold]Binge Time Planner[/]")
        console.print("5. [bold]Network Market Analysis[/] (Graph)")
        console.print("6. [bold red]Exit[/]")
        
        choice = Prompt.ask("\nSelect Option", choices=["1", "2", "3", "4", "5", "6"])
        
        if choice == "1": show_top_10(df)
        elif choice == "2": cast_director_search(df)
        elif choice == "3": smart_recommender(df)
        elif choice == "4": binge_planner(df)
        elif choice == "5": network_analysis(df)
        elif choice == "6": 
            console.print("[bold yellow]Goodbye! 👋[/]")
            break
        
        input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()