from Advanced_analysis import rating_measures

normal_cols = ['Mean', 'Median', 'Mode']

default_epsilon = 0.5
def get_normal_dist(df, epsilon = default_epsilon):

	normal_indexes_list = []
	for index, raw in df[normal_cols].iterrows():
		max_val = raw.max()
		min_val = raw.min()

		if (max_val - min_val) <= epsilon:
			normal_indexes_list.append(index)

	normal_indexes_list = df[df.index.isin(normal_indexes_list)]

	return normal_indexes_list

def check_for_norm(df, category_name):
	normal_categories = (get_normal_dist(df)['Category']).tolist()
	if category_name in normal_categories:
		return True
	else:
		return False


# The most stable app category

most_stableCate = rating_measures[rating_measures['STD'] == rating_measures['STD'].min()]
least_stableCate = rating_measures[rating_measures['STD'] == rating_measures['STD'].max()]

# Category normal distributor

norm_dist_list = (get_normal_dist(rating_measures)['Category']).tolist()
non_norm_list = rating_measures[~rating_measures['Category'].isin(norm_dist_list)]['Category'].tolist()

if __name__ == '__main__':

	print('''
	The most stable App Category is the Category that has the lowest STD.
	An App Category that's distributes normally its median is equals to its mean and mode (range of difference = 0.5)
	
	The most stable App Category is: {}
	The most stable App Category is distributing normally with: Mean = {}, Median = {}, Mode = {}, STD = {}.
	
	The least stable App Category is: {}
	The least stable App Category is distributing normally with: Mean = {}, Median = {}, Mode = {}, STD = {}.
	
	A list of all the Apps that distribute normally:
	{}
	
	A list of all the Apps that doesnt distribute normally:
	{}
	
	
		'''.format(most_stableCate['Category'].item(), most_stableCate['Mean'].item(), most_stableCate['Median'].item(),
	    most_stableCate['Mode'].item(), most_stableCate['STD'].item(), least_stableCate['Category'].item(),
	    least_stableCate['Mean'].item(), least_stableCate['Median'].item(), least_stableCate['Mode'].item(),
	    least_stableCate['STD'].item(), norm_dist_list, non_norm_list))
