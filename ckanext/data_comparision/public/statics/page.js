var selectedData = null;
var linePlot = null;
var legends = [];
var yAxisData = [];

$(document).ready(function(){
    

    /**
     * Click on process data button
     */
    $('#process_btn').click(function(){
        if(check_column_selected()){
            $('.no_col_selcted_div').hide();
            $('#selection-section-div').fadeOut();
            $('#analysis-result-area').fadeIn();
            if (linePlot){
                linePlot.destroy();
                linePlot = null;
                selectedData = null;
                linePlot = null;
                legends = [];
                yAxisData = [];
            }
            getPlotData();
        }
        else{
            $('.no_col_selcted_div').show();
        }        
    });


    /**
     * Select the plot type
     */
     $('body').on('change', '.plot-type', function() {
        // let xAxisName = $.trim($('.x-axis-col').select2('data').text);
        // if(xAxisName !== ''){
        //     let xAxis = [];
        //     let yAxisData = [];
        //     let legends = [];
        //     let keys = Object.keys(selectedData); 
        //     keys.forEach( function(key) {
        //         let dataColumn = data[key];            
        //         if(key === xAxisName){
        //             xAxis = dataColumn;
        //         }
        //         else{
        //             yAxisData.push(dataColumn);  
        //             legends.push(key);
        //         }

        //     });
        // }      

        let plotType = $.trim($(this).val());
        $('#resultPlot').css('background', '');
        if (linePlot){
            linePlot.destroy();
        }  
        draw(plotType, selectedData['x'], yAxisData, legends, selectedData['xtick']);        
    });
});


/**
 * get selected columsn to visulaize and call draw function
 */
 function getPlotData(){
    let formdata = new FormData();
    let checkboxes = $('.hidden-checkbox');
    let checked_ones = [];
    for (let i=0; i < checkboxes.length; i++){
        if ($(checkboxes[i]).prop('checked') === true){
            let id = $(checkboxes[i]).prop('id');
            let dbClickValue = $('#' + id + '-dbclick').val();
            checked_ones.push($(checkboxes[i]).val() + '@_@' + dbClickValue);
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
            // createSelectOptions($('#xAxisColumn'), keys);
            selectedData = data;
            // let canvas = document.getElementById('resultPlot');
            // let context = canvas.getContext("2d");
            // context.fillStyle = "blue";
            // context.font = "bold 16px Arial";
            // context.fillText("Please select the X axis for the plot.", (canvas.width / 2) - (canvas.width / 4) , (canvas.height / 2) + 8);
            // $(canvas).css('background', '#edf783');
            $.each(selectedData['y'], function(key,value){
                legends.push(key);
                yAxisData.push(value);
            }); 
            // console.info(selectedData);
            console.info(selectedData);
            draw('line', selectedData['x'], yAxisData, legends, selectedData['xtick']);           
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
 function draw(plotType, xAxis, yAxisData, legends, xAxisName){
    let plotArea = document.getElementById('resultPlot');
    let backgroundColrs = [];
    let borderColrs = [];
    for (let i=0; i < yAxisData.length; i++){
        let color = getRandomColor();
        backgroundColrs.push(color);
        borderColrs.push(color);
    }
    let chartObject = {};
    chartObject['type'] = plotType;
    plugins = {'title': {'display': true, 'text': 'Visualization Result'}};
    ticks_font = {family: 'Times', size: 20, style: 'normal', lineHeight: 1.2},
    y_scales = {beginAtZero: true, max: getMax(yAxisData) + 20, title: {display: true, text: legends[0], font: ticks_font}}
    x_scales = {beginAtZero: true, title: {display: true, text: xAxisName, font: ticks_font}}
    chartObject['options'] = {scales: {yAxes: y_scales, xAxes:x_scales}, responsive:true, 'plugins': plugins};
    chartObject['data'] = {};
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
    let options = $('.col_options');
    $(selectId).select2("val", "");
    if (options.length !== 0){
        for (let i=0; i < options.length; i++){
            $(options[i]).remove();
        }
    }
    for (let i=1; i <= data.length; i++){
        let option = '<option class="col_options" value="' + i + '">' + data[i - 1] + '</option>';
        $(selectId).append(option);
    }
}


/**
 * Generate a random color
 * source: https://stackoverflow.com/questions/1484506/random-color-generator
 * 
 */
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }



