$(document).ready(function(){

    /**
     * Click on process data button
     */
    $('#process_btn').click(function(){
        $('#selection-section-div').fadeOut();
        $('#analysis-result-area').fadeIn();
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
    for (let i = 0; i < checked_ones.length; i++) {
        formdata.append('columns[]', checked_ones[i]);
    }
    let dest_url = $('#process_url').val();
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == XMLHttpRequest.DONE && req.status === 200) {       
            let data=req.responseText;
            let jsonResponse = JSON.parse(data);   
            console.info(jsonResponse);                        
        }
    }
    req.open("POST", dest_url);
    req.send(formdata);
}
