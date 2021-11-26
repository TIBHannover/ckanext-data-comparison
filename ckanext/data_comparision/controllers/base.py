# encoding: utf-8

from flask import render_template
import ckan.plugins.toolkit as toolkit
from ckanext.data_comparision.libs.base_lib import Helper

class BaseController():

    def base_view():
        datasets = Helper.get_all_datasets()



        return render_template('base_index.html', 
            datasets=datasets
        
        )