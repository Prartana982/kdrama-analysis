import pandas as pd
import re
from rich.console import Console
from rich.panel import Panel

console = Console()
df = pd.read_csv('kdrama.csv')

def get_duration_minutes(duration_str):
    """Converts '1 hr. 10 min.' or '45 min.' into total integer minutes."""
    if pd.isna(duration_str): return 0
    hrs = re.search(r'(\d+)\s*hr', duration_str)
    mins = re.search(r'(\d+)\s*min', duration_str)
    return (int(hrs.group(1)) * 60 if hrs else 0) + (int(mins.group(1)) if mins else 0)

def binge_planner():
    drama_name = console.input("[bold cyan]Which drama do you want to binge? [/]").strip()
    
    # Find the drama (case-insensitive search)
    match = df[df['Name'].str.contains(drama_name, case=False, na=False)]
    
    if not match.empty:
        drama = match.iloc[0] # Take the first match
        episodes = int(drama['Number of Episodes'])
        ep_duration = get_duration_minutes(drama['Duration'])
        
        # Calculations
        total_mins = ep_duration * episodes
        total_hours = total_mins / 60
        
        console.print(f"\n[bold yellow]Total time for '{drama['Name']}':[/] {total_hours:.1f} hours")
        
        # User input for pace
        eps_per_day = int(console.input("[bold green]How many episodes can you watch per day? [/]"))
        
        days_to_finish = episodes / eps_per_day
        
        # Result Panel
        result_text = (
            f"📺 [bold]{drama['Name']}[/]\n"
            f"📅 It will take you [bold cyan]{days_to_finish:.1f} days[/] to finish.\n"
            f"⏰ You will spend [bold magenta]{(eps_per_day * ep_duration)/60:.1f} hours[/] watching every day."
        )
        console.print(Panel(result_text, title="Binge Plan", border_style="green"))
    else:
        console.print("[red]Drama not found. Try checking the spelling![/]")

binge_planner()