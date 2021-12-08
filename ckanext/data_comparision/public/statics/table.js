$(document).ready(function(){

    /**
     * Mouse over a column in a data table
     */
     $('body').on('mouseover', '.dcom-table-cell', function() {
        let id = $(this).attr('name');
        let checkbox = $('#' + id);
        if ($(checkbox).prop('checked') === false){
            $('.dcom-column-' + id).css('background-color', 'yellow');        
        }
    });


    /**
     * Mouse out a column in a data table
     */
     $('body').on('mouseout', '.dcom-table-cell', function() {
        let id = $(this).attr('name');
        let checkbox = $('#' + id);
        if ($(checkbox).prop('checked') === false){
            $('.dcom-column-' + id).css('background-color', '');       
        }
    });
    

    /**
     * Click on a column in a data table. It click on the column checkbox
     */
     $('body').on('click', '.dcom-table-cell', function() {
        let id = $(this).attr('name');
        let checkbox = $('#' + id);
        $(checkbox).prop('checked', !$(checkbox).is(":checked"));
        if ($(checkbox).prop('checked') === true){
            $('.dcom-column-' + id).css('background-color', 'green');        
        }
        else{
            $('.dcom-column-' + id).css('background-color', '');
        }
    });

    /**
     * Click next page pagination
     */
     $('body').on('click', '.next-btn', function() {
        let id_elem = $(this).attr('id');
        let id = id_elem.split('page-next-')[1]
        let page = $('#page-number-' + id).val();
        let max_page = $('#page-number-max-' + id).val();
        if(parseInt(page) < parseInt(max_page)){
            $('#page-number-' + id).val(parseInt(page) + 1);
            get_new_page(id, parseInt(page) + 1);
        }

    });

    /**
     * Click prev page pagination
     */
     $('body').on('click', '.prev-btn', function() {
        let id_elem = $(this).attr('id');
        let id = id_elem.split('page-prev-')[1]
        let page = $('#page-number-' + id).val();
        if (parseInt(page) > 1){
            $('#page-number-' + id).val(parseInt(page) - 1);
            get_new_page(id, parseInt(page) - 1);
        }        
    });

});


/**
 * Get new page on pagination
 */
 function get_new_page(resourceId, page){
    let formdata = new FormData();
    formdata.set('page', page);
    formdata.set('resourceId', resourceId);
    let dest_url = $('#new_page_url').val();
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == XMLHttpRequest.DONE && req.status === 200) {       
            data = JSON.parse(req.responseText);
            let tableBody = $('#data-table-body-' + resourceId);
            $(tableBody).remove();
            $($('#data-table-' + resourceId)).append(data['table']);
            let headers = $('#data-table-' + resourceId).find('th');
            for(let i=1; i <= headers.length; i++){
                let id = resourceId + '-' + i
                if($('#' + id).prop('checked') === true){
                    $('.dcom-column-' + id).css('background-color', 'green'); 
                }
            }
        }
    }
    req.open("POST", dest_url);
    req.send(formdata);
}