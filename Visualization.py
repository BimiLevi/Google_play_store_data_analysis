from Data_intro import apps, user, apps_user
from Advanced_analysis import map_sentiment
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.style.use('classic')
plt.rcParams['font.sans-serif'] = 'SimSun'
plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False})

color_palette = {'black': '#3D3D3D', 'blue': '#3F5E99', 'yellow': '#EBCA88', 'red': '#F04A6B', 'green': '#3AB08B'}

def bar_colors(df, col):
    colors = []
    min_val = df[col].min()
    max_val = df[col].max()
    for val in df[col]:
        if val == max_val:
            colors.append(color_palette['green'])
        elif val == min_val:
            colors.append(color_palette['red'])
        else:
            colors.append(color_palette['blue'])
    return colors

def get_minMax(df, col_name):
    min_val = df[df[col_name] == df[col_name].min()][col_name]
    max_val = df[df[col_name] == df[col_name].max()][col_name]
    min_max = pd.concat([min_val, max_val])
    return min_max

# Bar diagram that represents the count of sentiment.
def plot_sentimentBar_count():
    from Advanced_analysis import sentiments_count
    fig = plt.figure()

    color = [color_palette['green'], color_palette['red'], color_palette['blue']]
    sentiments_countPlot = sentiments_count.plot(kind= 'bar', rot= 0, color=color, edgecolor= 'black', figure=fig)

    for index, value in enumerate(sentiments_count.tolist()):
        sentiments_countPlot.text(index, value * 1.02, str(value), fontsize= 11, horizontalalignment= 'center')

    plt.tick_params(right = False, top = False, pad = 20)
    plt.title('The total amount of items according to sentiment', figure=fig)
    plt.xlabel('Sentiment', figure=fig)
    plt.ylabel('Sentiment Count', figure=fig)
    plt.savefig('The total count of items according to Sentiment.jpeg', dpi= 300, quality =100, progressive =True,
                bbox_inches='tight', figure=fig)
    return fig

# Avg rating grouped by genres  -  barh subplot

def genre_avgRating(df, col_name, axes, median_index):
    below_mid, above_mid = pd.DataFrame(df[0:median_index]), pd.DataFrame(df[median_index:]).reset_index(drop = True)

    count = 0
    for df in [below_mid, above_mid]:
        titels = ['Below Median', 'Above Median']
        yticks = np.arange(0, df.shape[0] + 1)
        xlim = (df[col_name].min() - 0.2, df[col_name].max() + 0.2)
        colors = bar_colors(df, col_name)
        df_labels = df['Genres'].tolist()

        df[col_name].plot.barh(subplots= True, ax= axes[count], width = 0.3, color= colors, edgecolor= 'black',
                               legend = False, xlim= xlim, yticks=yticks, title=[''])

        axes[count].set_ylabel(titels[count], labelpad= 20, fontsize = 15)
        axes[count].set_yticklabels(df_labels, fontsize=15, ha='left')


        max_title = len(max(df_labels, key = len))
        axes[count].tick_params(axis = 'y', pad= max_title * 7.5)
        axes[count].spines["left"].set_visible(False)
        axes[count].spines["bottom"].set_visible(False)
        axes[count].tick_params(right = False, top = False, left = False, bottom = False)


        min_max = get_minMax(df, col_name)
        for index, value in min_max.items():
            value = round(value, 2)
            axes[count].text(value + 0.01, index, str(value), va= 'center',  fontsize= 13, fontweight='bold')


        count += 1

def plot_avgRating_genre():
    from Advanced_analysis import ratingGroup_avg, median, median_index

    nrow = 1
    ncol = 2
    fig, axes = plt.subplots(nrow, ncol, figsize = (16, 13.5))

    genre_avgRating(ratingGroup_avg, 'Avg_Rating', axes, median_index)
    fig.suptitle('The average rating per genre', fontsize = 18)
    fig.tight_layout(rect = [0, 0.03, 1, 0.95])
    fig.savefig('The average rating per genre - barh.jpeg', dpi = 300, quality = 100, progressive = True,
                bbox_inches = 'tight')

    return fig

