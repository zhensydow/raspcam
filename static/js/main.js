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

function refreshServerValues(){
    $.ajax({
        type: "GET",
        dataType: "json",
        url: '/ajax/camera',
        success: function( data ) {
            if( data.ok ){
                var brightness = data.params.brightness;
                $( "#txt_brightness" ).html(brightness);
                $( "#sld_brightness" ).slider("value", brightness);

                var contrast = data.params.contrast;
                $( "#txt_contrast" ).html(contrast);
                $( "#sld_contrast" ).slider("value", contrast);
            }
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
        if( event.originalEvent ){
            configCamera({brightness: ui.value});
        }
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
        if( event.originalEvent ){
            configCamera({contrast: ui.value});
        }
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

    refreshServerValues()
});
