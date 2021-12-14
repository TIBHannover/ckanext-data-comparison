$(document).ready(function(){


    /**
     * Click on process data button
     */
    $('#process_btn').click(function(){
        if(check_column_selected()){
            $('.no_col_selcted_div').hide();
            $('#selection-section-div').fadeOut();
            $('#analysis-result-area').fadeIn();
            getPlotData('line');
        }
        else{
            $('.no_col_selcted_div').show();
        }        
    });

});


/**
 * get selected columsn to visulaize and call draw function
 */
 function getPlotData(plotType){
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
            let xAxis = [];
            let yAxisData = []
            let legends = []; 
            keys.forEach( function(key) {
                let table = data[key];
                if(key === 'F_2'){
                    yAxisData.push(table);  
                    legends.push(key);  
                }
                else{
                    xAxis = table;
                }

            })
            draw(plotType, xAxis, yAxisData, legends);
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


/**
 * Draw the result plot
 */
 function draw(plotType, xAxis, yAxisData, legends){
    var linePlot = null;
    let plotArea = document.getElementById('resultPlot');
    let backgroundColrs = ['red', 'green'];
    let borderColrs = ['red', 'green'];
    let chartObject = {};
    chartObject['type'] = plotType;
    chartObject['options'] = {scales: {y: {beginAtZero: true}}, responsive:true}
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

    linePlot = new Chart(plotArea, chartObject);
    
}