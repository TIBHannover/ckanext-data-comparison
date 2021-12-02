$(document).ready(function(){

    /**
     * Mouse over a column in a data table
     */
     $('body').on('mouseover', '.dcom-table-cell', function() {
        let id = $(this).attr('name');
        // id = id[id.length - 1];
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
        // id = id[id.length - 1];
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
        // id = id[id.length - 1];
        let checkbox = $('#' + id);
        $(checkbox).click();
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
        }        
    });


    /**
     * Click on process data button
     */
    $('#process_btn').click(function(){
        send_columns_data();
    });

});


/**
 * Post columns data to backend for processing
 */
function send_columns_data(){
    let formdata = new FormData();
    let checkboxes = $('.hidden-checkbox');
    let checked_ones = [];
    for (let i=0; i < checkboxes.length; i++){
        if ($(checkboxes[i]).prop('checked') === true){
            checked_ones.push($(checkboxes[i]).val());
        }
    }
    // formdata.set('columns', JSON.stringify(checked_ones));
    for (let i = 0; i < checked_ones.length; i++) {
        formdata.append('columns[]', checked_ones[i]);
    }
    let dest_url = $('#process_url').val();
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == XMLHttpRequest.DONE && req.status === 200) {       
            let data=req.responseText;
            let jsonResponse = JSON.parse(data);                           
        }
    }
    req.open("POST", dest_url);
    req.send(formdata);
}