# polarity difference between free and paid apps
def plot_type_polar_difference():
    from Advanced_analysis import sentPol_rating
    fig = plt.figure()

    colors = [color_palette['red'], color_palette['green']]
    sentPol_rating.plot(kind= 'bar', rot= 0, color=colors, edgecolor= 'black', figure=fig)

    plt.tick_params(right = False, top = False, pad = 20)

    for index, value in enumerate(sentPol_rating.tolist()):
        plt.text(index, value * 1.02, str(round(value, 3)), fontsize= 11, horizontalalignment= 'center', figure=fig)

    plt.title('Average Polarity')
    plt.savefig('Average Polarity Type difference.jpeg', dpi= 300, quality =100, progressive =True,  bbox_inches='tight')
    return fig

# Rating measures two subplots.

def axes_set(axes_list):
    for ax in axes_list:
        ax.legend(bbox_to_anchor=(1.15, 1))
        ax.tick_params(right = False, top = False)

def plot_ratingMeasure_smallSub():
    from Advanced_analysis import rating_measures

    fig, (ax, ax2) = plt.subplots(2, 1, figsize = (13, 11), sharex = True)
    axes_list = [ax, ax2]
    colors = bar_colors(rating_measures, 'STD')

    rating_measures.plot.bar(x='Category', y='STD', ax= ax, color=colors, ec="black")

    min_max = get_minMax(rating_measures, 'STD')
    for index, value in min_max.items():
        value = round(value, 2)
        ax.text(index - 0.5, value + 0.02, str(value), va= 'center',  fontsize= 13, fontweight='bold')

    rating_measures.plot.bar(x='Category', y=['Mean', 'Median', 'Mode'], ax= ax2, rot=90, ec="black", fontsize=12)
    axes_set(axes_list)

    plt.xlabel('Category', fontsize=15)
    fig.suptitle('The measures of each category by its rating', y=1, fontsize=20)
    fig.savefig('measures second plot.jpeg', dpi= 300, quality =100, progressive =True,  bbox_inches='tight')
    return fig

# Rating measures multiple subplots.
def subplot_measures(df, nrow, ncol, col_list, axes, labels_col, xticks):
    count = 0
    for r in range(nrow):
        for c in range(ncol):
            colors = bar_colors(df, col_list[count])
            df[col_list[count]].plot(kind = 'bar', ax = axes[r, c], color = colors, xticks = xticks, width = 0.4,
                                     edgecolor= 'black', fontsize= 12, rot=90, subplots=True)

            axes[r, c].set_title(col_list[count], pad= 17)
            axes[r, c].set_xticklabels(df[labels_col], va= 'center_baseline', fontsize=12)
            axes[r, c].tick_params(right = False, top = False, pad = 20)


            min_max = get_minMax(df, col_list[count])
            for index, value in min_max.items():
                value = round(value, 1)
                axes[r, c].text(index, value * 1.02, str(value), fontsize= 11, ha= 'center', fontweight='bold')
            count += 1

def plot_ratingMeasures_bigSub():
    from Advanced_analysis import rating_measures

    nrow = 2
    ncol = 2
    fig, axes = plt.subplots(nrow, ncol, figsize = (14, 9.5), sharex = True)

    col_list = list(rating_measures.columns[1:])
    labels_col = 'Category'
    xticks = np.arange(rating_measures.shape[0])
    subplot_measures(rating_measures, nrow, ncol, col_list, axes, labels_col, xticks)
    fig.text(0.5, 0.025, 'Categories', ha= 'center', fontsize= 12)
    g_patch, r_patch = mpatches.Patch(color=color_palette['green'], label='Max value'), mpatches.Patch(
            color=color_palette['red'], label='Min value')

    fig.legend(handles=[g_patch, r_patch], loc='upper right', frameon=True, fontsize= 10)
    fig.suptitle('The measures of each category by its rating', fontsize = 20, y=1)
    fig.subplots_adjust(hspace = 0.4, wspace = 0.4, top = 0.8)
    fig.tight_layout()
    fig.savefig('measures multiple subplots.jpeg', dpi= 300, quality =100, progressive = True,  bbox_inches='tight')
    return fig

