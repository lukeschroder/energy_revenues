import pandas as pd
import numpy as np
from simpledbf import Dbf5
import math

def re_index_sixty(sixty):
    for item in sixty.items():
            headers = sixty[item[0]].iloc[0]
            sixty[item[0]] = pd.DataFrame(sixty[item[0]].values[1:], columns=headers)


def month_agg(sixty):
    default = sixty[1]
    for item in sixty.items():
        if item[0] > 1:
            default = default.append(item[1]).copy()
    return default

def add_month(sixty):
    for item in sixty.items():
        item[1]['Month'] = item[0]

def rename_cols(sixty):
    for item in sixty.items():
        item[1].columns = item[1].columns.str.upper()
        item[1].columns = item[1].columns.str.replace(' ', '')
        item[1].columns = item[1].columns.str.replace('-', '')
        item[1].columns = item[1].columns.str.replace('_', '')
        item[1].columns = item[1].columns.str.replace('\\n', '')
        item[1].columns = item[1].columns.str.replace('ENTITYID', 'UTILITYID')
        item[1].columns = item[1].columns.str.replace('ENTITYNAME', 'UTILITYNAME')
        
        
def drop_cols(sixty):
    for item in sixty.items():
        item[1].drop(columns=['TECHNOLOGY','PRIMEMOVERCODE', 'OPERATINGMONTH', 'OPERATINGYEAR',
                                           'PLANNEDRETIREMENTMONTH', 'PLANNEDRETIREMENTYEAR', 'STATUS',
                                           'PLANNEDDERATEYEAR', 'PLANNEDDERATEMONTH',
                                           'PLANNEDDERATEOFSUMMERCAPACITY(MW)', 'PLANNEDUPRATEYEAR',
                                            'PLANNEDUPRATEMONTH', 'PLANNEDUPRATEOFSUMMERCAPACITY(MW)', 'COUNTY','BALANCINGAUTHORITYCODE',
                                            'GOOGLEMAP','BINGMAP', 'UNITCODE','SECTOR','PLANTSTATE','GENERATORID'],errors='ignore').copy()

def clean_agg_sixtys(sixtys=sixtys):
    out = {}
    for item in sixtys.items():
        re_index_sixty(item[1])
        rename_cols(item[1])
        add_month(item[1])
        drop_cols(item[1])
        out[item[0]] = month_agg(item[1])
    for key in out.keys():
        out[key]['DATAYEAR'] = 2000 + key
    return out

