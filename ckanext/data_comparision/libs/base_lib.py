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
    
   
    

    def get_one_column(resource_id, column_name, file_type):
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        if file_type == 'csv':
            try:
                df = clevercsv.read_dataframe(file_path)
                return list(df[column_name])

            except:
                return None


    

    

            