# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.model import Package
import pandas as pd


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
    
    def is_csv_or_xlsx(resource):
        if resource.format in ['CSV', 'XLSX']:
            return True
        if  '.csv' in  resource.name or '.xlsx' in  resource.name:
            return True 
        return False

    
    def get_file(package_id, resource_id):
        link = h.url_for('dataset.resource_download', id=str(package_id), resource_id=resource_id  ,  _external=True)
        df = pd.read_csv(link, index_col=0)
        # print(df.columns)
        # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        return list(df.columns)
    

            