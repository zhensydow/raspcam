function configCamera( newconfig ){
    $.ajax({
        type: "PUT",
        dataType: "json",
        data: newconfig,
        url: '/ajax/camera',
        success: function( data ) {
            console.log( "camera config OK" );
        }
    });
}

$( document ).ready(function(){
    $( "#sld_brightness" ).slider({
        value: 50,
        min: 0,
        max: 100,
        animate: true,
        range: "min"
    });

    $( "#sld_brightness" ).on( "slidechange", function( event, ui ){
        $( "#txt_brightness" ).html(ui.value);
        configCamera({brightness: ui.value});
    });

    $( "#sld_contrast" ).slider({
        value: 0,
        min: -100,
        max: 100,
        animate: true,
        range: "min"
    });

    $( "#sld_contrast" ).on( "slidechange", function( event, ui ){
        $( "#txt_contrast" ).html(ui.value);
        configCamera({contrast: ui.value});
    });

    $( "#b_vflip" ).click(function(){
        configCamera({vflip: true});
    });

    $( "#b_hflip" ).click(function(){
        configCamera({hflip: true});
    });

    setInterval(function(){
        $("#cam_img").attr("src", "/lastimage.jpg?"+new Date().getTime());
    }, 5000);

});
