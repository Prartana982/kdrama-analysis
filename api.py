from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re

app = FastAPI()

# IMPORTANT: This allows your React app (on a different port) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv('kdrama.csv')

# Utility function from your previous work
def get_duration_minutes(duration_str):
    if pd.isna(duration_str): return 0
    hrs = re.search(r'(\d+)\s*hr', duration_str)
    mins = re.search(r'(\d+)\s*min', duration_str)
    return (int(hrs.group(1)) * 60 if hrs else 0) + (int(mins.group(1)) if mins else 0)

@app.get("/dramas/search")
def search_dramas(query: str, type: str = "Cast"):
    """API Endpoint for Cast/Director search"""
    results = df[df[type].str.contains(query, case=False, na=False)]
    return results.sort_values(by='Rating', ascending=False).head(10).to_dict(orient="records")

@app.get("/dramas/top10")
def get_top_10():
    """API Endpoint for Top 10 list"""
    return df.sort_values(by='Rating', ascending=False).head(10).to_dict(orient="records")

@app.get("/dramas/binge")
def calculate_binge(name: str, episodes_per_day: int = 1):
    """API Endpoint for Binge Planning"""
    match = df[df['Name'].str.contains(name, case=False, na=False)]
    if not match.empty:
        drama = match.iloc[0]
        mins = get_duration_minutes(drama['Duration'])
        total_hrs = (mins * int(drama['Number of Episodes'])) / 60
        days = int(drama['Number of Episodes']) / episodes_per_day
        return {"name": drama['Name'], "total_hours": round(total_hrs, 2), "days": round(days, 2)}
    return {"error": "Not found"}

@app.get("/dramas/recommend")
def recommend_dramas(genre: str, min_rating: float = 8.0):
    # Filter by rating first for speed
    mask = (df['Rating'] >= min_rating) & (df['Genre'].str.contains(genre, case=False, na=False))
    results = df[mask].sort_values(by='Rating', ascending=False).head(10)
    return results.to_dict(orient="records")