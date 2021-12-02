$(document).ready(function(){
    $('#import-btn').click(function(){
        send_columns_data();

    });
});


/**
 * Post resources name data to backend for importing
 */
 function send_columns_data(){
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
                $('#raw_tables_area').append(table);
            })
        }
    }
    req.open("POST", dest_url);
    req.send(formdata);
}