import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Initialize Rich Console
console = Console()

# ... [Your existing data loading and processing code] ...
df = pd.read_csv('kdrama.csv')
df_clean = df.copy()
df_clean['Genre'] = df_clean['Genre'].str.split(',').apply(lambda x: [i.strip() for i in x] if isinstance(x,list) else x)
exploded_df = df_clean.explode('Genre')

# Themed Input Prompts
user_input = console.input("[bold cyan]Enter a genre (e.g., Romance, Thriller): [/bold cyan]").strip()
try:
    min_rating_str = console.input("[bold cyan]Enter minimum rating (e.g., 8.5): [/bold cyan]")
    min_rating = float(min_rating_str)
except ValueError:
    rprint("[yellow]Invalid rating. Considering default rating 0.0[/yellow]")
    min_rating = 0.0

# Filtering
results = exploded_df[(exploded_df['Genre'].str.contains(user_input, case=False, na=False)) & (exploded_df['Rating'] >= min_rating)]

if results.empty:
    rprint(f"[bold red]No dramas found for '{user_input}' with rating >= {min_rating}.[/bold red]")
else:
    # Drop duplicates if a show belongs to multiple sub-genres that match the search
    results = results.drop_duplicates(subset="Name")
    top3 = results.sort_values(by="Rating", ascending=False).head(3)

    # Create a Rich Table
    table = Table(title=f"Top Rated {user_input} Dramas", title_style="bold magenta", header_style="bold white on blue")

    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Rating", justify="center", style="green")
    table.add_column("Year", justify="center", style="yellow")
    table.add_column("Director", style="magenta")

    # Add rows to the table
    for _, row in top3.iterrows():
        table.add_row(
            str(row['Name']), 
            str(row['Rating']), 
            str(row['Year of release']), 
            str(row['Director'])
        )

    console.print(table)