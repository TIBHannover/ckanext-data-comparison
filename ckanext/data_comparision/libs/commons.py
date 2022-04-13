# encoding: utf-8

from os import stat
import ckan.plugins.toolkit as toolkit
import clevercsv
import pandas as pd



RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'
STANDARD_HEADERS = ['X-Kategorie', 'Y-Kategorie', 'Datentyp', 'Werkstoff-1', 'Werkstoff-2', 'Atmosphaere', 'Vorbehandlung']


class Commons():
    '''
        The class contains the common functions used by other libraries.
    '''


    @staticmethod
    def check_access_view_package(package_id):
        '''
            Check a user can view a dataset in ckan or not.

            Args:
                - package_id: the datset id in ckan
            
            Returns:
                - Boolean
        '''
        
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':package_id}
        try:
            toolkit.check_access('package_show', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return False
    


    @staticmethod
    def check_access_view_resource(resource_id):
        '''
            Check a user can view a data resource in ckan or not.

            Args:
                - resource_id: the data resource id in ckan
            
            Returns:
                - Boolean
        '''
        
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':resource_id}
        try:
            toolkit.check_access('resource_show', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return toolkit.abort(403, "You do not have the required authorization.")



    @staticmethod   
    def get_resource_type(resource_id):
        '''
            Get a data resource type.

            Args:
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - the resource type as String
        '''

        resource = toolkit.get_action('resource_show')({}, {'id': resource_id})
        if resource['format'] in ['CSV'] or '.csv' in  resource['name']: 
            return 'csv'
        if resource['format'] in ['XLSX'] or '.xlsx' in  resource['name']: 
            return 'xlsx'

        return None
    


    @staticmethod
    def csv_to_dataframe(resource_id):
        '''
            Read a csv file as pandas dataframe.

            Args:
                - resource_id: the data resource id in ckan
            
            Returns:
                - a python dataframe
        '''

        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        df = clevercsv.read_dataframe(file_path)
        df = df.fillna(0)

        return df


    @staticmethod
    def xlsx_to_dataframe(resource_id):
        '''
            Read a xlsx file as pandas dataframe.

            Args:
                - resource_id: the data resource id in ckan
            
            Returns:
                - a dictionary where key is the sheet name and value is a dataframe
        '''

        result_df = {}
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)        
        for sheet, data_f in data_sheets.items():
            temp_df = data_f.dropna(how='all').dropna(how='all', axis=1)
            if len(temp_df) == 0:
                continue
            if 0 in list(temp_df.columns):
                actual_headers = temp_df.iloc[0]
                temp_df = temp_df[1:]
                temp_df.columns = actual_headers
            
            if not Commons.is_possible_to_automate(temp_df):                
                headers = temp_df.iloc[0]
                final_data_df  = pd.DataFrame(temp_df.values[1:], columns=headers)
                result_df[sheet] = final_data_df
            else:
                headers = temp_df.iloc[1]
                final_data_df  = pd.DataFrame(temp_df.values[2:], columns=headers)
                result_df[sheet] = final_data_df

        return result_df
    


    @staticmethod
    def process_resource_id(raw_id):
        '''
            Process the input resource Id to get the sheet name and resource Id.

            Args:
                - raw_id: the raw resource id input
            
            Returns:
                - resource id and sheet name
        '''

        resource_id = raw_id.split('---')[0]
        sheet = raw_id.split('---')[1]
        return [resource_id, sheet]
    



    @staticmethod
    def is_possible_to_automate(resource_df):
        '''
            Is the data resource annotated by the researcher. Then, the actual headers are the second row. 

            Args:
                - resource_df: the target data resource pandas dataframe.

        '''
        
        df_columns = resource_df.columns    
        if len(df_columns) != len(STANDARD_HEADERS):
            return False
        for header in df_columns:            
            if header.strip() not in STANDARD_HEADERS:
                return False
        return True
    


    @staticmethod
    def cast_string_to_num(List):
        '''
            Cast the values in a list from string to float for the visualization.

            Args:
                - List: the input list of string.

            Returns:
                - List of float numbers
        
        '''
        
        result = []
        for val in List:
            num = None
            if isinstance(val, str) and ',' in val:
                num = val.replace(',', '.')
            else:
                num = val
            
            try:
                num = float(num)
                result.append(num)
            except:
                result.append(0)
        
        return result


