# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from ckan.model import Package


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
            