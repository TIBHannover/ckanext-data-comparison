$(document).ready(function(){
    $('.dcom-table-cell').mouseover(function(){
        let id = $(this).attr('name');
        id = id[id.length - 1];
        let checkbox = $('#col-checkbox-' + id);
        if ($(checkbox).prop('checked') === false){
            $('.dcom-column-' + id).css('background-color', 'yellow');        
        }

    });

    $('.dcom-table-cell').mouseout(function(){
        let id = $(this).attr('name');
        id = id[id.length - 1];
        let checkbox = $('#col-checkbox-' + id);
        if ($(checkbox).prop('checked') === false){
            $('.dcom-column-' + id).css('background-color', '');       
        }
    });

    $('.dcom-table-cell').click(function(){
        let id = $(this).attr('name');
        id = id[id.length - 1];
        let checkbox = $('#col-checkbox-' + id);
        $(checkbox).click();
        if ($(checkbox).prop('checked') === true){
            $('.dcom-column-' + id).css('background-color', 'green');        
        }
        else{
            $('.dcom-column-' + id).css('background-color', '');
        }





        

    });




});