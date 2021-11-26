import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.data_comparision.controllers.base import BaseController


class DataComparisionPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public/statics', 'ckanext-datas-comparision')


    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)        
       
        blueprint.add_url_rule(
            u'/data_comparision/base_view',
            u'base_view',
            BaseController.base_view,
            methods=['GET']
            )
        

        return blueprint