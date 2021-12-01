# encoding: utf-8

from flask import render_template, request
import ckan.plugins.toolkit as toolkit
from ckanext.data_comparision.libs.base_lib import Helper
import json

class BaseController():

    def base_view(package_name, resId):
        datasets = Helper.get_all_datasets()
        package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
        resource = toolkit.get_action('resource_show')({}, {'id': resId})


        return render_template('base_index.html', 
            datasets=datasets,
            pkg_dict=package,
            package=package,
            resource=resource
        
        )
    
    def process_columns():
        columns_data = request.form.getlist('columns[]')       
        result_columns = {}        
        for value in columns_data:
            temp = value.split('@_@')
            resource_id = temp[0]
            col_name = temp[1]
            col_data = Helper.get_one_column(resource_id, col_name, 'csv')
            if col_data:
                result_columns[col_name] = col_data
            

        return json.dumps(result_columns)