# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.model import Package
import clevercsv


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

    
    def get_columns(package_id, resource_id, file_type):
        if file_type == 'csv':
            try:
                file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
                df = clevercsv.read_dataframe(file_path)
                return list(df.columns)

            except:
                return ['Error']
    

            