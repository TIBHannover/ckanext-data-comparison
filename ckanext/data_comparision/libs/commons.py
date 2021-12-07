# encoding: utf-8

import ckan.plugins.toolkit as toolkit


class Commons():
    '''
        The class contains the common functions used by other libraries.
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

