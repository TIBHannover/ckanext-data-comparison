# encoding: utf-8

from flask import render_template
import ckan.plugins.toolkit as toolkit
from ckanext.data_comparision.libs.base_lib import Helper

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

        return '0'