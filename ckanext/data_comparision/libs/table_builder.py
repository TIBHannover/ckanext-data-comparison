# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckanext.data_comparision.libs.template_helper import TemplateHelper


Tokenizer = '---'

class Builder():
    '''
        The class for creating an html table dynamically for a data resource in ckan.
    '''

    @staticmethod
    def build_data_table(resource_id, sheet, columns, resource_data, max_page, load_first_time):
        '''
            Build a table in html format to add to the page.

            Args:
                - resource_id: the id of the target data resource in ckan
                - sheet: the data sheet in case of xlsx
                - columns: the columns names of an data resource (csv, xlsx)
                - resource_data: the table data inside a data resource 
                - max_page: maximum number of table pages, used for pagination
                - load_first_time: is the table loading first time or not (pagination page changes)
            
            Returns:
                - The html table 
        '''

        
        if load_first_time:
            root_div = '<div class="element-container-box table-div">'
            root_div_end = '</div>'
            table_start = '<table class="data-comp-table"  id="data-table-' + str(resource_id) + Tokenizer + sheet + '">'
            table_end = '</table>'
            pagination_section = Builder.build_pagination(resource_id, max_page, sheet)
            header_section = Builder.build_table_header(resource_id, columns, sheet)
            body_section = Builder.build_table_body(resource_id, resource_data, sheet)
            table_title = Builder.build_table_title(resource_id, sheet)
            delete_btn = Builder.build_close_btn()
            table = root_div + delete_btn + table_title  + pagination_section + table_start + header_section + body_section + table_end + root_div_end
        else:
            table = Builder.build_table_body(resource_id, resource_data, sheet)

        return table
    

    @staticmethod
    def build_table_header(resource_id, columns, sheet):
        '''
            Create the table header <thead>.

            Args:
                - resource_id: the id of the target data resource in ckan
                - columns: the columns names of an data resource (csv, xlsx)
            
            Returns:
                - the table header section <thead>
        '''

        table_header = ''
        header_row = '<tr class="dcom-table-header-row">'
        header_row_end = '</tr>'
        Id = 1
        inner_content = ''
        for col in columns:
            cell = Builder.build_header_cell(Id, col, resource_id, sheet)            
            inner_content += cell 
            Id += 1
        
        table_header = header_row + inner_content + header_row_end
        return table_header
    

    @staticmethod
    def build_table_body(resource_id, resource_data_rows, sheet):
        '''
            Create the table body.

            Args:
                - resource_id: the id of the target data resource in ckan
                - resource_data_rows: the data resource rows (list of lists)
            
            Returns:
                - the table body section <tbody>
        
        '''

        body_section = '<tbody id="data-table-body-' + str(resource_id) + Tokenizer + sheet + '">'
        for row in resource_data_rows:
            body_section += Builder.build_table_row(row, resource_id, sheet)
        
        body_section += '</tbody>'

        return body_section



    @staticmethod
    def build_table_row(data_row, resource_id, sheet):
        '''
            Create one table row.

            Args:
                - data_row: The row from the resource data table
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - One table row <tr>
        '''

        table_row = ''
        body_row = ' <tr class="dcom-table-content-row">'
        body_row_end = '</tr>'
        Id = 1
        inner_content = ''
        for value in data_row:
            cell = Builder.build_body_cell(Id, value, resource_id, sheet)
            Id += 1
            inner_content += cell
        
        table_row = body_row + inner_content + body_row_end
        return table_row


    @staticmethod
    def build_header_cell(Id, value, resource_id, sheet):
        '''
            Create one table header cell.

            Args:
                - Id: The column Id 
                - value: The value for this cell
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - One table header cell <th>
        '''

        cell = '<th class="dcom-table-cell dcom-table-header-cell '
        cell += ('dcom-column-' + str(resource_id) + Tokenizer + sheet + '-' + str(Id) + '" ')
        cell += ('name="' +  str(resource_id) + Tokenizer + sheet + '-' + str(Id) + '"> ')
        cell += str(value)
        default_checked = False
        default_value = '0'
        annotatorCheckerInput = ''
        if TemplateHelper.get_column_anotation(resource_id, value, sheet) == 'x':
            cell += '<span class="column_x_axis_tag">X-axis</span>'
            # default_checked = True
            default_value = '0'
            # annotatorCheckerInput = '<input type="hidden" annotatedCheckerInput="axis-is-annotated">'          
        elif TemplateHelper.get_column_anotation(resource_id, value, sheet) == 'y':
            cell += '<span class="column_y_axis_tag">Y-axis</span>'
            # default_checked = True
            default_value = '0'
            # annotatorCheckerInput = '<input type="hidden" annotatedCheckerInput="axis-is-annotated">'
        
        checkbox = Builder.build_checkbox_input(Id, value, resource_id, sheet, default_checked)
        dbclick_input = Builder.build_dbclick_input(Id, value, resource_id, sheet, default_value)        
        cell += (checkbox + dbclick_input + annotatorCheckerInput + '</th>')
        return cell
    

    @staticmethod
    def build_body_cell(Id, value, resource_id, sheet):
        '''
            Create one table body cell.

            Args:
                - Id: The column Id 
                - value: The value for this cell
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - One table body cell <td>
        '''

        cell = '<td class="dcom-table-cell dcom-table-body-cell '
        cell += ('dcom-column-' + str(resource_id) + Tokenizer + sheet + '-' + str(Id) + '" ')
        cell += ('name="' +  str(resource_id) + Tokenizer + sheet + '-' + str(Id) + '"> ')
        cell += str(value)
        cell += '</td>'
        return cell

 
    @staticmethod
    def build_checkbox_input(Id, column, resource_id, sheet, default_checked=False):
        '''
            Create a checkbox input for a table column.

            Args:
                - Id: The column Id 
                - value: The value for this cell
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - a checkbox html input. 
        '''

        checkbox = '<input  type="checkbox" name="chosen_columns" class="hidden-checkbox" '
        checkbox += ('value="' + str(resource_id) + Tokenizer + sheet + '@_@' + str(column) + '" ')
        if(default_checked):
            checkbox += ('checked="checked" ')
        checkbox += ('id="' +  str(resource_id) + Tokenizer + sheet + '-' + str(Id) + '" > ')        
        return checkbox
    

    @staticmethod
    def build_pagination(resource_id, max_page, sheet):
        '''
            Create the pagination section for a table.

            Args:            
                - resource_id: the id of the target data resource in ckan
                - max_page: maximum number of table pages, used for pagination
            
            Returns:
                - The table pagination section. Including the previous button, input for pagination number, and 
                the next page button.  
        '''

        pagination_section = '<div class="row pagination-area">'
        pagination_section += '<div class="col-sm-12">'
        pagination_section += ('<button type="button" class="btn prev-btn" id="page-prev-' + str(resource_id) + Tokenizer + sheet + '" > ')
        pagination_section += '<i class="fa fa fa-step-backward"></i></button>'
        pagination_section += ('<input type="text" class="page-number" id="page-number-' + str(resource_id) + Tokenizer + sheet + '" value="1" readonly>' )
        pagination_section += ('<input type="hidden" id="page-number-max-' + str(resource_id) + Tokenizer + sheet + '" value="' + str(max_page) + '">')
        pagination_section += ('<button type="button" class="btn next-btn" id="page-next-' + str(resource_id) + Tokenizer + sheet + '"><i class="fa fa fa-step-forward"></i></button>')
        pagination_section += '</div></div>'        
        return pagination_section
    

    @staticmethod
    def build_close_btn():
        '''
            Create the close button.
            
            Returns:
                - a column contains the close button.  
        '''
        close_btn = '<div class="row close-table-column"><div class="col-sm-12">'
        close_btn += '<button class="btn btn-sm btn-danger close_table_btn"><i class="fa fa-close"></i></button>'       
        close_btn += '</div></div>'
        return close_btn


    @staticmethod
    def build_table_title(resource_id, sheet):
        '''
            Create a table title with the resource name and url. 

            Args:
                - resource_id: the id of the target data resource in ckan
            
            Returns:
                - a div contains table title
        '''

        resource = toolkit.get_action('resource_show')({}, {'id': resource_id})
        package = toolkit.get_action('package_show')({}, {'name_or_id': resource['package_id']})
        res_url = h.url_for('dataset_resource.read', resource_id=resource['id'], package_type=package['type'], id=package['id'], _external=True)
        title = '<div class="row text-center resource-name-div"><h3>'
        title += ('<a href="' + res_url + '" target="_blank">')
        if sheet != 'None':
            title += ('<b>' + resource['name'] + '(' + sheet + ')' + '</b>')
        else:
            title += ('<b>' + resource['name'] + '</b>')
        title += ('</a></h3></div>')

        return title
    

    @staticmethod
    def build_dbclick_input(Id, column, resource_id, sheet, default_value='0'):
        '''
            Create a hidden input for checking the double click on a column.

            Args:
                - Id: The column Id 
                - value: The value for this cell
                - resource_id: the id of the target data resource in ckan
                - sheet: the sheet name for xlsx
            
            Returns:
                - a hidden html input. 
        '''

        dbcick_input = '<input  type="hidden" name="hidden_dbclick_checker" value="{}"'.format(default_value)
        dbcick_input += ('id="' +  str(resource_id) + Tokenizer + sheet + '-' + str(Id) + '-dbclick" > ')
        return dbcick_input