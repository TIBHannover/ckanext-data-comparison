$(document).ready(function(){
    var linePlot = null;
    draw('line');

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

/**
 * Draw the result plot
 */
function draw(plotType){
    let plotArea = document.getElementById('resultPlot');
    let xAxis = [1,2,3,4,5,6,7];
    let yAxisData = [[12, 19, 3, 5, 2, 3], [16, 29, 5, 7, 12, 23]];
    let legends = ['col1', 'col2']
    let backgroundColrs = ['red', 'green'];
    let borderColrs = ['red', 'green'];
    let chartObject = {};
    chartObject['type'] = plotType;
    chartObject['options'] = {scales: {y: {beginAtZero: true}}}
    chartObject['data'] = {}
    chartObject['data']['labels'] = xAxis; 
    chartObject['data']['datasets'] = []; 
    for (let i=0; i<yAxisData.length; i++){
        let temp = {};
        temp['label'] = legends[i];
        temp['data'] = yAxisData[i];
        temp['borderWidth'] = 1;
        temp['backgroundColor'] = backgroundColrs[i];
        temp['borderColor'] = borderColrs[i];
        chartObject['data']['datasets'][i] = temp;
        
    }

    plot = new Chart(plotArea, chartObject);
    
}




