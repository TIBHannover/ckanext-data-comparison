# encoding: utf-8

from flask import render_template, request
import ckan.plugins.toolkit as toolkit
from ckanext.data_comparision.libs.base_lib import Helper
import json

from ckanext.data_comparision.libs.template_helper import TemplateHelper

class BaseController():
    '''
        The controller class contains the Plugin logic.
    '''


    @staticmethod
    def base_view(package_name, resId):
        '''
            The function for rendering the plugin index page.

            Method:
                - GET

            Args:
                - package_name: the target dataset name
                - resId: The target data resource id in ckan

            Returns:
                - The base_index.html page        
        '''

        datasets = Helper.get_all_datasets()
        package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
        resource = toolkit.get_action('resource_show')({}, {'id': resId})

        return render_template('base_index.html', 
            datasets=datasets,
            pkg_dict=package,
            package=package,
            resource=resource
        
        )
    

    @staticmethod
    def process_columns():
        '''
            The function for processing the selected data columns.

            Method:
                - POST

            Returns:
                - ???        
        '''

        columns_data = request.form.getlist('columns[]')       
        result_columns = {}        
        for value in columns_data:
            print(value)
            print('--------------------------------------&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            temp = value.split('@_@')
            resource_id = temp[0]
            col_name = temp[1]
            col_data = Helper.get_one_column(resource_id, col_name)
            if col_data:
                result_columns[col_name] = col_data
            

        return json.dumps(result_columns)
    


    @staticmethod
    def import_data():
        '''
            Import data from selected resources in the browes view.

            Method:
                - POST

            Returns:
                - The dictionary contains html tables. The key is a resource id, and the value is the table.        
        '''

        resources = request.form.getlist('resources[]') 
        imported_tables = {}
        for res_id in resources:
            imported_tables[res_id] = Helper.get_resource_table(res_id, 1, True)

        return json.dumps(imported_tables)
    

    
    @staticmethod
    def load_new_page():
        '''
            Load new data page for a table.

            Method:
                - POST

            Returns:
                - An html table contains the new page data        
        '''

        page_number = request.form.get('page')
        resource_id = request.form.get('resourceId')
        table = Helper.get_resource_table(resource_id, int(page_number), False)
        if not table:
            return '0'

        return json.dumps({'table': table})