# encoding: utf-8

from flask import render_template, request, make_response
import ckan.plugins.toolkit as toolkit
from ckanext.data_comparision.libs.base_lib import Helper
import json
import csv, clevercsv
from io import StringIO
import pandas as pd
from ckanext.data_comparision.libs.commons import Commons
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
    def get_selected_columns():
        '''
            The function for fetching the selected data columns from resources in ckan.

            Method:
                - POST

            Returns:
                - {'x': x_axis, 'y': y_axis, 'xtick': x_axis_name} where:

                    'x': x axis values sorted
                    'y': all y axis values in format --> "column_name": [values]
                    'xtick': x axis label       
        '''

        columns_data = request.form.getlist('columns[]') 
        x_axis_raw_data = []
        y_axis_raw_data = {}
        resource_x_y_axis_map = {}
        x_axis_name = ''
        existed_y_labels = []
        existed_y_labels_counter = {}
        for value in columns_data:
            if '@_@' in value:
                resource_id_raw = value.split('@_@')[0]
                col_name = value.split('@_@')[1]
                dbClickedValue = value.split('@_@')[2]
                resource_id, sheet = Commons.process_resource_id(resource_id_raw)
                Commons.check_access_view_resource(resource_id)
                col_data = Helper.get_one_column(resource_id, sheet, col_name)
                if dbClickedValue == '2':
                    # x axis data. need to merge together
                    if resource_id not in resource_x_y_axis_map.keys():
                        resource_x_y_axis_map[resource_id] = {}
                    resource_x_y_axis_map[resource_id]['x'] = Commons.cast_string_to_num(col_data)
                    x_axis_raw_data.extend(Commons.cast_string_to_num(col_data))
                    if x_axis_name == '':
                        # assign x tick
                        x_axis_name = col_name

                elif dbClickedValue == '1':
                    # y axis data.
                    if col_name in existed_y_labels:
                        if col_name in existed_y_labels_counter.keys():
                            existed_y_labels_counter[col_name] += 1
                        else:
                            existed_y_labels_counter[col_name] = 1
                            col_name = col_name + '(' + str(existed_y_labels_counter[col_name] + 1) + ')'
                        existed_y_labels.append(col_name)
                    else:
                        existed_y_labels.append(col_name)

                    if resource_id not in resource_x_y_axis_map.keys():
                        resource_x_y_axis_map[resource_id] = {}
                        resource_x_y_axis_map[resource_id]['y'] = []
                        resource_x_y_axis_map[resource_id]['y'].append([col_name, Commons.cast_string_to_num(col_data)]) 
                    elif 'y' not in resource_x_y_axis_map[resource_id].keys():
                        resource_x_y_axis_map[resource_id]['y'] = []
                        resource_x_y_axis_map[resource_id]['y'].append([col_name, Commons.cast_string_to_num(col_data)]) 
                    else:
                        resource_x_y_axis_map[resource_id]['y'].append([col_name, Commons.cast_string_to_num(col_data)]) 
                
            
        
        # sort the x axis data to merge all selected x axises (double clicked). remove duplicates
        x_axis = sorted(list(set(x_axis_raw_data)))

        y_axis = {}
        replace_value = None
        for x_value in x_axis:
            for resource_id, resource_data in resource_x_y_axis_map.items():
                if x_value not in resource_data['x']:
                    # if x value does not exist for the y in this data resource (put None)
                    for y_vars in resource_data['y']:                        
                        if y_vars[0] in y_axis.keys():
                            # y_vars[0] is the column name
                            y_axis[y_vars[0]].append(replace_value)
                        else:
                            y_axis[y_vars[0]] = [replace_value]
                else:
                    x_index = resource_data['x'].index(x_value)
                    for y_vars in resource_data['y']:                                  
                        if y_vars[0] in y_axis.keys():
                            y_axis[y_vars[0]].append(y_vars[1][x_index])
                        else:
                            y_axis[y_vars[0]] = [y_vars[1][x_index]]
                
        
        plot_data = {'x': x_axis, 'y': y_axis, 'xtick': x_axis_name}        
            
        return json.dumps(plot_data)
    


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
            columns = TemplateHelper.get_columns(res_id)
            if isinstance(columns, list):
                # resource is a CSV 
                imported_tables[res_id] = Helper.get_resource_table(res_id, 'None', 1, True)
            else:
                # resource is a XLSX
                for sheet in columns.keys():
                    Id = res_id + '---' + sheet
                    imported_tables[Id] = Helper.get_resource_table(res_id, sheet, 1, True)


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
            csv_data_dict, columns_references = Helper.gather_data_from_columns(columns_data)
            csv_data = Helper.prepare_data_for_download(csv_data_dict, columns_references)
            string_io_object = StringIO()
            csv_writer_object = csv.writer(string_io_object)
            csv_writer_object.writerows(csv_data)
            csv_file = make_response(string_io_object.getvalue())
            csv_file.headers["Content-Disposition"] = "attachment; filename=export.csv"
            csv_file.headers["Content-type"] = "text/csv"
            return csv_file
        
        except:
            return toolkit.abort(500, 'Download failed!') 



    @staticmethod
    def get_one_resource_plot_data(resource_id):
        '''
            Return the plot data for one data resource. used for plotting preview for a data.
        '''

        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':resource_id}
        try:
            toolkit.check_access('resource_show', context, data_dict)

        except toolkit.NotAuthorized:
            return []
        
        RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        resource = toolkit.get_action('resource_show')({}, {'id': resource_id})
        
        if TemplateHelper.is_csv(resource):
            # resource is csv
            
            df = clevercsv.read_dataframe(file_path)
            if not Commons.is_possible_to_automate(df):
                return "false"
            
            df = Commons.csv_to_dataframe(resource_id)
            x = []
            y = []
            x_tick = ""
            y_tick = ""
            for col in df.columns:
                if TemplateHelper.get_column_anotation(resource_id, col) == 'x':
                    x = list(df[col].values)
                    x_tick = col
                elif TemplateHelper.get_column_anotation(resource_id, col) == 'y':
                    y = list(df[col].values)
                    y_tick = col
            
            return json.dumps({'x': x, 'y': y, 'x_tick': x_tick, 'y_tick': y_tick})
        
        elif  TemplateHelper.is_xlsx(resource):
            # resource is xlsx
            plot_data = {}
            data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)   
            for sheet, data_f in data_sheets.items():
                x = []
                y = []
                x_tick = ""
                y_tick = ""
                temp_df = data_f.dropna(how='all').dropna(how='all', axis=1).fillna(0)
                if len(temp_df) == 0:
                    continue
                if 0 in list(temp_df.columns):
                    actual_headers = temp_df.iloc[0]
                    temp_df = temp_df[1:]
                    temp_df.columns = actual_headers
                
                if not Commons.is_possible_to_automate(temp_df):                
                    continue
                else:
                    temp_df = Commons.remove_extra_columns(temp_df)
                    headers = temp_df.iloc[0]
                    final_data_df  = pd.DataFrame(temp_df.values[1:], columns=headers)
                    for col in final_data_df.columns:
                        if TemplateHelper.get_column_anotation(resource_id, col, sheet) == 'x':
                            x = list(final_data_df[col].values)
                            x_tick = col
                        elif TemplateHelper.get_column_anotation(resource_id, col, sheet) == 'y':
                            y = list(final_data_df[col].values)
                            y_tick = col
                    
                    plot_data[sheet] = {'x': x, 'y': y, 'x_tick': x_tick, 'y_tick': y_tick}
            
            if len(plot_data.keys()) == 0:
                return "false"

            return json.dumps(plot_data)
        
        else:
            return "false"






