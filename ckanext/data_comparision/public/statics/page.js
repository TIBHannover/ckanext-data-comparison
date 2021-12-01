$(document).ready(function(){
    $('.dcom-table-cell').mouseover(function(){
        let id = $(this).attr('name');
        id = id[id.length - 1];
        $('.dcom-column-' + id).css('background-color', 'green');

    });

    $('.dcom-table-cell').mouseout(function(){
        let id = $(this).attr('name');
        id = id[id.length - 1];
        $('.dcom-column-' + id).css('background-color', '');
    });
});