$(document).ready(function() {
    // all custom jQuery will go here

    var $banner = $('#banner'); 
    var $header = $('#header');

    $(window).scroll(function () {

    	var yoffset = $(document).scrollTop();

    	if (yoffset >= $banner.outerHeight()) {
    		$header.addClass('scrolling');
    	}
    	else {
    		$header.removeClass('scrolling');
    	}

    });
	
});