var onclickColor = '#96f9ff'
var dbclickColor = '#a1fcb2'
var mouseoverColor = 'yellow'

$(document).ready(function(){

    let checkboxes = $('.hidden-checkbox');
    for (let i=0; i < checkboxes.length; i++){
        if ($(checkboxes[i]).prop('checked') === true){
            $(checkboxes[i]).prop('checked', false);
        }
    }

    /**
     * Mouse over a column in a data table
     */
     $('body').on('mouseover', '.dcom-table-cell', function() {
        let id = $(this).attr('name');
        let checkbox = $('#' + id);
        if ($(checkbox).prop('checked') === false){
            $('.dcom-column-' + id).css('background-color', mouseoverColor);        
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
     * Click on a column in a data table. It click on the column checkbox.
     * The first click is for the normal selection and the second click is for the shared column(s) selection (x-Axis)
     */
     $('body').on('click', '.dcom-table-cell', function() {        
        let id = $(this).attr('name');
        let checkbox = $('#' + id);
        let dbClickChecker = $('#' + id + '-dbclick').val(); // we use this to check wether the click is second click or first
        let nextSiblingNme = $('#' + id + '-dbclick').next().attr('annotatedCheckerInput');                
        if(dbClickChecker === '0'){
            // not clicked yet
            $(checkbox).prop('checked', true);
            $('#' + id + '-dbclick').val('1');
            $('.no_col_selcted_div').hide();
            $('.dcom-column-' + id).css('background-color', onclickColor);
        }
        else if (dbClickChecker === '1' && nextSiblingNme !== 'axis-is-annotated'){
            // already clicked once. This is the double click
            $('#' + id + '-dbclick').val('2');
            $('.no_col_selcted_div').hide();
            $('.dcom-column-' + id).css('background-color', dbclickColor);
        }             
        else if(dbClickChecker === '2' && nextSiblingNme !== 'axis-is-annotated'){
            // double clicked already. now deselect.
            $(checkbox).prop('checked', false);
            $('#' + id + '-dbclick').val('0');
            $('.no_col_selcted_div').hide();
            $('.dcom-column-' + id).css('background-color', '');
        }
        // else if (nextSiblingNme === 'axis-is-annotated'){            
        //     // annoated as y/x-axis already
        //     $('#' + id + '-dbclick').val('1');
        //     $('.no_col_selcted_div').hide();
        //     $('.dcom-column-' + id).css('background-color', onclickColor);
        //     $('#' + id + '-dbclick').next().remove()
        // } 

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

    /**
     * Close a table. 
     */
     $('body').on('click', '.close_table_btn', function() {
        let table = $(this).parent().parent().parent();
        $(table).remove(); 
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
                if($('#' + id).prop('checked') === true && $('#' + id + "-dbclick").val() === '1'){
                    $('.dcom-column-' + id).css('background-color', onclickColor); 
                }
                else if($('#' + id).prop('checked') === true && $('#' + id + "-dbclick").val() === '2'){
                    $('.dcom-column-' + id).css('background-color', dbclickColor); 
                }
                else{
                    
                }
            }
        }
    }
    req.open("POST", dest_url);
    req.send(formdata);
}