def gentype(row):
    if row['ENERGYSOURCECODE'] == 'Coal Integrated Gasification Combined Cycle' or row['ENERGYSOURCECODE'] == 'Conventional Steam Coal':
        return 'coal'
    elif row['ENERGYSOURCECODE'] == "Natural Gas Fired Combined Cycle" or row['ENERGYSOURCECODE'] == 'Natural Gas Fired Combustion Turbine' or row['ENERGYSOURCECODE'] == 'Natural Gas Internal Combustion Engine' \
    or row['ENERGYSOURCECODE'] == 'Natural Gas Steam Turbine' or row['ENERGYSOURCECODE'] == 'Natural Gas with Compressed Air Storage' or row['ENERGYSOURCECODE'] == 'Other Natural Gas' or row['ENERGYSOURCECODE'] == 'Other Gases'or row['ENERGYSOURCECODE'] == 'Landfill Gas':
        return 'natural_gas'
    elif row['ENERGYSOURCECODE'] == 'Petroleum Coke' or row['ENERGYSOURCECODE'] == 'Petroleum Liquids':
        return 'oil'
    elif row['ENERGYSOURCECODE'] == 'Conventional Hydroelectric' or row['ENERGYSOURCECODE'] == 'Hydroelectric Pumped Storage':
        return 'hydroelectric'
    elif row['ENERGYSOURCECODE'] == 'Geothermal':
        return 'geothermal'
    elif row['ENERGYSOURCECODE'] == 'Onshore Wind Turbine' or row['ENERGYSOURCECODE'] == 'Offshore Wind Turbine':
        return 'wind'
    elif row['ENERGYSOURCECODE'] == 'Solar Photovoltaic' or row['ENERGYSOURCECODE'] == 'Solar Thermal with Energy Storage' or row['ENERGYSOURCECODE'] == 'Solar Thermal without Energy Storage':
        return 'solar'
    elif row['ENERGYSOURCECODE'] == 'Nuclear':
        return 'nuclear'
    elif row['ENERGYSOURCECODE'] == 'ANT' or row['ENERGYSOURCECODE'] == 'BIT' or row['ENERGYSOURCECODE'] == 'COL' or row['ENERGYSOURCECODE'] == 'COM' or row['ENERGYSOURCECODE'] == 'CWM' or row['ENERGYSOURCECODE'] == 'SUB'\
    or row['ENERGYSOURCECODE'] == 'LIG' or row['ENERGYSOURCECODE'] == 'SGC' or row['ENERGYSOURCECODE'] == 'WC' or row['ENERGYSOURCECODE'] == 'RC':
        return 'coal'
    elif row['ENERGYSOURCECODE'] == 'BFG' or row['ENERGYSOURCECODE'] == 'NG' or row['ENERGYSOURCECODE'] == 'OG' or row['ENERGYSOURCECODE'] == 'GAS' or row['ENERGYSOURCECODE'] == 'MTH' or row['ENERGYSOURCECODE'] == 'LNG'\
    or row['ENERGYSOURCECODE'] == 'LPG' or row['ENERGYSOURCECODE'] == 'RG' or row['ENERGYSOURCECODE'] == 'MTH' or row['ENERGYSOURCECODE'] == 'SNG' or row['ENERGYSOURCECODE'] == 'LFG':
        return 'natural_gas'
    elif row['ENERGYSOURCECODE'] == 'DFO' or row['ENERGYSOURCECODE'] == 'JF' or row['ENERGYSOURCECODE'] == 'KER' or row['ENERGYSOURCECODE'] == 'PC' or row['ENERGYSOURCECODE'] == 'PG' or row['ENERGYSOURCECODE'] == 'RFO'\
    or row['ENERGYSOURCECODE'] == 'SGP' or row['ENERGYSOURCECODE'] == 'WO' or row['ENERGYSOURCECODE'] == 'CRU' or row['ENERGYSOURCECODE'] == 'FO1' or row['ENERGYSOURCECODE'] == 'FO2' or row['ENERGYSOURCECODE'] == 'FO3'\
    or row['ENERGYSOURCECODE'] == 'FO4' or row['ENERGYSOURCECODE'] == 'FO5' or row['ENERGYSOURCECODE'] == 'FO6' or row['ENERGYSOURCECODE'] == 'JF' or row['ENERGYSOURCECODE'] == 'KER' or row['ENERGYSOURCECODE'] == 'PET'\
    or row['ENERGYSOURCECODE'] == 'TOP':
        return 'oil'
    elif row['ENERGYSOURCECODE'] == 'WAT':
        return 'hydroelectric'
    elif row['ENERGYSOURCECODE'] == 'GST' or row['ENERGYSOURCECODE'] == 'GEO':
        return 'geothermal'
    elif row['ENERGYSOURCECODE'] == 'WND':
        return 'wind'
    elif row['ENERGYSOURCECODE'] == 'SUN':
        return 'solar'
    elif row['ENERGYSOURCECODE'] == 'NUC' or row['ENERGYSOURCECODE'] == 'UR':
        return 'nuclear'
    else:
        return 'other/unreported'

def re_index_sixtyones(sixtyones=sixtyones):
    for item in sixtyones.items():
            headers = sixtyones[item[0]].iloc[1]
            sixtyones[item[0]] = pd.DataFrame(sixtyones[item[0]].values[2:], columns=headers)

def sixtyones_drop(sixtyones=sixtyones):
    for item in sixtyones.items():
        sixtyones[item[0]] = item[1].iloc[:,[0,1,2,3,4,5,19,20,21]].copy()

def sixtyones_rename(sixtyones=sixtyones):
    for item in sixtyones.items():
        sixtyones[item[0]] = item[1].rename(columns={'THOUSANDSDOLLARS':'TOTALREVENUE','MEGAWATTHOURS':'TOTALSALES','COUNT':'TOTALCUSTOMERS'})
        
def sixtyones_addyear(sixtyones=sixtyones):
    for item in sixtyones.items():
        item[1]['DATAYEAR'] = 2000 + item[0]

def droplast(sixtyones=sixtyones):
    for df in sixtyones.items():
        sixtyones[df[0]] = df[1].iloc[:-1,:]

def clean_sixtyones(sixtyones=sixtyones):
    re_index_sixtyones()
    sixtyones_drop()
    rename_cols(sixtyones)
    sixtyones_rename()
    sixtyones_addyear()
    droplast()

