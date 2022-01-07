# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.model import Package
from ckanext.data_comparision.libs.template_helper import TemplateHelper
from ckanext.data_comparision.libs.table_builder import Builder
from ckanext.data_comparision.libs.commons import Commons
from itertools import zip_longest


RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'

class Helper():
    '''
        The Helper class includes functions that preform the plugin functionalities.
    '''


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
            if dt.state == 'active' and dt.type == 'dataset' and Commons.check_access_view_package(dt.id) and Helper.dataset_has_csv_xlsx(dt):
                result.append(dt)
        return result
    
   
    
    @staticmethod
    def get_one_column(resource_id, sheet, column_name):
        '''
            Return the data of one column in a data resource table.

            Args:
                - resource_id: the data resource id in ckan
                - sheet: name of the target sheet in a xlsx data resource
                - column_name: target column name
            
            Returns:
                - list of the column data
        '''
        
        Commons.check_access_view_resource(resource_id)
        file_type = Commons.get_resource_type(resource_id)
        df = None
        try:
            if file_type == 'csv':
                df = Commons.csv_to_dataframe(resource_id)

            elif file_type == 'xlsx':
                df = Commons.xlsx_to_dataframe(resource_id)[sheet] 
            
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
    def get_resource_table(resource_id, sheet, page, load_first_time):
        '''
            Create a data resource html table.

            Args:
                - resource_id: the data resource id in ckan
                - sheet: the data sheet in case of xlsx
                - page: the data table page number (pagination)
                - load_first_time: is the table loading first time or not (pagination page changes)
            
            Returns:
                - The html table for the target data resource.
        '''

        Commons.check_access_view_resource(resource_id)
        columns = TemplateHelper.get_columns(resource_id)
        if sheet != 'None': # xlsx file
            columns = columns[sheet]
        data_rows = TemplateHelper.get_data(resource_id, page, sheet)
        max_page = TemplateHelper.get_max_table_page_count(resource_id, sheet)
        if page > max_page or page < 1:
            return None
        
        return Builder.build_data_table(resource_id, sheet, columns, data_rows, max_page, load_first_time)
    


    @staticmethod
    def gather_data_from_columns(columns_data):
        '''
            Gathers data from different columns in different data resources.

            Args:
                - columns_data: the list of resource/column strings. Each element has the target data resource id and column name
                    separated by @_@. for Example: resource_x_id@_@column_name@_@dbClickValue.

            Returns:
                - A dictionary in which the key is the column name placeholder and the value is a list of values for that column. 
                - A dictionary that contains the columns' name placeholder references:
                    [column name, resource url]
        '''

        result_columns = {}
        column_name_prefix = 'F_' 
        column_references = {}
        column_number = 1
        for value in columns_data:
            if '@_@' in value:
                resource_id_raw = value.split('@_@')[0]
                col_name = value.split('@_@')[1]
                resource_id, sheet = Commons.process_resource_id(resource_id_raw)                                
                Commons.check_access_view_resource(resource_id)
                col_data = Helper.get_one_column(resource_id, sheet, col_name)
                col_name_placeholder = column_name_prefix + str(column_number)
                resource = toolkit.get_action('resource_show')({}, {'id': resource_id})
                package = toolkit.get_action('package_show')({}, {'name_or_id': resource['package_id']})
                res_url = h.url_for('dataset_resource.read', resource_id=resource['id'], package_type=package['type'], id=package['id'], _external=True)
                if col_data and col_name not in result_columns.keys() and sheet == 'None': #csv 
                    result_columns[col_name_placeholder] = col_data
                    column_references[col_name_placeholder] = [col_name, res_url]

                elif col_data and col_name not in result_columns.keys() and sheet != 'None': #xlsx                    
                    result_columns[col_name_placeholder] = col_data
                    column_references[col_name_placeholder + ' (sheet: ' + sheet + ')'] = [col_name, res_url]
               
                column_number += 1

        return [result_columns, column_references]
    


    @staticmethod
    def prepare_data_for_download(data_dict, columns_refs):
        '''
            Prepares the data resource for downloading.

            Args:
                - data_dict: the dictionary of selected data columns. the key is the column name and the value is the column values.
                - columns_refs: the dictionary of columns placeholder and their resource url in ckan.

            Returns:
                - list of dataframes rows
        '''

        result_rows = []
        body = data_dict.values()
        zipped_body = zip_longest(*body)
        for col, ref in columns_refs.items():
            refs = [col, ref[0], ref[1]]
            result_rows.append(refs)
        
        result_rows.append([])
        result_rows.append([])
        result_rows.append([])
        columns_names = data_dict.keys()
        result_rows.append(columns_names)

        for row in zipped_body:
            result_rows.append(list(row))
    
        return result_rows
    

    # @staticmethod
    # def get_y_value(x_value, x_column_name, y_column_name, resource_id):
    #     '''
    #         Get the y-axis value based on the selected x-axis in a data resource.

    #         Args:
    #             - x_value: the value of x
    #             - x_column_name: the x variable column name
    #             - y_column_name: the y variable column name
    #             - resource_id: the target data resource in ckan
            
    #         Returns:
    #             - A numeric value or 0 in case the x value does not exist.
    #     '''




   
    

    

            