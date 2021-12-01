import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.data_comparision.controllers.base import BaseController
from ckanext.data_comparision.libs.base_lib import Helper


class DataComparisionPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public/statics', 'ckanext-data-comparision')


    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)        
       
        blueprint.add_url_rule(
            u'/data_comparision/base_view/<package_name>/<resId>',
            u'base_view',
            BaseController.base_view,
            methods=['GET']
            )
        
        blueprint.add_url_rule(
            u'/data_comparision/process_columns',
            u'process_columns',
            BaseController.process_columns,
            methods=['POST']
            )

        return blueprint
    
    #ITemplateHelpers

    def get_helpers(self):
        return {'is_csv': Helper.is_csv,
            'is_xlsx': Helper.is_xlsx,
            'get_data': Helper.get_data,
            'get_columns': Helper.get_columns
        }