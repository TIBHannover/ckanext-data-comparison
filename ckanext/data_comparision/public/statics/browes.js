$(document).ready(function(){
    $('#import-btn').click(function(){
        $('#import_loader').show();
        import_table();

    });

    /**
     * unckecked all checkbox on modal open
     */
    $('#modal-browes-btn').click(function(){
        let checkboxes = $('.resource-box');
        for (let i=0; i < checkboxes.length; i++){
            if ($(checkboxes[i]).prop('checked') === true){
                $(checkboxes[i]).click();
            }
        }
    });


    /**
     * click on the dataset name to expand/collapse
     */
    $('.dataset-box').click(function(){
        let id = $(this).attr('id');
        id = id[id.length - 1]
        if($('#dataset-list-' + id).hasClass('hidden-list')){
            $('#dataset-list-' + id).fadeIn();
            $('#dataset-list-' + id).removeClass('hidden-list');        
        }
        else{
            $('#dataset-list-' + id).fadeOut();
            $('#dataset-list-' + id).addClass('hidden-list');
        }

    });


});


/**
 * Post resources name data to backend for importing
 */
 function import_table(){
    let formdata = new FormData();
    let checkboxes = $('.resource-box');
    let checked_ones = [];
    for (let i=0; i < checkboxes.length; i++){
        if ($(checkboxes[i]).prop('checked') === true){
            checked_ones.push($(checkboxes[i]).val());
        }
    }
    for (let i = 0; i < checked_ones.length; i++) {
        formdata.append('resources[]', checked_ones[i]);
    }
    let dest_url = $('#import_url').val();
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == XMLHttpRequest.DONE && req.status === 200) {       
            data = JSON.parse(req.responseText);
            let keys = Object.keys(data); 
            keys.forEach( function(key) {
                let table = data[key]
                $('#raw_tables_area').find('.data-comparision-module-col').append(table);
                $('#import_loader').hide();
            })
        }
    }
    req.open("POST", dest_url);
    req.send(formdata);
}