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

$(function() {
	$( "#id_permit_exp" ).datepicker({
		dateFormat: "yy-mm-dd",
		defaultDate: +30,
		minDate: 1
	});
});