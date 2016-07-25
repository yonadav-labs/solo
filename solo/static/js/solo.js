function start_order(seller_id, seller_distance) 
{
	$.post('/start_order/', 'id='+seller_id+'&location='+customer_location+'&distance='+seller_distance)
	.success(function(data){
	  $('#order_div').html(data);
	});
	$('#map_wrapper').hide();
	$('#seller_wrapper').hide();
}

function agree_terms(obj)
{
	var flag = $(obj).prop('checked');
	$('#connect_stripe').addClass('disabled');

	if (flag)
		$('#connect_stripe').removeClass('disabled');
}

$(function(){
	$( "#id_permit_exp" ).datepicker({
		dateFormat: "yy-mm-dd",
		defaultDate: +30,
		minDate: 1
	});

	if (typeof open_hour != 'undefined') {
	$("#slider-range").slider({
		range: true,
		min: 0,
		max: 1440,
		step: 15,
		values: [open_hour, close_hour],
		slide: function (e, ui) {
			var hours1 = Math.floor(ui.values[0] / 60);
			var minutes1 = ui.values[0] - (hours1 * 60);
			$('#id_open_hour').val(hours1 + ':' + minutes1);

			if (hours1.length == 1) hours1 = '0' + hours1;
			if (minutes1.length == 1) minutes1 = '0' + minutes1;
			if (minutes1 == 0) minutes1 = '00';
			if (hours1 >= 12) {
				if (hours1 == 12) {
					hours1 = hours1;
					minutes1 = minutes1 + " p.m.";
				} else {
					hours1 = hours1 - 12;
					minutes1 = minutes1 + " p.m.";
				}
			} else {
				hours1 = hours1;
				minutes1 = minutes1 + " a.m.";
			}
			if (hours1 == 0) {
				hours1 = 12;
				minutes1 = minutes1;
			}

			$('.slider-time').html(hours1 + ':' + minutes1);

			var hours2 = Math.floor(ui.values[1] / 60);
			var minutes2 = ui.values[1] - (hours2 * 60);
			
			$('#id_close_hour').val(hours2 + ':' + minutes2);
			if (hours2 == 24 && minutes2 == 0)
				$('#id_close_hour').val('23:59');
			
			if (hours2.length == 1) hours2 = '0' + hours2;
			if (minutes2.length == 1) minutes2 = '0' + minutes2;
			if (minutes2 == 0) minutes2 = '00';
			if (hours2 >= 12) {
				if (hours2 == 12) {
					hours2 = hours2;
					minutes2 = minutes2 + " p.m.";
				} else if (hours2 == 24) {
					hours2 = 11;
					minutes2 = "59 p.m.";
				} else {
					hours2 = hours2 - 12;
					minutes2 = minutes2 + " p.m.";
				}
			} else {
				hours2 = hours2;
				minutes2 = minutes2 + " a.m.";
			}

			$('.slider-time2').html(hours2 + ':' + minutes2);
		}
	});
	}

	// videojs('landing-video').ready(function() {
	// 	console.log('start');
	//     this.play();
	// });

	// videojs.autoSetup();

    // videojs('landing-video').ready(function(){
      // console.log(this.options()); //log all of the default videojs options
      
       // Store the video object
      // var myPlayer = this, id = myPlayer.id();
      // // Make up an aspect ratio
      // var aspectRatio = 264/640; 

      // function resizeVideoJS(){
      //   var width = document.getElementById(id).parentElement.offsetWidth;
      //   // myPlayer.width(width).height( width * aspectRatio );
      // }
      
      // // Initialize resizeVideoJS()
      // resizeVideoJS();
      // // Then on resize call resizeVideoJS()
      // window.onresize = resizeVideoJS; 
  	 //  console.log('start');
    //   this.play();
    // });	
});
