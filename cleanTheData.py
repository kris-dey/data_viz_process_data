import pandas as pd
import numpy as np

df = pd.read_csv('SpotifyFeatures.csv')

genres = df.genre.unique()
FEATURE_COUNT = 7


class GenreData:
	def __init__(self, genre):
		self.genre = genre
		self.data = [0.0] * FEATURE_COUNT

gds = []
currGenre = df.iloc[0][0]
gd = GenreData(currGenre)
counter  = 0
for index, row in df.iterrows():
	popularity = float(df.iloc[index][1])
	if popularity > 40:
		continue
	print(index)
	if currGenre != row['genre']:
		if counter != 0:
			for i in range(len(gd.data)):
				gd.data[i] = gd.data[i]/counter
			gds.append(gd)

		gd = GenreData(row['genre'])
		currGenre = row['genre']
		counter = 0

	for i in range(FEATURE_COUNT):
		gd.data[i] += float(df.iloc[index][2+i])

	counter += 1

if counter != 0:
	for i in range(len(gd.data)):
		gd.data[i] = gd.data[i]/counter
	gds.append(gd)


features = [
        'Acousticness', 
        'Danceability', 
        'Energy',
        'Instrumentalness', 
        'Liveness', 
        'Speechiness', 
        'Valence'
]
cols = ['Features', 'Genre', 'Score']

rows = []
for gd in gds:
	for i in range(len(features)):
		row = [features[i], gd.genre, gd.data[i]]
		rows.append(row)

df = pd.DataFrame(data=np.array(rows), columns=cols)
df.to_csv('unpopular_song_data.csv')


