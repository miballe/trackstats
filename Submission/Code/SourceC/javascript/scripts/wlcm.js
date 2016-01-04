$(document).ready(function() {

  var active1 = false;
  var active2 = false;
  var active3 = false;
  var active4 = false;

    $('.wlcmNav').on('mousedown touchstart', function() {
    
    if (!active1) $(this).find('.help').css({'background-color': 'gray', 'transform': 'translate(0px,125px)'});
    else $(this).find('.help').css({'background-color': 'dimGray', 'transform': 'none'}); 
     if (!active2) $(this).find('.signUp').css({'background-color': 'gray', 'transform': 'translate(60px,105px)'});
    else $(this).find('.signUp').css({'background-color': 'darkGray', 'transform': 'none'});
      if (!active3) $(this).find('.login').css({'background-color': 'gray', 'transform': 'translate(105px,60px)'});
    else $(this).find('.login').css({'background-color': 'silver', 'transform': 'none'});
      if (!active4) $(this).find('.home').css({'background-color': 'gray', 'transform': 'translate(125px,0px)'});
    else $(this).find('.home').css({'background-color': 'silver', 'transform': 'none'});
    active1 = !active1;
    active2 = !active2;
    active3 = !active3;
    active4 = !active4;
    
  
    });
	
	
	
});