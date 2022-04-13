# encoding: utf-8

from unicodedata import name
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
        format = ''
        name = ''
        if isinstance(resource, dict):
            format = resource['format']
            name = resource['name']
        else:
            format = resource.format
            name = resource.name
        
        return (format in ['CSV']) or ('.csv' in name)

    
    @staticmethod
    def is_xlsx(resource):
        '''
            Check if a data resource in xlsx or not.

            Args:
                - resource: the data resource object.
            
            Returns:
                - Boolean        
        '''

        format = ''
        name = ''
        if isinstance(resource, dict):
            format = resource['format']
            name = resource['name']
        else:
            format = resource.format
            name = resource.name
        
        return (format in ['XLSX']) or ('.xlsx' in name)
    
    
    @staticmethod
    def get_data(resource_id, page, sheet_name=None):
        '''
            Get a ckan data reosurce table data.

            Args:
                - resource_id: the id of the target data resource in ckan
                - page: page number for pagination
                - sheet_name: the name of the target sheet in the xlsx data resource
            
            Returns:
                - list of data rows (list of lists)
        '''

        lower_bound = (page -1) * PAGINATION_SIZE
        upper_bound = page * PAGINATION_SIZE
        file_type = Commons.get_resource_type(resource_id)
        result = []
        df = None
        try:
            if file_type == 'csv':
                df = Commons.csv_to_dataframe(resource_id)
            if file_type == 'xlsx':
                df = Commons.xlsx_to_dataframe(resource_id)[sheet_name]
            
            if upper_bound > len(df):
                upper_bound = len(df)
            for index, row in df.iloc[lower_bound:upper_bound].iterrows():                    
                result.append(list(row))
            
            return result
            
        except:
            return []

       
    


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

        if file_type == 'xlsx':
            columns = {}
            try:
                excel_data = Commons.xlsx_to_dataframe(resource_id)
                for sheet, df in excel_data.items():
                    columns[sheet] = list(df.columns)
                
                return columns

            except:
                # raise
                return {'Error': []}
    

    @staticmethod
    def get_max_table_page_count(resource_id, sheet_name=None):
        '''
            Calculate max number of pages for a data table.

            Args:
                - resource_id: the id of the target data resource in ckan
                - sheet_name: the name of the target sheet in the xlsx data resource
            
            Returns:
                - Max page count
        '''

        file_type = Commons.get_resource_type(resource_id)
        df = None
        try:
            if file_type == 'csv':
                df = Commons.csv_to_dataframe(resource_id)
            if file_type == 'xlsx':
                df = Commons.xlsx_to_dataframe(resource_id)[sheet_name]
            
            return int(len(df) / PAGINATION_SIZE) + 1
        
        except:
            return 1

    
    


    

    

            