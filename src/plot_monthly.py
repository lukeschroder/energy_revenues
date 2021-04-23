import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

def month(row):
    if row['DATAYEAR'] == 2016:
        return row['MONTH']
    elif row['DATAYEAR'] == 2017:
        return (12+row['MONTH'])
    elif row['DATAYEAR'] == 2018:
        return (24+row['MONTH'])
    elif row['DATAYEAR'] == 2019:
        return (36+row['MONTH'])

def histplot_raw(df,ax,colname='TOTALREVENUE'):
    ax.hist(df[colname],bins=20,edgecolor='black')
    ax.set_xlabel('Revenue',fontsize=16)
    ax.set_ylabel('Count of Datapoints',fontsize=16)
    ax.set_title('Distribution of Revenues (No Transformation)',fontsize=22)
    
def histplot_transform(df,ax,colname='TOTALREVENUE'):
    ax.hist(np.log(df[colname]),bins=20,edgecolor='black')
    ax.set_xlabel('Revenue',fontsize=16)
    ax.set_ylabel('Count of Datapoints',fontsize=16)
    ax.set_title('Distribution of Revenues (With Transformation)',fontsize=22)
    
def plot_gen_type(df,ax,labels,colnames=['MW_COAL','MW_GEOTHERMAL', 'MW_HYDROELECTRIC',
                                  'MW_NATURAL_GAS', 'MW_NUCLEAR','MW_OIL', 'MW_OTHER',
                                  'MW_SOLAR', 'MW_WIND']):
    for idx, col in enumerate(colnames):
        ax.plot(df['MONTH_YEAR'],df[col],label=labels[idx])
    ax.legend()
    ax.set_xlabel('Months',fontsize=16)
    ax.set_ylabel('Average MW Generated',fontsize=16)

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
    ax.set_title('Distribution of Total MW Generated (No Transformation)',fontsize=22)
    ax.set_xlabel('Total MW Generated',fontsize=16)
    plt.savefig('../images/raw_mw.png',dpi=600,bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(12,10))
    histplot_transform(combined,ax,'NAMEPLATECAPACITY(MW)')
    ax.set_title('Distribution of Total MW Generated (With Transformation)',fontsize=22)
    ax.set_xlabel('Total MW Generated',fontsize=16)
    plt.savefig('../images/transformed_mw.png',dpi=600,bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(12,10))
    plot_gen_type(avg_gen,ax,['Coal','Natural Gas'],['MW_COAL','MW_NATURAL_GAS'])
    ax.set_title('Decrease in Coal Generation',fontsize=22)
    plt.savefig('../images/gen_type_coal.png',dpi=600,bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(12,10))
    plot_gen_type(avg_gen,ax,['Wind','Solar','Nuclear'],['MW_WIND','MW_SOLAR','MW_NUCLEAR'])
    ax.set_title('Renewable Energy Trends',fontsize=22)
    plt.savefig('../images/gen_type_green.png',dpi=600,bbox_inches='tight')