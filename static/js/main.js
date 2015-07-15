$( document ).ready(function() {
    $( "#b_vflip" ).click(function(){
        $.ajax({
            type: "PUT",
            dataType: "json",
            url: '/ajax/camera',
            success: function( data ) {
                alert( "vflip ok" + data );
            }
        });
    });

    $( "#b_hflip" ).click(function(){
        $.ajax({
            type: "PUT",
            dataType: "json",
            url: '/ajax/camera',
            success: function( data ) {
                alert( "hflip ok" + data );
            }
        });
    });
});
