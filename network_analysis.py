import pandas as pd
import matplotlib.pyplot as plt

df= pd.read_csv('kdrama.csv')

df['Original Network'] = df['Original Network'].str.split(',').apply(lambda x: [i.strip() for i in x] if isinstance(x,list) else x)
exploded_df= df.explode('Original Network')
network_counts= exploded_df['Original Network'].value_counts()
network_counts.head(5).plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Distribution of top 250 dramas by network')
plt.ylabel('')
plt.tight_layout()
plt.savefig('network_distribution.png')
print(network_counts.head(10))


