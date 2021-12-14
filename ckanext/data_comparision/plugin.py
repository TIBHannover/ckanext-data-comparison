import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.data_comparision.controllers.base import BaseController
from ckanext.data_comparision.libs.template_helper import TemplateHelper


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
            u'/data_comparision/get_selected_columns',
            u'get_selected_columns',
            BaseController.get_selected_columns,
            methods=['POST']
            )
        
        blueprint.add_url_rule(
            u'/data_comparision/import_data',
            u'import_data',
            BaseController.import_data,
            methods=['POST']
            )
        
        blueprint.add_url_rule(
            u'/data_comparision/load_new_page',
            u'load_new_page',
            BaseController.load_new_page,
            methods=['POST']
            )
        
        blueprint.add_url_rule(
            u'/data_comparision/download_file',
            u'download_file',
            BaseController.download_file,
            methods=['POST']
            )

        return blueprint
    
    #ITemplateHelpers

    def get_helpers(self):
        return {'is_csv': TemplateHelper.is_csv,
            'is_xlsx': TemplateHelper.is_xlsx,
            'get_data': TemplateHelper.get_data,
            'get_columns': TemplateHelper.get_columns,
            'get_max_table_page_count': TemplateHelper.get_max_table_page_count
        }