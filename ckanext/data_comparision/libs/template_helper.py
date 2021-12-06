# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import clevercsv
import pandas as pd


RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'
PAGINATION_SIZE = 50

class TemplateHelper():
    '''
        The class that provides Helper functions for ckan template (ITemplateHelpers). 
    '''
    
    @staticmethod
    def is_csv(resource):
        '''
            Check if a data resource in csv or not.

            Args:
                - resource: the data resource object.
            
            Returns:
                - Boolean        
        '''

        if resource.format in ['CSV']:
            return True
        if  '.csv' in  resource.name:
            return True 
        return False

    
    @staticmethod
    def is_xlsx(resource):
        '''
            Check if a data resource in xlsx or not.

            Args:
                - resource: the data resource object.
            
            Returns:
                - Boolean        
        '''

        if resource.format in ['XLSX']:
            return True
        if  '.xlsx' in  resource.name:
            return True 
        return False



    @staticmethod   
    def get_resource_type(resource_id):
        '''
            Get a data resource type.

            Args:
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - the resource type as String
        '''

        resource = toolkit.get_action('resource_show')({}, {'id': resource_id})
        if resource['format'] in ['CSV'] or '.csv' in  resource['name']: 
            return 'csv'
        if resource['format'] in ['XLSX'] or '.xlsx' in  resource['name']: 
            return 'xlsx'

        return None

    
    
    @staticmethod
    def get_data(resource_id, page):
        '''
            Get a ckan data reosurce table data.

            Args:
                - resource_id: the id of the target data resource in ckan
                - page: page number for pagination
            
            Returns:
                - list of data rows (list of lists)
        '''


        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        lower_bound = (page -1) * PAGINATION_SIZE
        upper_bound = page * PAGINATION_SIZE
        file_type = TemplateHelper.get_resource_type(resource_id)
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
    


    @staticmethod
    def get_columns(resource_id):
        '''
            Get a ckan data reosurce table column.

            Args:
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - list of columns names
        '''

        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        file_type = TemplateHelper.get_resource_type(resource_id)
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
    

    @staticmethod
    def get_max_table_page_count(resource_id):
        '''
            Calculate max number of pages for a data table.

            Args:
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - Max page count
        '''

        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        file_type = TemplateHelper.get_resource_type(resource_id)
        if file_type == 'csv':
            try:
                df = clevercsv.read_dataframe(file_path)
                return int(len(df) / PAGINATION_SIZE) + 1

            except:
                return 1

        return 1
    
    


    

    

            