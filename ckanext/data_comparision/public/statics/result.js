$(document).ready(function(){
    $('#download_btn').click(function(){
        downloadData();
    });
});



/**
 * send download csv file request
 */
 function downloadData(){
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
    let dest_url = $('#download_url').val();
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == XMLHttpRequest.DONE && req.status === 200) {       
            let blob = new Blob([req.response], {type: 'text/csv'});
            let a = document.createElement("a");
            a.style = "display: none";
            document.body.appendChild(a);
            let url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = 'result.csv';
            a.click();
            window.URL.revokeObjectURL(url);                     
        }
    }
    req.open("POST", dest_url);
    req.send(formdata);


}