import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


def check_missing_values(df):
	if not df.isnull().values.any():
		# print('there are no missing values')
		return True
	else:
		# print('ERROR - there are missing values')
		print(df.isnull().sum())

apps_table = pd.read_csv('apps.csv')
apps_table = apps_table[['App', 'Category', 'Rating', 'Size', 'Type', 'Price', 'Genres']]
user_table = pd.read_csv('user_reviews.csv')
user_table = user_table[['App', 'Sentiment', 'Sentiment_Polarity', 'Sentiment_Subjectivity']]

# Organizing the data
apps_table['Price'] = apps_table['Price'].str.replace('$', '', ).astype(float)
apps_table['Size'] = apps_table['Size'].replace({'K': '*1e3', 'M': '*1e6', 'Varies with device': -99999, 'k': '*1e3'},
                                  regex=True).map(pd.eval).astype(int)

apps_user_table = pd.merge(apps_table, user_table, on = 'App')

# Copy relevant columns to local variables and split it between 'data' and 'labels'.
X = apps_user_table[['App', 'Category', 'Rating', 'Size', 'Type', 'Price', 'Genres', 'Sentiment_Polarity',
					 'Sentiment_Subjectivity']].copy().reset_index(drop = True)
Y = pd.DataFrame(apps_user_table['Sentiment'].copy().reset_index(drop = True), columns = ['Sentiment'])

# X table preparation

# Completing missing numeric values
imp = SimpleImputer(missing_values = np.nan, strategy = 'mean')
X[['Rating', 'Price', 'Size', 'Sentiment_Polarity', 'Sentiment_Subjectivity']] = imp.fit_transform(
		X[['Rating', 'Price', 'Size', 'Sentiment_Polarity', 'Sentiment_Subjectivity']])

check_missing_values(X)

# Converting categorical values to indicators.
x_category = X.select_dtypes(include = ['object']).copy()

# Transforming categorical values to indicators.
x_category_dummies = pd.get_dummies(x_category)

# Drooping the col's that had been transformed
X = X.drop(columns = ['App', 'Category', 'Type', 'Genres'])

# New X table after completing missing values + transformed categorical values
X = x_category_dummies.merge(X, left_index = True, right_index = True)

# Deleting temp tables
del (x_category, x_category_dummies)

# Y table preparation
# Completing missing values

imp = SimpleImputer(missing_values = np.nan, strategy = 'most_frequent')
y_com_values = pd.DataFrame(imp.fit_transform(Y), columns = ['Sentiment'])

if check_missing_values(y_com_values):
	Y = y_com_values
	del y_com_values

# Converting categorical values to indicators.
Y = pd.get_dummies(Y)
Y.columns = ['Negative', 'Neutral', 'Positive']

