# encoding: utf-8


class Builder():

    '''
        Build a table in html format to add to the page
    '''
    def build_data_table(resource_id, columns, resource_data, max_page, load_first_time):
        root_div = '<div class="table-div">'
        root_div_end = '</div>'
        table_start = '<table class="data-comp-table"  id="data-table-' + str(resource_id) + '">'
        table_end = '</table>'
        pagination_section = Builder.build_pagination(resource_id, max_page)
        header_section = Builder.build_table_header(resource_id, columns)
        body_section = '<tbody>'
        for row in resource_data:
            body_section += Builder.build_table_row(row, resource_id)
        
        body_section += '</tbody>'
        if load_first_time:
            table = root_div + pagination_section + table_start + header_section + body_section + table_end + root_div_end
        else:
            table = root_div  + table_start + header_section + body_section + table_end + root_div_end

        return table
    


    def build_table_header(resource_id, columns):
        table_header = ''
        header_row = '<thead><tr class="dcom-table-header-row">'
        header_row_end = '</tr><thead>'
        Id = 1
        inner_content = ''
        for col in columns:
            cell = Builder.build_header_cell(Id, col, resource_id)
            checkbox = Builder.build_checkbox_input(Id, col, resource_id)
            inner_content += (cell + checkbox) 
            Id += 1
        
        table_header = header_row + inner_content + header_row_end
        return table_header



    def build_table_row(data_row, resource_id):
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



    def build_header_cell(Id, value, resource_id):
        cell = '<th class="dcom-table-cell dcom-table-header-cell '
        cell += ('dcom-column-' + str(resource_id) + '-' + str(Id) + '" ')
        cell += ('name="' +  str(resource_id) + '-' + str(Id) + '"> ')
        cell += str(value)
        cell + '</th>'
        return cell
    

    def build_body_cell(Id, value, resource_id):
        cell = '<td class="dcom-table-cell dcom-table-body-cell '
        cell += ('dcom-column-' + str(resource_id) + '-' + str(Id) + '" ')
        cell += ('name="' +  str(resource_id) + '-' + str(Id) + '"> ')
        cell += str(value)
        cell += '</td>'
        return cell

 

    def build_checkbox_input(Id, column, resource_id):
        checkbox = '<input  type="checkbox" name="chosen_columns" class="hidden-checkbox" '
        checkbox += ('value="' + str(resource_id) + '-' + str(column) + '" ')
        checkbox += ('id="' +  str(resource_id) + '-' + str(Id) + '" > ')
        return checkbox
    

    def build_pagination(resource_id, max_page):
        pagination_section = '<div class="row pagination-area">'
        pagination_section += ('<button type="button" class="btn prev-btn" id="page-prev-' + str(resource_id) + '" > ')
        pagination_section += '<i class="fa fa fa-step-backward"></i></button>'
        pagination_section += ('<input type="text" class="page-number" id="page-number-' + str(resource_id) + '" value="1">' )
        pagination_section += ('<input type="hidden" id="page-number-max-' + str(resource_id) + '" value="' + str(max_page) + '">')
        pagination_section += ('<button type="button" class="btn next-btn" id="page-next-' + str(resource_id) + '"><i class="fa fa fa-step-forward"></i></button>')
        pagination_section += '</div>'        
        return pagination_section