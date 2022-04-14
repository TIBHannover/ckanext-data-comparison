# encoding: utf-8

from re import X
from unicodedata import name
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import pandas as pd
from ckanext.data_comparision.libs.commons import Commons
import clevercsv


PAGINATION_SIZE = 50
RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'
X_ANNOTATION = "X-Kategorie"
Y_ANNOTATION = "Y-Kategorie"

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
    


    @staticmethod
    def get_column_anotation(resource_id, column_name, sheet_name=None):
        '''
            Get the column "x-axis/y-axis" tag for the table view. The tag is based on column annotation (if exists)

            Args:
                - resource_id
                - column_name
                - sheet_name (for xlsx files)
            
            Return:
                - 'x' | 'y' | ''
        '''

        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]

        if Commons.get_resource_type(resource_id) == 'csv':
            df = clevercsv.read_dataframe(file_path)
            if Commons.is_possible_to_automate(df):
                if column_name in list(df[X_ANNOTATION]):
                    return 'x'
                elif column_name in list(df[Y_ANNOTATION]):
                    return 'y'
                else:
                    return ''
        
            else:
                return ''
        
        if Commons.get_resource_type(resource_id) == 'xlsx':
             data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
             for sheet, data_f in data_sheets.items():
                if sheet != sheet_name or len(data_f) == 0:
                    continue
                
                if 0 in list(data_f.columns):
                    actual_headers = data_f.iloc[0]
                    data_f = data_f[1:]
                    data_f.columns = actual_headers
                
                data_f.columns = [header.strip() for header in data_f.columns]
                if Commons.is_possible_to_automate(data_f):
                    if column_name in list(data_f[X_ANNOTATION]):
                        return 'x'
                    elif column_name in list(data_f[Y_ANNOTATION]):
                        return 'y'
                    else:
                        return ''
                else:
                    return ''

        return ''

    
    


    

    

            