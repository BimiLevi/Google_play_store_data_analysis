from Files_functions import read_csv_pandas
import pandas as pd

def get_basic_details(df):
	raw_num = df.shape[0]
	col_num = df.shape[1]
	col_list_names = list(df.columns)
	duplicated_raws = df.duplicated(df.columns.tolist()).sum()
	col_types = df.dtypes
	return raw_num, col_num, col_list_names, duplicated_raws, col_types


def print_basic_details(df, file_name, report = False, open_html = False):
	from pandas_profiling import ProfileReport
	raw_num, col_num, col_list_names, duplicated_raws, col_types = get_basic_details(df)
	print('''
The number of raws in {0} DF are: {1}
The number of columns in {0} DF are: {2}
The names of columns in {0} DF are: \n {3}
The count of duplicated raws in {0} DF is: {4}
Columns types in {0} DF are: \n {5}
						'''.format(file_name, raw_num, col_num, col_list_names, duplicated_raws, col_types)
	      )

	if report:
		profile = ProfileReport(df, title = 'Pandas Profiling Report - {} Data Frame'.format(file_name),
		                        html = {'style': {'full_width': True}})
		profile.to_file(output_file = "{}.html".format(file_name))
		if open_html:
			import webbrowser
			webbrowser.open('{}.html'.format(file_name))


# loading the data to pandas DF.
apps = read_csv_pandas('apps.csv')
user = read_csv_pandas('user_reviews.csv')

# changing the type of Installs col from object to int.
apps["Installs"] = apps["Installs"].str.replace("+", "")
apps["Installs"] = apps["Installs"].str.replace(",", "").astype('int64')

apps['Last Updated'] = pd.to_datetime(apps['Last Updated'], errors='coerce')

apps_user = apps.merge(user, on = 'App')
apps_user.to_csv('apps and user joined.csv')

if __name__ == '__main__':

	# print Data Intro insights.
	print('Data Intro')


	print_basic_details(apps, 'Apps')
	print_basic_details(user, 'User Reviews')
	print_basic_details(apps_user, 'Apps and Users')


