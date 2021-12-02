# encoding: utf-8


class Builder():

    '''
        Build a table in html format to add to the page
    '''
    def build_data_table(resource_id, columns, resource_data):
        root_div = '<div class="table-div">'
        root_div_end = '</div>'
        table_start = '<table class="data-comp-table">'
        table_end = '</table>'
        header_section = Builder.build_table_header(resource_id, columns)
        body_section = ''
        for row in resource_data:
            body_section += Builder.build_table_row(row)
        
        table = root_div + table_start + header_section + body_section + table_end + root_div_end
        return table
    


    def build_table_header(resource_id, columns):
        table_header = ''
        header_row = '<tr class="dcom-table-header-row">'
        header_row_end = '</tr>'
        Id = 1
        inner_content = ''
        for col in columns:
            cell = Builder.build_header_cell(Id, col)
            checkbox = Builder.build_checkbox_input(Id, col, resource_id)
            inner_content += (cell + checkbox) 
            Id += 1
        
        table_header = header_row + inner_content + header_row_end
        return table_header



    def build_table_row(data_row):
        table_row = ''
        body_row = ' <tr class="dcom-table-content-row">'
        body_row_end = '</tr>'
        Id = 1
        inner_content = ''
        for value in data_row:
            cell = Builder.build_body_cell(Id, value)
            Id += 1
            inner_content += cell
        
        table_row = body_row + inner_content + body_row_end
        return table_row



    def build_header_cell(Id, value):
        cell = '<th class="dcom-table-cell dcom-table-header-cell '
        cell += ('dcom-column-' + str(Id) + '" ')
        cell += ('name="dcom-column-name-' + str(Id) + '"> ')
        cell += str(value)
        cell + '</th>'
        return cell
    

    def build_body_cell(Id, value):
        cell = '<td class="dcom-table-cell '
        cell += ('dcom-column-' + str(Id) + '" ')
        cell += ('name="dcom-column-name-' + str(Id) + '"> ')
        cell += str(value)
        cell += '</td>'
        return cell

 

    def build_checkbox_input(Id, column, resource_id):
        checkbox = '<input  type="checkbox" name="chosen_columns" class="hidden-checkbox" '
        checkbox += ('value="' + str(resource_id) + '@_@' + str(column) + '" ')
        checkbox += ('id="col-checkbox-' + str(Id) + '" >')
        return checkbox