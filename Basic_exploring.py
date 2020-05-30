from Data_intro import apps, user, apps_user
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def get_app_by_letter(letter):
	try:
		# if the user entered lower case instead of upper case letter
		if letter.islower():
			letter = letter.upper()
		# if the user entered more than one letter
		if len(letter) != 1:
			return 'enter one letter only'
		DF_by_letter = apps.loc[apps['App'].str.startswith(letter, na = False)].reset_index(drop = True)
		return DF_by_letter
	except:
		return 'there is a problem with the input. '


# The number of categories in apps table.
categories_count = apps['Category'].drop_duplicates().count()

# The heaviest app in apps table.
max_m = int(apps[apps['Size'].str.lower().str.endswith('m')]['Size'].str.replace('M', '').max())
max_k = (int(apps[apps['Size'].str.lower().str.endswith('k')]['Size'].str.replace('k', '').max()) / 1024)

# Global var.
max_size = None
heaviest_app = None

if max_m > max_k:
	max_size = max_m
	str_size = str(max_m) + 'M'
	heaviest_app = list(apps[apps['Size'] == str_size]['App'].drop_duplicates())
	max_size = str_size
else:
	max_size = max_k
	str_size = str(int(max_k * 1024)) + 'k'
	heaviest_app = list(apps[apps['Size'] == str_size]['App'].drop_duplicates())
	max_size = str_size

# App with  the most installations.
most_install_app = list(apps[apps['Installs'] == apps['Installs'].max()]['App'].drop_duplicates())

# The most updated app.
recent_date = apps['Last Updated'].dt.date.max()
update_app = list(apps[recent_date == apps['Last Updated'].dt.date]['App'])

# The most popular app genre - according to average Installs, Rating, Genres.
group_genres = apps.groupby(['Genres']).mean().reset_index()

pop_genre_rating = group_genres[group_genres['Rating'] == group_genres['Rating'].max()]['Genres'].tolist()
pop_genre_installs = group_genres[group_genres['Installs'] == group_genres['Installs'].max()]['Genres'].tolist()
pop_genre_reviews = group_genres[group_genres['Reviews'] == group_genres['Reviews'].max()]['Genres'].tolist()

# Number of apps for each genre.
genres_apps = apps.groupby(['Genres'])['App'].count().sort_values(ascending = False)

# List of free apps names.
free_list = apps[apps['Type'] == 'Free']['App'].drop_duplicates().tolist()
free_count = len(free_list)

# Most popular app type - analytic proof.
typeAVG_group = apps.groupby(['Type']).mean().reset_index()
typeAVG_group[['Reviews', 'Installs']] = typeAVG_group[['Reviews', 'Installs']].astype(int)

max_popRating = typeAVG_group[typeAVG_group['Rating'] == typeAVG_group['Rating'].max()][['Type', 'Rating']]
max_popRating.reset_index(drop= True, inplace = True)
pop_rating_type, rating = max_popRating['Type'][0], max_popRating['Rating'][0]

max_popReviews = typeAVG_group[typeAVG_group['Reviews'] == typeAVG_group['Reviews'].max()][['Type', 'Reviews']]
max_popReviews.reset_index(drop= True, inplace = True)
pop_reviews_type, avg_reviews = max_popReviews['Type'][0], max_popReviews['Reviews'][0]

max_popInstalls = typeAVG_group[typeAVG_group['Installs'] == typeAVG_group['Installs'].max()][['Type', 'Installs']]
max_popInstalls.reset_index(drop= True, inplace = True)
pop_installs_type, avg_installs = max_popInstalls['Type'][0], max_popInstalls['Installs'][0]

if __name__ == '__main__':

	# print Basic Exploring insights.
	print('Basic Exploring')
	print('''
The total count of apps categories: {} \n
The heaviest app (size by mb) is: \n {},
 and its size is: {} \n
The app that has most installations is: \n {} \n
The most updated app is: {}
	and the most recent update is: {}. \n
The most popular app genre, by average rating is: {} \n
The most popular app genre, by average installs is: {} \n
The most popular app genre, by average reviews is: {} \n
The count of apps per genre:
{} \n
The count of free apps: {} \n
List of all the free apps:
	{} \n
The most popular app type according to rating: {}, and its average rating is: {}. \n
The most popular app type according to reviews: {}, and the average amount of reviews are: {}. \n
The most popular app type according to installs: {}, and the average amount of installs are: {}. \n
	
	'''.format(categories_count, heaviest_app, max_size, most_install_app, update_app, recent_date, pop_genre_rating,
	           pop_genre_installs, pop_genre_reviews, genres_apps, free_count, free_list, pop_rating_type, rating,
	           pop_reviews_type,
	           avg_reviews, pop_installs_type, avg_installs))



