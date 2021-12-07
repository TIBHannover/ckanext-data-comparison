# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.model import Package
import clevercsv
import pandas as pd
from ckanext.data_comparision.libs.template_helper import TemplateHelper
from ckanext.data_comparision.libs.table_builder import Builder
from itertools import zip_longest


RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'

class Helper():
    '''
        The Helper class includes functions that preform the plugin functionalities.
    '''

    @staticmethod
    def check_access_view_package(package_id):
        '''
            Check a user can view a dataset in ckan or not.

            Args:
                - package_id: the datset id in ckan
            
            Returns:
                - Boolean
        '''
        
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':package_id}
        try:
            toolkit.check_access('package_show', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return False
    

    @staticmethod
    def check_access_view_resource(resource_id):
        '''
            Check a user can view a data resource in ckan or not.

            Args:
                - resource_id: the data resource id in ckan
            
            Returns:
                - Boolean
        '''
        
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':resource_id}
        try:
            toolkit.check_access('resource_show', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return toolkit.abort(403, "You do not have the required authorization.")

    

    @staticmethod
    def get_all_datasets():
        '''
             Return all datasets in ckan that are: active, authoriezed for the user, and contain csv/xlsx resources.
            
            Returns:
                - A list of ckan datasets
        '''

        datasets = Package.search_by_name('')
        result = []
        for dt in datasets:
            if dt.state == 'active' and dt.type == 'dataset' and Helper.check_access_view_package(dt.id) and Helper.dataset_has_csv_xlsx(dt):
                result.append(dt)
        return result
    
   
    
    @staticmethod
    def get_one_column(resource_id, column_name):
        '''
            Return the data of one column in a data resource table.

            Args:
                - resource_id: the data resource id in ckan
                - column_name: target column name
            
            Returns:
                - list of the column data
        '''
        
        Helper.check_access_view_resource(resource_id)
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        file_type = TemplateHelper.get_resource_type(resource_id)
        if file_type == 'csv':
            try:
                df = clevercsv.read_dataframe(file_path)
                return list(df[column_name])

            except:
                return None
    

    
    @staticmethod
    def dataset_has_csv_xlsx(dataset):
        '''
            Check if a dataset contains csv or xlsx data resource.

            Args:
                - dataset: the target dataset in ckan
            
            Returns:
                - Boolean
        '''

        for resource in dataset.resources:
            if TemplateHelper.is_csv(resource) or TemplateHelper.is_xlsx(resource):
                return True
        return False
    
    

    @staticmethod
    def get_resource_table(resource_id, page, load_first_time):
        '''
            Create a data resource html table.

            Args:
                - resource_id: the data resource id in ckan
                - page: the data table page number (pagination)
                - load_first_time: is the table loading first time or not (pagination page changes)
            
            Returns:
                - The html table for the target data resource.
        '''

        Helper.check_access_view_resource(resource_id)
        columns = TemplateHelper.get_columns(resource_id)
        data_rows = TemplateHelper.get_data(resource_id, page)
        max_page = TemplateHelper.get_max_table_page_count(resource_id)
        if page > max_page or page < 1:
            return None
        
        return Builder.build_data_table(resource_id, columns, data_rows, max_page, load_first_time)
    

    @staticmethod
    def gather_data_from_columns(columns_data):
        '''
            Gathers data from different columns in different data resources.

            Args:
                - columns_data: the list of resource/column strings. Each element has the target data resource id and column name
                    separated by @_@. for Example: resource_x_id@_@column_name.

            Returns:
                - A dictionary in which the key is the column name and the value is a list of values for that column. 
        '''

        result_columns = {}        
        for value in columns_data:
            if '@_@' in value:
                resource_id = value.split('@_@')[0]
                Helper.check_access_view_resource(resource_id)
                col_name = value.split('@_@')[1]
                col_data = Helper.get_one_column(resource_id, col_name)
                if col_data:
                    result_columns[col_name] = col_data
        

        return result_columns
    

    @staticmethod
    def prepare_data_for_download(data_dict):
        '''
            Prepares the data resource for downloading.

            Args:
                - data_dict: the dictionary of selected data columns. the key is the column name and the value is the column values.

            Returns:
                - list of dataframes rows
        '''

        result_rows = []
        columns_names = data_dict.keys()
        result_rows.append(columns_names)
        body = data_dict.values()
        zipped_body = zip_longest(*body)
        for row in zipped_body:
            result_rows.append(list(row))

        return result_rows


   
    

    

            