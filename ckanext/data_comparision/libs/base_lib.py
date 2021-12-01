# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.model import Package
import clevercsv
import pandas as pd


RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'

class Helper():

    '''
        check the user can see a dataset or not
    '''
    def check_access_view_package(package_id):
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':package_id}
        try:
            toolkit.check_access('package_show', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return False
    

    def get_all_datasets():
        datasets = Package.search_by_name('')
        result = []
        for dt in datasets:
            if dt.state == 'active' and dt.type == 'dataset' and Helper.check_access_view_package(dt.id):
                result.append(dt)
        return result
    
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

    
    def get_data(package_id, resource_id, file_type):
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        if file_type == 'csv':
            result = []
            try:
                df = clevercsv.read_dataframe(file_path)
                for index, row in df.iterrows():
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
    

    def get_one_column(resource_id, column_name, file_type):
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        if file_type == 'csv':
            try:
                df = clevercsv.read_dataframe(file_path)
                return list(df[column_name])

            except:
                return None


    

    

            