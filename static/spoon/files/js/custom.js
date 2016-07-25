

	/*
	|--------------------------------------------------------------------------
	| GOOGLE ANALYTICS
	|--------------------------------------------------------------------------
	*/	
	/*************** REPLACE WITH YOUR OWN UA NUMBER ***********/
	window.onload = function () { "use strict"; gaSSDSLoad(); }; //load after page onload
	/*************** REPLACE WITH YOUR OWN UA NUMBER ***********/



	$(document).ready(function() { 
		"use strict";
		$( ".neko-mega-menu" ).wrapInner( "<div></div>");





	/*
	|--------------------------------------------------------------------------
	| Revolution slider fullscreen
	|--------------------------------------------------------------------------
	*/	

	if($('#rs-slider-fullscreen').length){

		$('#rs-slider-fullscreen').revolution(
		{
			debugMode: false,
			sliderType:'standard',
			jsFileLocation:'js-plugins/rs-plugin/js/',
			sliderLayout:'fullscreen',
			fullScreenOffsetContainer:'.menu-header',
			responsiveLevels: [1200,1024,768,480],
			gridwidth:1140,
			gridheight:720,	
			delay:6500,
			spinner:'spinner4',
			lazyType: 'none',
			navigation: {
				onHoverStop:"off",
				touch:{
					touchenabled:"on",
					swipe_threshold: 75,
					swipe_min_touches: 1,
					swipe_direction: "horizontal",
					drag_block_vertical: false
				},
				arrows: {
					style:"zeus",
					enable:true,
					hide_onmobile:true,
					hide_under:480,
					hide_onleave:true,
					hide_delay:200,
					hide_delay_mobile:1200,
					tmp: '<div class="tp-title-wrap"></div>',
					left: {
						h_align: "left",
						v_align: "center",
						h_offset: 10,
						v_offset: 0
					},
					right: {
						h_align: "right",
						v_align: "center",
						h_offset: 10,
						v_offset: 0
					}
				},
				bullets: {
					enable: true,
					hide_onmobile: false,
					style: 'zeus',
					hide_onleave: false,
					direction: 'horizontal',
					tmp: '<span class="tp-bullet-title"></span>',
					h_align: 'left',
					v_align: 'bottom',
					h_offset: 20,
					v_offset: 30,
					space: 5
				}
			}



		});

}


/*
	|--------------------------------------------------------------------------
	| Revolution slider fullwidth 1
	|--------------------------------------------------------------------------
	*/	

	if($('#rs-slider-fullwidth-1').length){

		$('#rs-slider-fullwidth-1').revolution(
		{
			debugMode: false,
			sliderType:'standard',
			jsFileLocation:'js-plugins/rs-plugin/js/',
			sliderLayout:'fullwidth',
			responsiveLevels: [1200,1025,768,480],
			delay:3000,
			gridheight:720,	
			spinner:'spinner2',
			lazyType: 'none',
			navigation: {
				onHoverStop:"off",
				touch:{
					touchenabled:"on",
					swipe_threshold: 75,
					swipe_min_touches: 1,
					swipe_direction: "horizontal",
					drag_block_vertical: false
				},
				arrows: {
					style:"gyges",
					enable:true,
					hide_onmobile:true,
					hide_under:480,
					hide_onleave:true,
					hide_delay:200,
					hide_delay_mobile:1200,
					tmp: '<div class="tp-title-wrap"></div>',
					left: {
						h_align: "left",
						v_align: "center",
						h_offset: 10,
						v_offset: 0
					},
					right: {
						h_align: "right",
						v_align: "center",
						h_offset: 10,
						v_offset: 0
					}
				},
				bullets: {
					enable: true,
					hide_onmobile: true,
					hide_onleave: false,
					direction: 'horizontal',
					tmp: '<span class="tp-bullet-title"></span>',
					h_align: 'center',
					v_align: 'bottom',
					h_offset: 0,
					v_offset: 30,
					space: 5
				}
			}
		});
	}

	/*
	|--------------------------------------------------------------------------
	| Revolution slider kenburn
	|--------------------------------------------------------------------------
	*/	

	if($('#rs-slider-kenburn').length){

		$('#rs-slider-kenburn').revolution(
		{
			debugMode: false,
			sliderType:'standard',
			jsFileLocation:'js-plugins/rs-plugin/js/',
			sliderLayout:'fullwidth',
			responsiveLevels: [1200,1025,768,480],
			delay:5000,
			gridheight:720,	
			spinner:'spinner2',
			lazyType: 'none',
			navigation: {
				onHoverStop:"off",
				touch:{
					touchenabled:"on",
					swipe_threshold: 75,
					swipe_min_touches: 1,
					swipe_direction: "horizontal",
					drag_block_vertical: false
				},
				arrows: {
					style:"gyges",
					enable:true,
					hide_onmobile:true,
					hide_under:480,
					hide_onleave:true,
					hide_delay:200,
					hide_delay_mobile:1200,
					tmp: '<div class="tp-title-wrap"></div>',
					left: {
						h_align: "left",
						v_align: "center",
						h_offset: 10,
						v_offset: 0
					},
					right: {
						h_align: "right",
						v_align: "center",
						h_offset: 10,
						v_offset: 0
					}
				},
				bullets: {
					enable: true,
					hide_onmobile: true,
					tmp: '<span class="tp-bullet-title"></span>',
					hide_onleave: false,
					direction: 'horizontal',
					h_align: 'center',
					v_align: 'bottom',
					h_offset: 0,
					v_offset: 30,
					space: 5
				}
			}



		});

}



$('#menu-opener').click(function(event) {
	event.preventDefault();

	var $finalHeight = ($('#features-section-menu').height() == 500 ) ? 0 : 500;

	$('#features-section-menu > div').animate({
		height: $finalHeight },
		300, 'easeInOutCubic',function() {
			/* stuff to do after animation is complete */
		});

	if( 0 == $finalHeight){
		$(this).html('<i class="icon-plus"></i> open <span>Neko bloc quick menu</span>');
	}else{
		$(this).html('<i class="icon-minus"></i> close <span>Neko bloc quick menu</span>');
	}

});


$(".copy-button-simple").each(function(index, el) {

	var $this = $(this),
	client = new ZeroClipboard( $this );

	client.on( "ready", function( event ) {
			//alert( "ZeroClipboard SWF is ready!" );


			client.on( 'copy', function(event) {
				var data = $this.parent().next('section')[0].outerHTML;
				var final_data = data.replace(/<!--[\s\S]*?-->/g, '');
				event.clipboardData.clearData();
				event.clipboardData.setData('text/plain', final_data);
				//event.clipboardData.setData('text/html', $data);
			});

			client.on( "aftercopy", function( event ) {
				alert("Bloc copied successfully");
			});
		});	
	
});

$(".copy-button-hidden-source").each(function(index, el) {

	var $this = $(this),
	client = new ZeroClipboard( $this );

	client.on( "ready", function( event ) {
			//alert( "ZeroClipboard SWF is ready!" );


			client.on( 'copy', function(event) {
				var data = $this.next('textarea').text();

				
				event.clipboardData.clearData();
				event.clipboardData.setData('text/plain', data);
				//event.clipboardData.setData('text/html', $data);
			});

			client.on( "aftercopy", function( event ) {
				alert("Bloc copied successfully");
			});
		});	
	
});


}); //End Doc Ready




