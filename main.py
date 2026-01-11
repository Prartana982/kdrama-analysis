import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Import functions from your other files (treating them as modules)
from binge_calculator import binge_planner
from cast_director_search import search_top_3
from recommender import smart_recommender # Ensure this function name exists in your recommender.py

console = Console()

def main():
    # Load the data once here to pass it to modules if needed
    try:
        df = pd.read_csv('kdrama.csv')
    except FileNotFoundError:
        console.print("[bold red]Error: 'kdrama.csv' not found![/]")
        return

    while True:
        console.clear()
        console.print(Panel.fit("🍿 K-DRAMA MULTI-TOOL 🍿", style="bold white on blue"))
        console.print("1. [bold]Smart Recommender[/] (Genre + Rating)")
        console.print("2. [bold]Cast/Director Search[/]")
        console.print("3. [bold]Binge Time Planner[/]")
        console.print("4. [bold red]Exit[/]")
        
        choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            # Call function from recommender.py
            smart_recommender(df) 
        elif choice == "2":
            # Call function from cast_director_search.py
            sub_choice = Prompt.ask("Search by", choices=["Cast", "Director"])
            search_top_3(sub_choice) 
        elif choice == "3":
            # Call function from binge_calculator.py
            binge_planner() 
        elif choice == "4":
            console.print("[bold yellow]Goodbye! Happy watching! 👋[/]")
            break
        
        input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()