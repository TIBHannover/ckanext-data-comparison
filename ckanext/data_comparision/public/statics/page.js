$(document).ready(function(){

    /**
     * Click on process data button
     */
    $('#process_btn').click(function(){
        if(check_column_selected()){
            $('.no_col_selcted_div').hide();
            $('#selection-section-div').fadeOut();
            $('#analysis-result-area').fadeIn();
            getPlotData();
        }
        else{
            $('.no_col_selcted_div').show();
        }        
    });

});


/**
 * get selected columsn to visulaize
 */
 function getPlotData(){
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
    let dest_url = $('#get_selected_url').val();
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == XMLHttpRequest.DONE && req.status === 200) {       
            data = JSON.parse(req.responseText);
            let keys = Object.keys(data); 
            keys.forEach( function(key) {
                let table = data[key]
                console.info(key);
                console.info(table);
            })
        }
    }
    req.open("POST", dest_url);
    req.send(formdata);
}


/**
 * Check atleast a column is selected
 */

function check_column_selected(){
    let checkboxes = $('.hidden-checkbox');
    for (let i=0; i < checkboxes.length; i++){
        if ($(checkboxes[i]).prop('checked') === true){
            return true;
        }
    }
    return false;
}
