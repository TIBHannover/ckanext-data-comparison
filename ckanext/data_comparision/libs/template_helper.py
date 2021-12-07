# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import pandas as pd
from ckanext.data_comparision.libs.commons import Commons


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
    def get_data(resource_id, page):
        '''
            Get a ckan data reosurce table data.

            Args:
                - resource_id: the id of the target data resource in ckan
                - page: page number for pagination
            
            Returns:
                - list of data rows (list of lists)
        '''

        lower_bound = (page -1) * PAGINATION_SIZE
        upper_bound = page * PAGINATION_SIZE
        file_type = Commons.get_resource_type(resource_id)
        if file_type == 'csv':
            result = []
            try:
                df = Commons.csv_to_dataframe(resource_id)
                if upper_bound > len(df):
                    upper_bound = len(df)
                
                for index, row in df.iloc[lower_bound:upper_bound].iterrows():                    
                    result.append(list(row))
                    
                return result

            except:
                return []

        # if file_type == 'xlsx':
        #     data = {}
        #     try:
        #         data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
        #         for sheet in data_sheets.keys():
        #             temp_df = data_sheets[sheet].dropna(how='all').dropna(how='all', axis=1)
        #             headers = temp_df.iloc[0]
        #             final_data_df  = pd.DataFrame(temp_df.values[1:], columns=headers)
        #             data[sheet] = list(final_data_df.columns)
        #         return data

        #     except:
        #         return {'Error': []}
    


    @staticmethod
    def get_columns(resource_id):
        '''
            Get a ckan data reosurce table column.

            Args:
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - list of columns names
        '''

        file_type = Commons.get_resource_type(resource_id)
        if file_type == 'csv':
            try:
                df = Commons.csv_to_dataframe(resource_id)
                return list(df.columns)

            except:
                return ['Error']

        # if file_type == 'xlsx':
        #     data = {}
        #     try:
        #         data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
        #         for sheet in data_sheets.keys():
        #             temp_df = data_sheets[sheet].dropna(how='all').dropna(how='all', axis=1)
        #             headers = temp_df.iloc[0]
        #             final_data_df  = pd.DataFrame(temp_df.values[1:], columns=headers)
        #             data[sheet] = list(final_data_df.columns)
        #         return data

        #     except:
        #         return {'Error': []}
    

    @staticmethod
    def get_max_table_page_count(resource_id):
        '''
            Calculate max number of pages for a data table.

            Args:
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - Max page count
        '''

        file_type = Commons.get_resource_type(resource_id)
        if file_type == 'csv':
            try:
                df = Commons.csv_to_dataframe(resource_id)
                return int(len(df) / PAGINATION_SIZE) + 1

            except:
                return 1

        return 1
    
    


    

    

            