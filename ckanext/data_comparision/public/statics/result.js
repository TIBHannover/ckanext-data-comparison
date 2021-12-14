$(document).ready(function(){

    
    const ctx = document.getElementById('myChart');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });




    /**
     * Click on the download button.
     */
    $('#download_btn').click(function(){
        downloadData();
    });

    /**
     * Click on back to selection that shows the selection section.
     */
    $('#back_to_selection_btn').click(function(){
        $('#analysis-result-area').fadeOut(1000);
        $('#selection-section-div').fadeIn(1000);
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


