import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

# Initialize the Rich Console
console = Console()

# Load the dataset
df = pd.read_csv('kdrama.csv')

def search_top_3(column_name):
    """Filters data for an actor/director and displays a beautiful Rich table."""
    search_term = console.input(f"[bold cyan]Enter the name of the {column_name}:[/] ").strip()
    
    # Filter the dataset
    results = df[df[column_name].str.contains(search_term, case=False, na=False)]
    
    if not results.empty:
        top_3 = results.sort_values(by='Rating', ascending=False).head(3)
        
        # Create a Rich Table
        table = Table(title=f"Top 3 Dramas involving '{search_term}'", header_style="bold magenta", border_style="bright_blue")
        
        table.add_column("Name", style="yellow", no_wrap=False)
        table.add_column("Rating", justify="center", style="green")
        table.add_column("Director", style="italic")
        table.add_column("Cast", style="dim")

        # Add rows to the table
        for _, row in top_3.iterrows():
            table.add_row(
                str(row['Name']), 
                str(row['Rating']), 
                str(row['Director']), 
                str(row['Cast'])
            )

        console.print(table)
    else:
        console.print(Panel(f"[bold red]No dramas found for '{search_term}' in the {column_name} column.[/]"))

# --- Main Execution ---
console.print(Panel("[bold white]K-Drama Search Engine[/]", subtitle="Powered by Python & Rich"))

# Using Rich's Prompt ensures the user chooses the right options
choice = Prompt.ask("Search by 1.Cast/2.Director", choices=["1", "2"], default="1")
choice_map = {"1": "Cast", "2": "Director"}

search_top_3(choice_map[choice])