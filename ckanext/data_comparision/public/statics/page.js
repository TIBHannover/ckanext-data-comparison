$(document).ready(function(){
    var selectedData = null;

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
            createSelectOptions($('#xAxisColumn'), keys);
            selectedData = data;
            let canvas = document.getElementById('resultPlot');
            let context = canvas.getContext("2d");
            context.fillStyle = "blue";
            context.font = "bold 16px Arial";
            context.fillText("Please select the X axis for the plot.", (canvas.width / 2) - (canvas.width / 4) , (canvas.height / 2) + 8);
            $(canvas).css('background', '#edf783');
            // let xAxis = [];
            // let yAxisData = [];
            // let legends = []; 
            // keys.forEach( function(key) {
            //     let table = data[key];
            //     if(key === 'F_2'){
            //         yAxisData.push(table);  
            //         legends.push(key);  
            //     }
            //     else{
            //         xAxis = table;
            //     }

            // })
            // draw(plotType, [], [], []);
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
    chartObject['options'] = {scales: {y: {beginAtZero: true, max: getMax(yAxisData)}}, responsive:true}
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

/**
 * get the max value from y axis data
 */
function getMax(yAxisData){
    allMax = [];
    for (let i=0; i < yAxisData.length; i++){
        allMax.push(Math.max.apply(Math, yAxisData[i])); 
    }
    return Math.max.apply(Math, allMax);
}

/**
 * Create select2 options
 */
function createSelectOptions(selectId, data){
    for (let i=0; i < data.length; i++){
        let option = '<option value="' + i + '">' + data[i] + '</option>';
        $(selectId).append(option);
    }
}