def owntype(row):
        if row['OWNERSHIP'] == 'Municipal' or row['OWNERSHIP'] == 'MUNICIPAL' or row['OWNERSHIP'] == 'Federal' or row['OWNERSHIP'] == 'State' or row['OWNERSHIP'] == 'Political Subdivision':
            return 1
        elif row['OWNERSHIP'] == "COOPERATIVE" or row['OWNERSHIP'] == 'Cooperative' or row['OWNERSHIP'] == 'COOP' or row['OWNERSHIP'] == 'coop':
            return 2
        elif row['OWNERSHIP'] == 'Investor Owned':
            return 3
        elif row['OWNERSHIP'] == 'Behind the Meter':
            return 4
        else:
            return 0

if __name__ == '__main__':
    sixtyone_2016_rev = pd.read_excel('../data/861m/f8262016.xls',sheet_name=0)
    sixtyone_2017_rev = pd.read_excel('../data/861m/retail_sales_2017.xlsx',sheet_name=0)
    sixtyone_2018_rev = pd.read_excel('../data/861m/retail_sales_2018.xlsx',sheet_name=0)
    sixtyone_2019_rev = pd.read_excel('../data/861m/retail_sales_2019.xlsx',sheet_name=0)

    yr = 2016
    sixty_2016_1 = pd.read_excel(f'../data/860m/january_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_2 = pd.read_excel(f'../data/860m/february_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_3 = pd.read_excel(f'../data/860m/march_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_4 = pd.read_excel(f'../data/860m/april_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_5 = pd.read_excel(f'../data/860m/may_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_6 = pd.read_excel(f'../data/860m/june_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_7 = pd.read_excel(f'../data/860m/july_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_8 = pd.read_excel(f'../data/860m/august_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_9 = pd.read_excel(f'../data/860m/september_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_10 = pd.read_excel(f'../data/860m/october_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_11 = pd.read_excel(f'../data/860m/november_generator{yr}.xlsx',sheet_name=0)
    sixty_2016_12 = pd.read_excel(f'../data/860m/december_generator{yr}.xlsx',sheet_name=0)
    yr = 2017
    sixty_2017_1 = pd.read_excel(f'../data/860m/january_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_2 = pd.read_excel(f'../data/860m/february_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_3 = pd.read_excel(f'../data/860m/march_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_4 = pd.read_excel(f'../data/860m/april_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_5 = pd.read_excel(f'../data/860m/may_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_6 = pd.read_excel(f'../data/860m/june_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_7 = pd.read_excel(f'../data/860m/july_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_8 = pd.read_excel(f'../data/860m/august_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_9 = pd.read_excel(f'../data/860m/september_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_10 = pd.read_excel(f'../data/860m/october_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_11 = pd.read_excel(f'../data/860m/november_generator{yr}.xlsx',sheet_name=0)
    sixty_2017_12 = pd.read_excel(f'../data/860m/december_generator{yr}.xlsx',sheet_name=0)
    yr = 2018
    sixty_2018_1 = pd.read_excel(f'../data/860m/january_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_2 = pd.read_excel(f'../data/860m/february_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_3 = pd.read_excel(f'../data/860m/march_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_4 = pd.read_excel(f'../data/860m/april_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_5 = pd.read_excel(f'../data/860m/may_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_6 = pd.read_excel(f'../data/860m/june_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_7 = pd.read_excel(f'../data/860m/july_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_8 = pd.read_excel(f'../data/860m/august_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_9 = pd.read_excel(f'../data/860m/september_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_10 = pd.read_excel(f'../data/860m/october_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_11 = pd.read_excel(f'../data/860m/november_generator{yr}.xlsx',sheet_name=0)
    sixty_2018_12 = pd.read_excel(f'../data/860m/december_generator{yr}.xlsx',sheet_name=0)
    yr = 2019
    sixty_2019_1 = pd.read_excel(f'../data/860m/january_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_2 = pd.read_excel(f'../data/860m/february_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_3 = pd.read_excel(f'../data/860m/march_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_4 = pd.read_excel(f'../data/860m/april_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_5 = pd.read_excel(f'../data/860m/may_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_6 = pd.read_excel(f'../data/860m/june_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_7 = pd.read_excel(f'../data/860m/july_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_8 = pd.read_excel(f'../data/860m/august_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_9 = pd.read_excel(f'../data/860m/september_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_10 = pd.read_excel(f'../data/860m/october_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_11 = pd.read_excel(f'../data/860m/november_generator{yr}.xlsx',sheet_name=0)
    sixty_2019_12 = pd.read_excel(f'../data/860m/december_generator{yr}.xlsx',sheet_name=0)

    sixty_2016 = {1:sixty_2016_1,2:sixty_2016_2,3:sixty_2016_3,4:sixty_2016_4
              ,5:sixty_2016_5,6:sixty_2016_6,7:sixty_2016_7,8:sixty_2016_8
              ,9:sixty_2016_9,10:sixty_2016_10,11:sixty_2016_11,12:sixty_2016_12}

    sixty_2017 = {1:sixty_2017_1,2:sixty_2017_2,3:sixty_2017_3,4:sixty_2017_4
                ,5:sixty_2017_5,6:sixty_2017_6,7:sixty_2017_7,8:sixty_2017_8
                ,9:sixty_2017_9,10:sixty_2017_10,11:sixty_2017_11,12:sixty_2017_12}

    sixty_2018 = {1:sixty_2018_1,2:sixty_2018_2,3:sixty_2018_3,4:sixty_2018_4
                ,5:sixty_2018_5,6:sixty_2018_6,7:sixty_2018_7,8:sixty_2018_8
                ,9:sixty_2018_9,10:sixty_2018_10,11:sixty_2018_11,12:sixty_2018_12}

    sixty_2019 = {1:sixty_2019_1,2:sixty_2019_2,3:sixty_2019_3,4:sixty_2019_4
                ,5:sixty_2019_5,6:sixty_2019_6,7:sixty_2019_7,8:sixty_2019_8
                ,9:sixty_2019_9,10:sixty_2019_10,11:sixty_2019_11,12:sixty_2019_12}

    sixtys = {16:sixty_2016,17:sixty_2017,18:sixty_2018,19:sixty_2019}

    sixtys_clean = clean_agg_sixtys()
    sixtys_clean_f = {}
    for df in sixtys_clean.items():
        sixtys_clean_f[df[0]] = df[1].drop(columns=['TECHNOLOGY','PRIMEMOVERCODE', 'OPERATINGMONTH', 'OPERATINGYEAR',
                                            'PLANNEDRETIREMENTMONTH', 'PLANNEDRETIREMENTYEAR', 'STATUS',
                                            'PLANNEDDERATEYEAR', 'PLANNEDDERATEMONTH',
                                            'PLANNEDDERATEOFSUMMERCAPACITY(MW)', 'PLANNEDUPRATEYEAR',
                                                'PLANNEDUPRATEMONTH', 'PLANNEDUPRATEOFSUMMERCAPACITY(MW)', 'COUNTY','BALANCINGAUTHORITYCODE',
                                                'GOOGLEMAP','BINGMAP', 'UNITCODE','SECTOR','PLANTSTATE','GENERATORID'],errors='ignore').copy()
        sixtys_clean_f[df[0]] =  sixtys_clean_f[df[0]].iloc[:-1,:]
    
    sixtys_full = sixtys_clean_f[16]
    i = 0
    for df in sixtys_clean_f.items():
        if i >= 1:
            sixtys_full = pd.concat([sixtys_full,df[1]],axis=0,ignore_index=True)
        i += 1

    sixtys_full = sixtys_full.replace(r'^\s*$', np.nan, regex=True)
    sixtys_full['NETSUMMERCAPACITY(MW)'].fillna(sixtys_full['NAMEPLATECAPACITY(MW)'], inplace=True)
    sixtys_full['NAMEPLATECAPACITY(MW)'].fillna(sixtys_full['NETSUMMERCAPACITY(MW)'], inplace=True)
    sixtys_full['NETWINTERCAPACITY(MW)'].fillna(sixtys_full['NAMEPLATECAPACITY(MW)'], inplace=True)
    sixtys_full = sixtys_full.dropna()

    sixtys_full['GEN_TYPE'] = sixtys_full.apply (lambda row: gentype(row), axis=1)

    sixtys_full = sixtys_full.infer_objects()
    sixtys_full = sixtys_full.rename(columns={'Month':'MONTH','UTILITYID':'UTILITYNUMBER'})
    sixtys_full = sixtys_full.drop(columns=['ENERGYSOURCECODE'])

    sixtys_full.to_csv('../data/860m_clean.csv',index=False)

    sixtyones = {16:sixtyone_2016_rev,17:sixtyone_2017_rev,18:sixtyone_2018_rev,
           19:sixtyone_2019_rev}
           
    clean_sixtyones()
    sixtyones_full = sixtyones[16]
    i = 0
    for df in sixtyones.items():
        if i >= 1:
            sixtyones_full = pd.concat([sixtyones_full,df[1]],axis=0,ignore_index=True)
        i += 1

    sixtyones_full['OWNERTYPE'] = sixtyones_full.apply (lambda row: owntype(row), axis=1)

    f = sixtyones_full.TOTALREVENUE.where(sixtyones_full.TOTALREVENUE=='.').isna()
    sixtyones_full = sixtyones_full[f]
    f = sixtyones_full.TOTALSALES.where(sixtyones_full.TOTALSALES=='.').isna()
    sixtyones_full = sixtyones_full[f]
    sixtyones_full = sixtyones_full.drop(columns=['OWNERSHIP'])
    sixtyones_full = sixtyones_full.infer_objects()
    f = sixtyones_full.UTILITYNUMBER.where(sixtyones_full.UTILITYNUMBER==0).isna()
    sixtyones_full = sixtyones_full[f]
    f = sixtyones_full.UTILITYNUMBER.where(sixtyones_full.UTILITYNUMBER==88888).isna()
    sixtyones_full = sixtyones_full[f]
    f = sixtyones_full.TOTALREVENUE.where(sixtyones_full.TOTALREVENUE==0).isna()
    sixtyones_full = sixtyones_full[f]
    f = sixtyones_full.TOTALSALES.where(sixtyones_full.TOTALSALES==0).isna()
    sixtyones_full =sixtyones_full[f]
    sixtyones_group = sixtyones_full.groupby(['DATAYEAR','MONTH','UTILITYNUMBER','UTILITYNAME']).agg({'TOTALREVENUE':'sum','TOTALSALES':'sum','TOTALCUSTOMERS':'sum','OWNERTYPE':'max'})
    sixtyones_group =sixtyones_group.reset_index()

    sixtyones_full.to_csv('../data/861m_state_clean.csv',index=False)
    sixtyones_group.to_csv('../data/861m_clean.csv',index=False)

    # COMBINING DATASETS
    sixtys_combine = sixtys_full.drop(columns=['LATITUDE','LONGITUDE','PLANTID','PLANTNAME']).copy()
    y = pd.get_dummies(sixtys_combine.GEN_TYPE, prefix='is')
    sixtys_combine = pd.concat([sixtys_combine, y],axis=1)
    sixtys_combine = sixtys_combine.drop(columns=['GEN_TYPE'])
    full_dirty = pd.merge(left=sixtys_combine,right=sixtyones_group,on=['DATAYEAR','MONTH','UTILITYNUMBER'])

    full_dirty['MW_COAL'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_coal']
    full_dirty['MW_GEOTHERMAL'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_geothermal']
    full_dirty['MW_HYDROELECTRIC'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_hydroelectric']
    full_dirty['MW_NATURAL_GAS'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_natural_gas']
    full_dirty['MW_NUCLEAR'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_nuclear']
    full_dirty['MW_OIL'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_oil']
    full_dirty['MW_OTHER'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_other/unreported']
    full_dirty['MW_SOLAR'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_solar']
    full_dirty['MW_WIND'] = full_dirty['NAMEPLATECAPACITY(MW)']*full_dirty['is_wind']

    combine = full_dirty.groupby(['DATAYEAR','MONTH','UTILITYNUMBER']).agg({'NETSUMMERCAPACITY(MW)':'sum','NETWINTERCAPACITY(MW)':'sum','NAMEPLATECAPACITY(MW)':'sum'
                                                                       ,'is_coal':'mean','is_geothermal':'mean','is_hydroelectric':'mean','is_natural_gas':'mean'
                                                                       ,'is_nuclear':'mean','is_oil':'mean','is_other/unreported':'mean','is_solar':'mean','is_wind':'mean'
                                                                        ,'MW_COAL':'sum','MW_GEOTHERMAL':'sum','MW_HYDROELECTRIC':'sum','MW_NATURAL_GAS':'sum'
                                                                       ,'MW_NUCLEAR':'sum','MW_OIL':'sum','MW_OTHER':'sum','MW_SOLAR':'sum','MW_WIND':'sum'
                                                                       ,'TOTALREVENUE':'mean','TOTALSALES':'mean','TOTALCUSTOMERS':'mean'})
    combine = combine.reset_index()

    combine.to_csv('../data/combined.csv',index=False)