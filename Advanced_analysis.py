from Data_intro import apps, user, apps_user
import pandas as pd
import numpy as np



pd.set_option('display.float_format', lambda x: '%.3f' % x)
def get_average_polarity(app_name):
    if not check_in_dataset(app_name, table = 'user'):
        raise NameError('The app name that has entered is not inside the data set.')
    app_mean = round(user[user['App'] == app_name]['Sentiment_Polarity'].mean(), 3)
    return app_mean

def check_in_dataset(app_name, table = False):
    if not table:
        return 'You need to choose a table to check'
    if table == 'apps':
        apps_appList = apps['App'].drop_duplicates().tolist()
        if app_name in apps_appList:
            return True
        else:
            print('The apps name you entered is not inside the {} dataset'.format(table))
            return False
    elif table == 'user':
        user_appList = user['App'].drop_duplicates().tolist()
        if app_name in user_appList:
            return True
        else:
            print('The apps name you entered is not inside the {} dataset'.format(table))
            return False
    elif table == 'apps_user':
        apps_user_appList = apps_user['App'].drop_duplicates().tolist()
        if app_name in apps_user_appList:
            return True

def get_sentiment(app_name):
    if check_in_dataset(app_name, table = 'user'):
        avg_polarity = get_average_polarity(app_name)
        if avg_polarity == np.nan:
                return 'The sentiment is not calculable, contains Null values'
        sentiment = map_sentiment(avg_polarity)
        return sentiment

def map_sentiment(raw):
    try:
        if float(raw) < 0:
            val = 'Negative'
        elif float(raw) == 0:
            val = 'Neutral'
        elif str(raw) == 'nan':
            val = np.nan
        else:
            val = 'Positive'
        return val
    except:
        print('An error has occurred')

# The amount of apps that are classified sentiments.

grouped_app = user.groupby(['App'])['Sentiment_Polarity'].mean().reset_index()
grouped_app.rename(columns = {"Sentiment_Polarity": "Sentiment_Polarity_Avg"}, inplace = True)
grouped_app['Sentiment'] = grouped_app['Sentiment_Polarity_Avg'].apply(map_sentiment)

apps_sentiment_count = grouped_app['Sentiment'].value_counts(dropna = False)
app_positive, app_neutral, app_negative = apps_sentiment_count[0], apps_sentiment_count[3], apps_sentiment_count[2]
app_nan = apps_sentiment_count[1]


# The sentiment of the app with the highest rating.
avgRating_group = apps_user.groupby('App')['Rating'].mean().sort_values(ascending= False).reset_index()
avgRating_group.rename(columns = {"Rating": "Avg_Rating"}, inplace = True)

highest_ratingApp = pd.DataFrame(avgRating_group[avgRating_group['Avg_Rating'] == avgRating_group['Avg_Rating'].max()])
highest_ratingApp['Sentiment'] = highest_ratingApp['Avg_Rating'].apply(map_sentiment)

appList_maxAvgRating = highest_ratingApp['App'].tolist()
max_avgRating = round(highest_ratingApp['Avg_Rating'].max(), 3)
sentiment_avgRating = highest_ratingApp['Sentiment'].drop_duplicates()[0]


# Average polarity of free apps.
perc = [.20, .40, .60, .80]
free_polarity_stats = apps_user[apps_user['Type'] == 'Free']['Sentiment_Polarity'].describe(percentiles = perc)

free_polarity_mean = round(free_polarity_stats['mean'], 3)

# Count of sentiments -  for visualization.
sentiments_count = user['Sentiment'].value_counts()

# Avg rating grouped by genres  -  for visualization.
ratingGroup_avg = apps.groupby('Genres')['Rating'].mean().dropna().sort_values().reset_index()
ratingGroup_avg.rename(columns = {"Rating": "Avg_Rating"}, inplace = True)
ratingGroup_avg.round({'Avg_Rating': 3})

median = ratingGroup_avg['Avg_Rating'].median()
median_index = ratingGroup_avg.loc[ratingGroup_avg['Avg_Rating'] >= median].iloc[[0]].index[0]


# Sentiment polarity mean by by type -  for visualization.
sentPol_rating = apps_user.groupby('Type')['Sentiment_Polarity'].mean()
sentPol_difference = sentPol_rating[1] - sentPol_rating[0]

# Rating measures for multiple subplots by category  -  for visualization.
rating_measures = apps.drop_duplicates().groupby('Category')['Rating'].describe()[['mean', 'std', '50%']].reset_index()
rating_measures.rename(columns = {'50%': 'Median', 'mean': 'Mean', 'std': 'STD'}, inplace = True)

rating_mode = apps.drop_duplicates().groupby('Category')['Rating'].apply(lambda x: x.mode()[0]).reset_index()
rating_mode.rename(columns = {'Rating': 'Mode'}, inplace = True)

rating_measures = rating_measures.join(rating_mode.set_index('Category'), on = 'Category')


# sentiment pol avg ratio -  for visualization.
app_sentiPol = apps_user.groupby(['App'])['Sentiment_Polarity'].mean().dropna().reset_index()
app_sentiPol.rename(columns = {"Sentiment_Polarity": "Sentiment_Polarity_Avg"}, inplace = True)
app_sentiPol['Sentiment'] = app_sentiPol['Sentiment_Polarity_Avg'].apply(map_sentiment)
sentiPol_ratio = (app_sentiPol['Sentiment'].value_counts() / app_sentiPol['Sentiment'].count())

if __name__ == '__main__':

    # print Advanced Analysis insights.
    print('Advanced Analysis')
    print('''
The amount of apps that are classified as Positive sentiment is: {}.\n
The amount of apps that are classified as Neutral sentiment is: {}.\n
The amount of apps that are classified as Negative sentiment is: {}.\n
The sentiment of the app with the highest average rating is: {}, and the rating is: {}.\n
The apps that has the highest average rating are: 
{}.\n
The average sentiment polarity of free apps is: {}.\n
Sentiment values count: 
{}.\n
Sentiment average polarity by app type: 
{} \n
and the difference is: {}.\n 
Average rating measures: 
{}.\n
Sentiment polarity average ratio is: 
{}.\n 
    '''.format(app_positive, app_neutral, app_negative, sentiment_avgRating, max_avgRating, appList_maxAvgRating,
               free_polarity_mean, sentiments_count, sentPol_rating, sentPol_difference, rating_measures, sentiPol_ratio))

