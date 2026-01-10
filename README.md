# K-Drama Data Analysis & Insights 🇰🇷📊

An exploratory data analysis (EDA) project using Python to uncover trends within the highest-rated Korean Dramas. This project focuses on cleaning messy categorical data and visualizing genre popularity to understand what themes dominate the "Top 250" list.

## 📁 Project Overview
This project takes a raw dataset of the top 250 K-Dramas and transforms it into actionable insights. The main challenge involved handling "nested" strings where multiple genres were stored in a single cell, requiring data "explosion" techniques to ensure accurate statistical counting.

### Key Tasks Accomplished:
* **Virtual Environment Setup:** Isolated project dependencies using `venv`.
* **Data Cleaning:** Stripped whitespace and handled inconsistent string formatting in the Genre , Cast and Directors columns.
* **Data Transformation:** Utilized the Pandas `.explode()` method to flatten multi-genre dramas into individual rows as well as to flatten the dramas with multiple cast members and directors.
* **Visualization:** Generated a bar chart using Matplotlib to visualize the Top 10 genres by frequency. Generated a pie chart using Matplotlib to visualize the Top 5 popular networks based on distribution of the 250 dramas.
* **Recommendation System** Filtered and displayed top 3 items based on user input of genre and rating. Also filtered and displayed top 3 items based on user input of cast and director.

## 📊 The Dataset
The data used in this project is sourced from **MyDramaList**, specifically focusing on the "Top 250" ranked Korean Dramas as voted by the user community.

* **Origin:** MyDramaList (Community-driven database)
* **Size:** 250 Rows (Top 250 Dramas)
* **Key Features:** Title, Rating, Year of Release, Original Network, Genre, Episode Count, and Cast.



## 🛠️ Setup & Usage

1. **Clone the repository:**
   bash
   git clone https://github.com/Prartana982/kdrama-analysis.git

2.**Run the python script: **
   bash
   python3 main.py

