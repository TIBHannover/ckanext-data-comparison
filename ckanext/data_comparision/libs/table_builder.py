# encoding: utf-8


class Builder():
    '''
        The class for creating an html table dynamically for a data resource in ckan.
    '''

    @staticmethod
    def build_data_table(resource_id, columns, resource_data, max_page, load_first_time):
        '''
            Build a table in html format to add to the page.

            Args:
                - resource_id: the id of the target data resource in ckan
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
            table_start = '<table class="data-comp-table"  id="data-table-' + str(resource_id) + '">'
            table_end = '</table>'
            pagination_section = Builder.build_pagination(resource_id, max_page)
            header_section = Builder.build_table_header(resource_id, columns)
            body_section = Builder.build_table_body(resource_id, resource_data)
            table = root_div + pagination_section + table_start + header_section + body_section + table_end + root_div_end
        else:
            table = Builder.build_table_body(resource_id, resource_data)

        return table
    

    @staticmethod
    def build_table_header(resource_id, columns):
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
            cell = Builder.build_header_cell(Id, col, resource_id)
            checkbox = Builder.build_checkbox_input(Id, col, resource_id)
            inner_content += (cell + checkbox) 
            Id += 1
        
        table_header = header_row + inner_content + header_row_end
        return table_header
    

    @staticmethod
    def build_table_body(resource_id, resource_data_rows):
        '''
            Create the table body.

            Args:
                - resource_id: the id of the target data resource in ckan
                - resource_data_rows: the data resource rows (list of lists)
            
            Returns:
                - the table body section <tbody>
        
        '''

        body_section = '<tbody id="data-table-body-' + str(resource_id) + '">'
        for row in resource_data_rows:
            body_section += Builder.build_table_row(row, resource_id)
        
        body_section += '</tbody>'

        return body_section



    @staticmethod
    def build_table_row(data_row, resource_id):
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
            cell = Builder.build_body_cell(Id, value, resource_id)
            Id += 1
            inner_content += cell
        
        table_row = body_row + inner_content + body_row_end
        return table_row


    @staticmethod
    def build_header_cell(Id, value, resource_id):
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
        cell += ('dcom-column-' + str(resource_id) + '-' + str(Id) + '" ')
        cell += ('name="' +  str(resource_id) + '-' + str(Id) + '"> ')
        cell += str(value)
        cell + '</th>'
        return cell
    

    @staticmethod
    def build_body_cell(Id, value, resource_id):
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
        cell += ('dcom-column-' + str(resource_id) + '-' + str(Id) + '" ')
        cell += ('name="' +  str(resource_id) + '-' + str(Id) + '"> ')
        cell += str(value)
        cell += '</td>'
        return cell

 
    @staticmethod
    def build_checkbox_input(Id, column, resource_id):
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
        checkbox += ('value="' + str(resource_id) + '@_@' + str(column) + '" ')
        checkbox += ('id="' +  str(resource_id) + '-' + str(Id) + '" > ')
        return checkbox
    

    @staticmethod
    def build_pagination(resource_id, max_page):
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
        pagination_section += Builder.build_close_btn()
        pagination_section += '<div class="col-sm-8">'
        pagination_section += ('<button type="button" class="btn prev-btn" id="page-prev-' + str(resource_id) + '" > ')
        pagination_section += '<i class="fa fa fa-step-backward"></i></button>'
        pagination_section += ('<input type="text" class="page-number" id="page-number-' + str(resource_id) + '" value="1" readonly>' )
        pagination_section += ('<input type="hidden" id="page-number-max-' + str(resource_id) + '" value="' + str(max_page) + '">')
        pagination_section += ('<button type="button" class="btn next-btn" id="page-next-' + str(resource_id) + '"><i class="fa fa fa-step-forward"></i></button>')
        pagination_section += '</div></div>'        
        return pagination_section
    

    @staticmethod
    def build_close_btn():
        '''
            Create the close button.
            
            Returns:
                - a column contains the close button.  
        '''

        close_btn = '<div class="col-sm-2 close-table-column"><button class="btn btn-sm btn-danger close_table_btn"><i class="fa fa-close"></i></button></div>'       
        return close_btn