/*
|--------------------------------------------------------------------------
| Revolution slider fullwidth
|--------------------------------------------------------------------------
*/	

function gaSSDSLoad(acct) {
	"use strict";  
	var gaJsHost = (("https:" === document.location.protocol) ? "https://ssl." : "http://www."),
	pageTracker,
	s;
	s = document.createElement('script');
	s.src = gaJsHost + 'google-analytics.com/ga.js';
	s.type = 'text/javascript';
	s.onloadDone = false;
	function init () {
		pageTracker = _gat._getTracker(acct);
		pageTracker._trackPageview();
	}
	s.onload = function () {
		s.onloadDone = true;
		init();
	};
	s.onreadystatechange = function() {
		if (('loaded' === s.readyState || 'complete' === s.readyState) && !s.onloadDone) {
			s.onloadDone = true;
			init();
		}
	};
	document.getElementsByTagName('head')[0].appendChild(s);
}


/*
|--------------------------------------------------------------------------
| Google maps
|--------------------------------------------------------------------------
*/	

function initialize(id) {
	"use strict";
	var image = 'images/icon-map.png';

	var overlayTitle = 'Agencies';

	var locations = [
	/* point number 1 */
	['Madison Square Garden', '4 Pennsylvania Plaza, New York, NY'],

	/* point number 2 */
	['Best town ever', 'Santa Cruz', 36.986021, -122.02216399999998],

	/* point number 3 */
	['Midwest Agency', 'Kansas'],

	/* point number 4 */
	['I\'ll definitly be there one day', 'Chicago', 41.8781136, -87.62979819999998] 
	];

	/*** DON'T CHANGE ANYTHING PASSED THIS LINE ***/
	id = (id === undefined) ? 'map-wrapper' : id;

	var map = new google.maps.Map(document.getElementById(id), {
		scrollwheel: false,
		zoomControl: true,
		zoomControlOptions: {
			style: google.maps.ZoomControlStyle.LARGE,
			position: google.maps.ControlPosition.LEFT_CENTER
		},
		streetViewControl:true,
		scaleControl:false,
		zoom: 14
	});

	if($mapType == 'SATELLITE'){
		map.setMapTypeId(google.maps.MapTypeId.SATELLITE);
	}else if($mapType == 'HYBRID'){
		map.setMapTypeId(google.maps.MapTypeId.HYBRID);
	}else if($mapType == 'TERRAIN'){
		map.setMapTypeId(google.maps.MapTypeId.TERRAIN);
	}else{
		map.setMapTypeId(google.maps.MapTypeId.ROADMAP);
	}

	if($mapStyle == 'light' && $mapType == 'ROADMAP'){
		var $flatMap = [{"elementType":"labels.text","stylers":[{"visibility":"on"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"color":"#f5f5f2"},{"visibility":"on"}]},{"featureType":"administrative","stylers":[{"visibility":"on"}]},{"featureType":"transit","stylers":[{"visibility":"on"}]},{"featureType":"poi.attraction","stylers":[{"visibility":"on"}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"visibility":"on"}]},{"featureType":"poi.business","stylers":[{"visibility":"on"}]},{"featureType":"poi.medical","stylers":[{"visibility":"on"}]},{"featureType":"poi.place_of_worship","stylers":[{"visibility":"on"}]},{"featureType":"poi.school","stylers":[{"visibility":"on"}]},{"featureType":"poi.sports_complex","stylers":[{"visibility":"on"}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"color":"#ffffff"},{"visibility":"simplified"}]},{"featureType":"road.arterial","stylers":[{"visibility":"simplified"},{"color":"#ffffff"}]},{"featureType":"road.highway","elementType":"labels.icon","stylers":[{"color":"#ffffff"},{"visibility":"on"}]},{"featureType":"road.highway","elementType":"labels.icon","stylers":[{"visibility":"on"}]},{"featureType":"road.arterial","stylers":[{"color":"#ffffff"}]},{"featureType":"road.local","stylers":[{"color":"#ffffff"}]},{"featureType":"poi.park","elementType":"labels.icon","stylers":[{"visibility":"on"}]},{"featureType":"poi","elementType":"labels.icon","stylers":[{"visibility":"on"}]},{"featureType":"water","stylers":[{"color":"#71c8d4"}]},{"featureType":"landscape","stylers":[{"color":"#e5e8e7"}]},{"featureType":"poi.park","stylers":[{"color":"#8ba129"}]},{"featureType":"road","stylers":[{"color":"#ffffff"}]},{"featureType":"poi.sports_complex","elementType":"geometry","stylers":[{"color":"#c7c7c7"},{"visibility":"on"}]},{"featureType":"water","stylers":[{"color":"#a0d3d3"}]},{"featureType":"poi.park","stylers":[{"color":"#91b65d"}]},{"featureType":"poi.park","stylers":[{"gamma":1.51}]},{"featureType":"road.local","stylers":[{"visibility":"on"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"visibility":"on"}]},{"featureType":"poi.government","elementType":"geometry","stylers":[{"visibility":"on"}]},{"featureType":"landscape","stylers":[{"visibility":"on"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"on"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"visibility":"simplified"}]},{"featureType":"road.local","stylers":[{"visibility":"simplified"}]},{"featureType":"road"},{"featureType":"road"},{},{"featureType":"road.highway"}];
		var styledMap = new google.maps.StyledMapType($flatMap, {name: "light"});
	}else if($mapStyle == 'dark' && $mapType == 'ROADMAP'){
		var $darkMap = [{"stylers":[{"visibility":"on"},{"saturation":-100},{"gamma":0.54}]},{"featureType":"road","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"water","stylers":[{"color":"#4d4946"}]},{"featureType":"poi","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"poi","elementType":"labels.text","stylers":[{"visibility":"simplified"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"road.local","elementType":"labels.text","stylers":[{"visibility":"simplified"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"gamma":0.48}]},{"featureType":"transit.station","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"gamma":7.18}]}];
		var styledMap = new google.maps.StyledMapType($darkMap, {name: "dark"});
	}else if($mapStyle == 'gray' && $mapType == 'ROADMAP'){
		var $grayMap = [{"featureType":"landscape","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","stylers":[{"saturation":-100},{"lightness":51},{"visibility":"simplified"}]},{"featureType":"road.highway","stylers":[{"saturation":-100},{"visibility":"on"}]},{"featureType":"road.arterial","stylers":[{"saturation":-100},{"lightness":30},{"visibility":"on"}]},{"featureType":"road.local","stylers":[{"saturation":-100},{"lightness":40},{"visibility":"on"}]},{"featureType":"transit","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"administrative.province","stylers":[{"visibility":"on"}]},{"featureType":"water","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":-25},{"saturation":-100}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]}];
		var styledMap = new google.maps.StyledMapType($grayMap, {name: "grey"});
	}

	if( $mapStyle != 'DEFAULT' && $mapType == 'ROADMAP'){
		map.mapTypes.set('map_style', styledMap);
		map.setMapTypeId('map_style');
	}

	var myLatlng;
	var marker, i;
	var bounds = new google.maps.LatLngBounds();
	var infowindow = new google.maps.InfoWindow({ content: "loading..." });

	for (i = 0; i < locations.length; i++) { 


		if(locations[i][2] !== undefined && locations[i][3] !== undefined){
			var content = '<div class="infoWindow"><h3>'+locations[i][0]+'</h3><p>'+locations[i][1]+'</p></div>';
			(function(content) {
				myLatlng = new google.maps.LatLng(locations[i][2], locations[i][3]);

				marker = new google.maps.Marker({
					position: myLatlng,
					icon:image,  
					title: overlayTitle,
					map: map
				});

				google.maps.event.addListener(marker, 'click', (function() {
					return function() {
						infowindow.setContent(content);
						infowindow.open(map, this);
					};

				})(this, i));

				if(locations.length > 1){
					bounds.extend(myLatlng);
					map.fitBounds(bounds);
				}else{
					map.setCenter(myLatlng);
				}

			})(content);
		}else{

			var geocoder   = new google.maps.Geocoder();
			var info   = locations[i][0];
			var addr   = locations[i][1];
			var latLng = locations[i][1];

			(function(info, addr) {

				geocoder.geocode( {

					'address': latLng

				}, function(results) {

					myLatlng = results[0].geometry.location;

					marker = new google.maps.Marker({
						position: myLatlng,
						icon:image,  
						title: overlayTitle,
						map: map
					});
					var $content = '<div class="infoWindow"><h3>'+info+'</h3><p>'+addr+'</p></div>';
					google.maps.event.addListener(marker, 'click', (function() {
						return function() {
							infowindow.setContent($content);
							infowindow.open(map, this);
						};
					})(this, i));

					if(locations.length > 1){
						bounds.extend(myLatlng);
						map.fitBounds(bounds);
					}else{
						map.setCenter(myLatlng);
					}
				});
			})(info, addr);

		}
	}
}