# encoding: utf-8

from flask import render_template
import ckan.plugins.toolkit as toolkit

class BaseController():

    def base_view():


        return render_template('base_index.html')