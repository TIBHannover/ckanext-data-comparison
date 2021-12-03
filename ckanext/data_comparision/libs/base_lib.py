# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.model import Package
import clevercsv
import pandas as pd
from ckanext.data_comparision.libs.template_helper import TemplateHelper
from ckanext.data_comparision.libs.table_builder import Builder


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
    

    '''
        Return all site datasets which has CSV or/and XLSX
    '''
    def get_all_datasets():
        datasets = Package.search_by_name('')
        result = []
        for dt in datasets:
            if dt.state == 'active' and dt.type == 'dataset' and Helper.check_access_view_package(dt.id) and Helper.dataset_has_csv_xlsx(dt):
                result.append(dt)
        return result
    
   
    
    '''
        Return the data of one column in a dataframe
    '''
    def get_one_column(resource_id, column_name):
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        file_type = TemplateHelper.get_resource_type(resource_id)
        if file_type == 'csv':
            try:
                df = clevercsv.read_dataframe(file_path)
                return list(df[column_name])

            except:
                return None
    

    '''
        Check if a dataset contains csv or xlsx data resource
    '''
    def dataset_has_csv_xlsx(dataset):
        for resource in dataset.resources:
            if TemplateHelper.is_csv(resource) or TemplateHelper.is_xlsx(resource):
                return True
        return False
    

    '''
        Return a dataframe inside from a resource 
    '''
    def get_resource_table(resource_id, page, load_first_time):
        columns = TemplateHelper.get_columns('', resource_id)
        data_rows = TemplateHelper.get_data('', resource_id, page)
        max_page = TemplateHelper.get_max_table_page_count(resource_id)
        if page > max_page or page < 1:
            return None
        
        return Builder.build_data_table(resource_id, columns, data_rows, max_page, load_first_time)


   
    

    

            