plt.rcParams['patch.edgecolor'] = 'black'

# The ratio between paid and free apps.
def plot_type_ratioPie():
    Type_ratio = (apps['Type'].value_counts() / apps['Type'].count()).round(3)

    legend_labels = list(Type_ratio.index)
    sizes = Type_ratio.tolist()
    colors = [color_palette['green'], color_palette['red']]
    fig, ax = plt.subplots()
    _, _, autotexts = ax.pie(sizes, colors=colors, autopct= '%1.2f%%',  startangle=90)
    ax.axis('equal')
    ax.legend(legend_labels, loc= "best", bbox_to_anchor=(0.95, 0.95), frameon = True, edgecolor= 'black', fontsize = 11)

    plt.setp(autotexts, size=13.5, weight="bold")
    plt.title('Ratio between the Types of apps', fontsize = 20, fontweight = 'bold')
    plt.tight_layout()
    plt.savefig('Ratio between the Types of apps.jpeg', dpi= 300, quality =100, progressive =True,  bbox_inches='tight')
    return fig


# The ratio between avg sentiment.
def plot_avgSentiment_pie():
    from Advanced_analysis import sentiPol_ratio

    legend_labels = list(sentiPol_ratio.index)
    sizes = sentiPol_ratio.tolist()
    colors = [color_palette['green'], color_palette['red'], color_palette['blue']]

    fig, ax = plt.subplots(figsize=(6, 6))

    _, _, autotexts = ax.pie(sizes, colors=colors, autopct= '%1.2f%%',  startangle=90, pctdistance= 1.07)
    ax.axis('equal')
    ax.legend(legend_labels, loc= "best", bbox_to_anchor=(0.95, 0.9), frameon = True, edgecolor= 'black', fontsize = 11)

    plt.setp(autotexts, size=13.5, weight="bold")
    plt.title('Ratio of sentiment', fontsize = 20, fontweight = 'bold')
    plt.tight_layout()
    plt.savefig('Ratio of sentiment.jpeg', dpi= 300, quality =100, progressive =True, bbox_inches='tight')
    return fig

def plot_knn_bar():
    from Files_functions import load_json
    all_kAcc = pd.DataFrame.from_dict(load_json('All k and acc'), orient = 'index', columns = ['Accuracy'])

    fig = plt.figure(figsize = (8.3, 6))
    colors = bar_colors(all_kAcc, 'Accuracy')
    x = list(all_kAcc.index.values)
    y = all_kAcc['Accuracy'].tolist()
    plt.bar(x=x, height = y, color=colors, figure = fig)

    min_max = get_minMax(all_kAcc, 'Accuracy')
    for index, value in min_max.items():
        value = round(value, 2)
        plt.text(float(index) - 1.3, value + 0.02, str(value * 100) + '%', va = 'center', fontsize = 10, fontweight =
        'bold',
                 figure = fig)

    plt.tick_params(right = False, top = False, left= False)
    plt.title('Knn Accuracy Score',  figure = fig)
    plt.xlabel('K-nearest neighbors',  figure = fig)
    plt.ylabel('Accuracy score',  figure = fig)
    fig.savefig('Knn accuracy score - bar plot.jpeg', dpi=300, quality =100, progressive = True)

    return fig

if __name__=="__main__":

    plot_sentimentBar_count()
    plot_avgRating_genre()
    plot_type_polar_difference()
    plot_ratingMeasures_bigSub()
    plot_type_ratioPie()
    plot_avgSentiment_pie()
    plot_knn_bar()

    plt.show()
