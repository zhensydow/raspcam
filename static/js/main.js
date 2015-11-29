$( document ).ready(function() {
    $( "#b_vflip" ).click(function(){
        $.ajax({
            type: "PUT",
            dataType: "json",
            data: {vflip: true},
            url: '/ajax/camera',
            success: function( data ) {
                console.log( "vflip ok" );
            }
        });
    });

    $( "#b_hflip" ).click(function(){
        $.ajax({
            type: "PUT",
            dataType: "json",
            data: {hflip: true},
            url: '/ajax/camera',
            success: function( data ) {
                console.log( "hflip ok" );
            }
        });
    });

    setInterval(function(){
        $("#cam_img").attr("src", "/lastimage.jpg?"+new Date().getTime());
    }, 5000);

});
