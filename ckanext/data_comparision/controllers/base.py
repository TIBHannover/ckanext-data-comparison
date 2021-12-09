# encoding: utf-8

from flask import render_template, request, make_response
import ckan.plugins.toolkit as toolkit
from ckanext.data_comparision.libs.base_lib import Helper
import json
import csv
from io import StringIO
from ckanext.data_comparision.libs.commons import Commons


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
        result_columns = Helper.gather_data_from_columns(columns_data)        
            
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
        resource_id, sheet = Commons.process_resource_id(request.form.get('resourceId'))
        table = Helper.get_resource_table(resource_id, sheet, int(page_number), False)
        if not table:
            return '0'

        return json.dumps({'table': table})
    

    @staticmethod
    def download_file():
        '''
            Download the selcted data columns as a csv file.

            Method:
                - POST

            Return:
                - A csv file
        '''

        try:
            columns_data = request.form.getlist('columns[]')
            csv_data_dict = Helper.gather_data_from_columns(columns_data)
            csv_data = Helper.prepare_data_for_download(csv_data_dict)
            string_io_object = StringIO()
            csv_writer_object = csv.writer(string_io_object)
            csv_writer_object.writerows(csv_data)
            csv_file = make_response(string_io_object.getvalue())
            csv_file.headers["Content-Disposition"] = "attachment; filename=export.csv"
            csv_file.headers["Content-type"] = "text/csv"
            return csv_file
        
        except:
            return toolkit.abort(500, 'Download failed!') 