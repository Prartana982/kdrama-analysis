import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('kdrama.csv')

df['Genre'] = df['Genre'].str.split(',').apply(lambda x: [i.strip() for i in x] if isinstance(x, list) else x)

exploded_df = df.explode('Genre')

genre_counts = exploded_df['Genre'].value_counts()

genre_counts.head(10).plot(kind='bar', color='red', edgecolor='black')

plt.title('Top 10 Most Popular K-Drama Genres')
plt.xlabel('Genre')
plt.ylabel('Number of Dramas')
plt.xticks(rotation=45) 
plt.tight_layout()      

plt.savefig('genre_popularity.png')

print("Top 10 Most Popular Genres by Number of Dramas:")
print(genre_counts.head(10))
