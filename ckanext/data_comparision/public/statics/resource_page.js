var plotColors = ['#f54242', '#5df542', '#4263f5', '#42f5e9', '#f542f5', '#000000', '#cc9900']

$(document).ready(function(){
    let dest_url = $('#resource_plot_preview_url').val();
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == XMLHttpRequest.DONE && req.status === 200) {   
            // console.info(req.responseText);    
            if(req.responseText !== "false"){
                data = JSON.parse(req.responseText);
                if (data.hasOwnProperty('x')){
                    // data is csv
                    draw('line', data['x'], [data['y']], [data['y_tick']], data['x_tick'], false, true);
                    $('.attemp-to-plot-loading').hide();
                }
                else{
                    // data is xlsx
                    let counter = 1;
                    $.each(data, function(key, value){
                        if (counter === 1){
                            draw('line', value['x'], [value['y']], [value['y_tick']], value['x_tick'], false, true, "resultPlot", text="sheet: " + key);
                        }
                        else{
                            let canvas = document.createElement('canvas');
                            canvas.setAttribute('id', "resultPlot" + counter);
                            canvas.setAttribute('width', "300");
                            canvas.setAttribute('height', "200");
                            let div = document.createElement('div');
                            div.classList.add("col-sm-4");
                            div.append(canvas);
                            $('#resource-preview-canvas-area').append(div);                            
                            draw('line', value['x'], [value['y']], [value['y_tick']], value['x_tick'], false, true, "resultPlot" + counter, text="sheet: " + key);
                        }
                        counter += 1;
                        $('.attemp-to-plot-loading').hide();
                    });
                }        
            }
            else{
                $('#analysis-result-area').hide();
            }              
        }
    }
    req.open("GET", dest_url);
    req.send();
});


/**
 * Draw the result plot
 */
 function draw(plotType, xAxis, yAxisData, legends, xAxisName, multiAxis, dashed, canvasId="resultPlot", text="Visualization Result"){
    let plotArea = document.getElementById(canvasId);
    let colors = [];
    for (let i=0; i < yAxisData.length; i++){
        let color = '';
        if (i < plotColors.length){
            color = plotColors[i];
        }
        else{
            color = getRandomColor();
        }
        colors.push(color);
    }
    let chartObject = {};
    chartObject['type'] = plotType;
    plugins = {'title': {'display': true, 'text': text}};
    ticks_font = {family: 'Times', size: 20, style: 'normal', lineHeight: 1.2};
    x_scales = {beginAtZero: true, title: {display: true, text: xAxisName, font: ticks_font}};
    y = {
        id: legends[0],
        position: 'left',
        beginAtZero: true, 
        max: Math.max.apply(Math, yAxisData[0]) + 10,
        title: {display: true, text: legends[0], font: ticks_font}
    };
    chartObject['options'] = {scales: {y: y, xAxes:x_scales}, responsive:true, 'plugins': plugins};
    chartObject['data'] = {};
    chartObject['data']['labels'] = xAxis; 
    chartObject['data']['datasets'] = []; 
    for (let i=0; i<yAxisData.length; i++){
        let temp = {};
        temp['label'] = legends[i];
        temp['data'] = yAxisData[i];
        temp['borderWidth'] = 1;
        temp['backgroundColor'] = colors[i];
        temp['borderColor'] = colors[i];
        if(plotType == 'line' && dashed){
            temp['borderDash'] = [5, 5];
        }
        chartObject['data']['datasets'][i] = temp;
    }
    
    linePlot = new Chart(plotArea, chartObject);
    
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