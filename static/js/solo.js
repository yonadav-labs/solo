function start_order(seller_id) 
{
    $.post('/start_order/', 'id='+seller_id+'&location='+customer_location)
    .success(function(data){
      $('#order_div').html(data);
    });
    $('#map_wrapper').hide();
}

function agree_terms(obj)
{
	var flag = $(obj).prop('checked');
	if (flag)
		$('#connect_stripe').removeClass('disabled');
	else 
		$('#connect_stripe').addClass('disabled');
}