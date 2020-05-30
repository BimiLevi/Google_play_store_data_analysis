from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from Knn_preprocess import X, Y
from Files_functions import save_json, load_json

#  Splitting  groups to train and test
y = Y
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, shuffle = True)

def find_best_k(k_start, k_end, X_train, y_train, X_test, y_test):
	try:
		if k_start <= 0:
			raise ValueError('The first K must be grater then zero.')

		else:
			all_kAcc = {}

			for K in range(k_start, k_end + 1):
				print('Starts search with K = {}'.format(K))

				# Scaling the X variable data.
				sc_X = StandardScaler()
				X_train = sc_X.fit_transform(X_train)
				X_test = sc_X.transform(X_test)

				# Building and training the model with training data.
				clf = KNeighborsClassifier(n_neighbors = K)
				clf.fit(X_train, y_train)

				# Evaluating model's predication against test dataset.
				y_pred = clf.predict(X_test)

				temp_accScore = accuracy_score(y_test, y_pred)
				all_kAcc[K] = temp_accScore

				print('End search with K = {}'.format(K))

			save_json('All k and acc', all_kAcc)
			return bestK_acc
	except:
		return 'Error'

# Plotting Knn result's.
all_kAcc = pd.DataFrame.from_dict(load_json('All k and acc'), orient='index', columns = ['Accuracy'])

def plot_knn_bar(knn_df):
	from Visualization import bar_colors, get_minMax
	plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False})
	plt.style.use('classic')
	plt.rcParams['font.sans-serif'] = 'SimSun'

	fig = plt.figure()
	colors = bar_colors(all_kAcc, 'Accuracy')
	x = list(knn_df.index.values)
	y = knn_df['Accuracy'].tolist()
	plt.bar(x=x, height = y, color=colors, figure = fig)

	min_max = get_minMax(knn_df, 'Accuracy')
	for index, value in min_max.items():
		value = round(value, 2)
		plt.text(float(index) - 1.5, value + 0.015, str(value), va = 'center', fontsize = 10, fontweight = 'bold',
		         figure = fig)

	plt.tick_params(right = False, top = False, pad = 20)
	plt.title('Knn Accuracy Score',  figure = fig)
	plt.xlabel('K-nearest neighbors',  figure = fig)
	plt.ylabel('Accuracy score',  figure = fig)
	fig.tight_layout()
	fig.savefig('Knn accuracy score - bar plot.jpeg', dpi=300, quality =100, progressive = True)

	return fig


temp = plot_knn_bar(all_kAcc)
plt.show()