import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

def month(row):
    '''
    Args: 
        row: pandas dataframe
    Out:
        None
    Description:
        Gives month from starting epoch in new dataframe column
    '''
    if row['DATAYEAR'] == 2016:
        return row['MONTH']
    elif row['DATAYEAR'] == 2017:
        return (12+row['MONTH'])
    elif row['DATAYEAR'] == 2018:
        return (24+row['MONTH'])
    elif row['DATAYEAR'] == 2019:
        return (36+row['MONTH'])

def histplot_raw(df,ax,colname='TOTALREVENUE'):
    ax.hist(df[colname],bins=20,edgecolor='black',color='#002f4a')
    ax.set_xlabel('Revenue',fontsize=20, fontweight='bold',color='#002f4a')
    ax.set_ylabel('Count of Datapoints',fontsize=20, fontweight='bold',color='#002f4a')
    ax.set_title('Distribution of Revenues (No Transformation)',fontsize=26, fontweight='bold',color='#002f4a')
    [t.set_color('#002f4a') for t in ax.xaxis.get_ticklines()]
    [t.set_color('#002f4a') for t in ax.xaxis.get_ticklabels()]
    [t.set_color('#002f4a') for t in ax.yaxis.get_ticklines()]
    [t.set_color('#002f4a') for t in ax.yaxis.get_ticklabels()]
    ax.set_facecolor('#d9c4b1')
    ax.patch.set_alpha(0.5)
    
def histplot_transform(df,ax,colname='TOTALREVENUE'):
    ax.hist(np.log(df[colname]),bins=20,edgecolor='black',color='#002f4a')
    ax.set_xlabel('Revenue',fontsize=20, fontweight='bold',color='#002f4a')
    ax.set_ylabel('Count of Datapoints',fontsize=20, fontweight='bold',color='#002f4a')
    ax.set_title('Distribution of Revenues (With Transformation)',fontsize=26, fontweight='bold',color='#002f4a')
    [t.set_color('#002f4a') for t in ax.xaxis.get_ticklines()]
    [t.set_color('#002f4a') for t in ax.xaxis.get_ticklabels()]
    [t.set_color('#002f4a') for t in ax.yaxis.get_ticklines()]
    [t.set_color('#002f4a') for t in ax.yaxis.get_ticklabels()]
    ax.set_facecolor('#d9c4b1')
    ax.patch.set_alpha(0.5)

    
def plot_gen_type(df,ax,labels,colnames=['MW_COAL','MW_GEOTHERMAL', 'MW_HYDROELECTRIC',
                                  'MW_NATURAL_GAS', 'MW_NUCLEAR','MW_OIL', 'MW_OTHER',
                                  'MW_SOLAR', 'MW_WIND']):
    for idx, col in enumerate(colnames):
        ax.plot(df['MONTH_YEAR'],df[col],label=labels[idx],linewidth=2)
    ax.legend(prop={'size': 20})
    ax.set_xlabel('Months',fontsize=20, fontweight='bold',color='#002f4a')
    ax.set_ylabel('Average MW Generated',fontsize=20, fontweight='bold',color='#002f4a')
    [t.set_color('#002f4a') for t in ax.xaxis.get_ticklines()]
    [t.set_color('#002f4a') for t in ax.xaxis.get_ticklabels()]
    [t.set_color('#002f4a') for t in ax.yaxis.get_ticklines()]
    [t.set_color('#002f4a') for t in ax.yaxis.get_ticklabels()]
    ax.set_facecolor('#d9c4b1')
    ax.patch.set_alpha(0.5)



if __name__ == '__main__':

    plt.style.use('ggplot')

    sixty = pd.read_csv('../data/860m_clean.csv')
    sixtyone = pd.read_csv('../data/861m_clean.csv')
    combined = pd.read_csv('../data/combined.csv')

    combined['MONTH_YEAR'] = combined.apply (lambda row: month(row),axis=1)

    avg_gen = combined.groupby(['MONTH_YEAR']).agg({'MW_COAL':'sum','MW_GEOTHERMAL':'sum', 'MW_HYDROELECTRIC':'sum',
                                  'MW_NATURAL_GAS':'sum', 'MW_NUCLEAR':'sum','MW_OIL':'sum', 'MW_OTHER':'sum',
                                  'MW_SOLAR':'sum', 'MW_WIND':'sum'})
    avg_gen = avg_gen.reset_index()


    fig, ax = plt.subplots(figsize=(12,10))
    histplot_raw(combined,ax)
    plt.savefig('../images/raw_revenue.png',dpi=600,bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(12,10))
    histplot_transform(combined,ax)
    plt.savefig('../images/transformed_revenue.png',dpi=600,bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(12,10))
    histplot_raw(combined,ax,'NAMEPLATECAPACITY(MW)')
    ax.set_title('Distribution of Total MW Generated (No Transformation)',fontsize=26,color='#002f4a',fontweight='bold')
    ax.set_xlabel('Total MW Generated',fontsize=20,color='#002f4a',fontweight='bold')
    plt.savefig('../images/raw_mw.png',dpi=600,bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(12,10))
    histplot_transform(combined,ax,'NAMEPLATECAPACITY(MW)')
    ax.set_title('Distribution of Total MW Generated (With Transformation)',fontsize=26,color='#002f4a',fontweight='bold')
    ax.set_xlabel('Total MW Generated',fontsize=20,color='#002f4a',fontweight='bold')
    plt.savefig('../images/transformed_mw.png',dpi=600,bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(12,10))
    plot_gen_type(avg_gen,ax,['Coal','Natural Gas'],['MW_COAL','MW_NATURAL_GAS'])
    ax.set_title('Decrease in Coal Generation',fontsize=26,color='#002f4a',fontweight='bold')
    ax.set_xlim(left=5)

    plt.savefig('../images/gen_type_coal.png',dpi=600,bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(12,10))
    plot_gen_type(avg_gen,ax,['Wind','Solar','Nuclear'],['MW_WIND','MW_SOLAR','MW_NUCLEAR'])
    ax.set_title('Renewable Energy Trends',fontsize=26,color='#002f4a',fontweight='bold')
    plt.savefig('../images/gen_type_green.png',dpi=600,bbox_inches='tight')