# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import clevercsv
import pandas as pd


RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'
PAGINATION_SIZE = 50

class TemplateHelper():
 
    def is_csv(resource):
        if resource.format in ['CSV']:
            return True
        if  '.csv' in  resource.name:
            return True 
        return False

    
    def is_xlsx(resource):
        if resource.format in ['XLSX']:
            return True
        if  '.xlsx' in  resource.name:
            return True 
        return False

    
    '''
        Return a table data to a template view
    '''
    def get_data(package_id, resource_id, page, file_type):
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        lower_bound = (page -1) * PAGINATION_SIZE
        upper_bound = page * PAGINATION_SIZE
        if file_type == 'csv':
            result = []
            try:
                df = clevercsv.read_dataframe(file_path)
                if upper_bound > len(df):
                    upper_bound = len(df)
                
                for index, row in df.iloc[lower_bound:upper_bound].iterrows():                    
                    result.append(list(row))
                    
                return result

            except:
                return []

        if file_type == 'xlsx':
            data = {}
            try:
                data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
                for sheet in data_sheets.keys():
                    temp_df = data_sheets[sheet].dropna(how='all').dropna(how='all', axis=1)
                    headers = temp_df.iloc[0]
                    final_data_df  = pd.DataFrame(temp_df.values[1:], columns=headers)
                    data[sheet] = list(final_data_df.columns)
                return data

            except:
                return {'Error': []}
    


    '''
        Return a table columns to a template view
    '''
    def get_columns(package_id, resource_id, file_type):
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        if file_type == 'csv':
            try:
                df = clevercsv.read_dataframe(file_path)
                return list(df.columns)

            except:
                return ['Error']

        if file_type == 'xlsx':
            data = {}
            try:
                data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
                for sheet in data_sheets.keys():
                    temp_df = data_sheets[sheet].dropna(how='all').dropna(how='all', axis=1)
                    headers = temp_df.iloc[0]
                    final_data_df  = pd.DataFrame(temp_df.values[1:], columns=headers)
                    data[sheet] = list(final_data_df.columns)
                return data

            except:
                return {'Error': []}
    
    


    

    

            