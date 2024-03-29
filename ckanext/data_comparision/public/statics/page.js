var selectedData = null;
var linePlot = null;
var legends = [];
var yAxisData = [];
var backgroundColrs = [];
var borderColrs = [];
var defaultPlotType = 'line';
var plotColors = ['#f54242', '#5df542', '#4263f5', '#42f5e9', '#f542f5', '#000000', '#cc9900']

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
                backgroundColrs = [];
                borderColrs = [];
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
        let plotType = $.trim($(this).val());
        $('#resultPlot').css('background', '');
        if (linePlot){
            linePlot.destroy();
        }
        if(plotType === 'dline'){
            draw('line', selectedData['x'], yAxisData, legends, selectedData['xtick'], $('#two_y_axis_checkbox').prop('checked'), true);    
        }
        else{
            draw(plotType, selectedData['x'], yAxisData, legends, selectedData['xtick'], $('#two_y_axis_checkbox').prop('checked'), false);
        }
    });

    /**
     * click the I need two y-axis checkbox 
     * 
     */
    $('#two_y_axis_checkbox').click(function(){
        let plotType = $.trim($('.plot-type').find(":selected").val());
        if($(this).prop('checked') === true){
            linePlot.destroy();
            if(plotType === 'dline'){
                draw('line', selectedData['x'], yAxisData, legends, selectedData['xtick'], true, true);    
            }
            else{
                draw(plotType, selectedData['x'], yAxisData, legends, selectedData['xtick'], true, false);
            }
            
        }
        else{
            linePlot.destroy();
            if(plotType === 'dline'){
                draw('line', selectedData['x'], yAxisData, legends, selectedData['xtick'], false, true);    
            }
            else{
                draw(plotType, selectedData['x'], yAxisData, legends, selectedData['xtick'], false, false);
            }
        }
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
        if ($(checkboxes[i]).prop('checked') === true || $(checkboxes[i]).attr('checked') === "checked"){
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
            // console.info(req.responseText);    
            data = JSON.parse(req.responseText);
            let keys = Object.keys(data);
            selectedData = data;            
            $.each(selectedData['y'], function(key,value){
                legends.push(key);
                yAxisData.push(value);
            });
            if(yAxisData.length > 2){
                $('#two_axis_checkbox_container').hide();
            } 
            else if (yAxisData.length === 2){
                $('#two_axis_checkbox_container').show();
            }
        
            draw(defaultPlotType, selectedData['x'], yAxisData, legends, selectedData['xtick'], false, true);           
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
    let xSelected = false;
    let ySelected = false;
    for (let i=0; i < checkboxes.length; i++){        
        if ($(checkboxes[i]).prop('checked') === true || $(checkboxes[i]).attr('checked') === "checked"){
            if (($(checkboxes[i]).next().val()) === '1'){
                xSelected = true;
            }
            else if(($(checkboxes[i]).next().val()) === "2"){
                ySelected = true;
            }
            if(xSelected && ySelected){
                return true;
            }            
        }
    }
    return false;
}


/**
 * Draw the result plot
 */
 function draw(plotType, xAxis, yAxisData, legends, xAxisName, multiAxis, dashed){        
    let plotArea = document.getElementById('resultPlot');
    if (backgroundColrs.length == 0 && borderColrs.length == 0){
        for (let i=0; i < yAxisData.length; i++){
            let color = '';
            if (i < plotColors.length){
                color = plotColors[i];
            }
            else{
                color = getRandomColor();
            }
            backgroundColrs.push(color);
            borderColrs.push(color);
        }
    }
    let chartObject = {};
    chartObject['type'] = plotType;    
    plugins = {'title': {'display': true, 'text': 'Visualization Result'}};
    ticks_font = {family: 'Times', size: 20, style: 'normal', lineHeight: 1.2};
    x_scales = {beginAtZero: true, title: {display: true, text: xAxisName, font: ticks_font}};
    if(multiAxis && yAxisData.length === 2){
        y = {
            id: legends[0],
            position: 'left',
            beginAtZero: true, 
            max: (Math.max.apply(Math, yAxisData[0]) > 1 ? Math.max.apply(Math, yAxisData[0]) + 5 : Math.max.apply(Math, yAxisData[0]) + 0.2),
            title: {display: true, text: legends[0], font: ticks_font}
        };
        y1 = {
            id: legends[1],
            position: 'right',
            beginAtZero: true,
            max: (Math.max.apply(Math, yAxisData[1]) > 1 ? Math.max.apply(Math, yAxisData[1]) + 5 : Math.max.apply(Math, yAxisData[1]) + 0.2),
            title: {display: true, text: legends[1], font: ticks_font},
            grid: {drawOnChartArea: false,}
        };
        chartObject['options'] = {scales: {y: y, y1:y1, xAxes:x_scales}, responsive:true, 'plugins': plugins};
    }
    else{
        y_scales = {beginAtZero: true, max: getMax(yAxisData), title: {display: true, font: ticks_font}};
        chartObject['options'] = {scales: {yAxes: y_scales, xAxes:x_scales}, responsive:true, 'plugins': plugins};
    }

    chartObject['data'] = {};
    chartObject['data']['labels'] = xAxis;      
    chartObject['data']['datasets'] = []; 
    for (let i=0; i<yAxisData.length; i++){
        let temp = {};        
        temp['label'] = legends[i];       
        temp['spanGaps'] = true;
        temp['data'] = yAxisData[i];
        temp['borderWidth'] = 5;
        temp['backgroundColor'] = backgroundColrs[i];
        temp['borderColor'] = borderColrs[i];
        if(plotType == 'line' && dashed){
            temp['borderDash'] = [5, 5];
        }
        chartObject['data']['datasets'][i] = temp;
    }

    if(multiAxis && yAxisData.length === 2){
        chartObject['data']['datasets'][0]['yAxisID'] = 'y';
        chartObject['data']['datasets'][1]['yAxisID'] = 'y1';
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
    if(Math.max.apply(Math, allMax) > 1){
        return Math.max.apply(Math, allMax) + 5;
    }
    else{
        return Math.max.apply(Math, allMax) + 0.2;
    }
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



