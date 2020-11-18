var resize = function() {
    var a = 1;
    var wH = $(window).height();
    var wW = $(window).width();
    if(wH<=wW){
        vH = wH-5
        $("#bg_img").css("height", vH + "px");    
    }else{
        vW = wW-5
        $("#bg_img").css("width", vW + "px"); 
    }

    // console.log();
};



window.onresize = function(event) {
    resize();
};

resize();

