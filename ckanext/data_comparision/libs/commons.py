# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import clevercsv



RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'


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



    @staticmethod   
    def get_resource_type(resource_id):
        '''
            Get a data resource type.

            Args:
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - the resource type as String
        '''

        resource = toolkit.get_action('resource_show')({}, {'id': resource_id})
        if resource['format'] in ['CSV'] or '.csv' in  resource['name']: 
            return 'csv'
        if resource['format'] in ['XLSX'] or '.xlsx' in  resource['name']: 
            return 'xlsx'

        return None
    


    @staticmethod
    def csv_to_dataframe(resource_id):
        '''
            Read a csv file as pandas dataframe.

            Args:
                - resource_id: the data resource id in ckan
            
            Returns:
                - a python dataframe
        '''

        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        df = clevercsv.read_dataframe(file_path)

        return df

