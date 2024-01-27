let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default country
        componentRestrictions: {'country': ['co']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Type your address...";
    }
    else{
        // console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value 
    geocoder.geocode({'address': address}, function(results, status){
        if(status === google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            $('#id_latitude').val(latitude);
            $('#id_longuitude').val(longitude);
            $('#id_address').val(address);
        }
    });
    console.log(place.address_components)
    for (var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] === 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            if(place.address_components[i].types[j] === 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            if(place.address_components[i].types[j] === 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            if(place.address_components[i].types[j] === 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val('')
            }

        }
    }
}


$(document).ready(function(){
    // Add to cart
    $('.addToCart').on('click', function(e){
        e.preventDefault();
        product_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'notAuthenticated'){
                    Swal.fire(response.message, '', 'info').then(function(){
                        window.location = '/login/';
                    })
                }else if(response.status == 'Failed'){
                    Swal.fire(response.message, '', 'error')
                }else{
                $('#cart_counter').html(response.cart_counter)
                $('#qty-'+product_id).html(response.qty)

                // Update subtotal, tax and total
                applyCartTotals(
                    response.cart_totals.sub_total,
                    response.cart_totals.tax,
                    response.cart_totals.grand_total,
                )
            }}
        })
    })


    // Remove from cart
    $('.removeFromCart').on('click', function(e){
        e.preventDefault();
        product_id = $(this).attr('data-id');
        cart_id = $(this).attr('id');
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'notAuthenticated'){
                    Swal.fire(response.message, '', 'info').then(function(){
                        window.location = '/login/';
                    })
                }else if(response.status == 'Failed'){
                    Swal.fire(response.message, '', 'error')
                }else{
                $('#cart_counter').html(response.cart_counter)
                $('#qty-'+product_id).html(response.qty)

                    // Update subtotal, tax and total
                    applyCartTotals(
                    response.cart_totals.sub_total,
                    response.cart_totals.tax,
                    response.cart_totals.grand_total,
                    )

                    if(window.location.pathname == '/cart/'){
                    removeCartItem(response.qty, cart_id);
                    checkEmptyCart()
                     };
            }}
        })
    })


    // Place the cart item quantity
    $('.item_qty').each(function(){
        var product_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + product_id).html(qty)
    })


    // Delete cart item
        $('.deleteCart').on('click', function(e){
            e.preventDefault();
            cartId = $(this).attr('data-id');
            url = $(this).attr('data-url');
            $.ajax({
                type: 'GET',
                url: url,
                success: function(response){
                     if(response.status == 'Failed'){
                        Swal.fire(response.message, '', 'error')
                    }else{
                    $('#cart_counter').html(response.cart_counter)
                    Swal.fire(response.status, response.message, 'success')
                                    // Update subtotal, tax and total
                applyCartTotals(
                    response.cart_totals.sub_total,
                    response.cart_totals.tax,
                    response.cart_totals.grand_total,
                )
                    removeCartItem(0, cartId)
                    checkEmptyCart();
                }}
            })
        })


        // Update cart item on the page
        function removeCartItem(cartItemQty, cartId){
            
                if(cartItemQty <= 0){
                    document.getElementById('cart-item-'+cartId).remove();
                }
        
            }
            

        // Check if the cart is empty
        function checkEmptyCart(){
            var cart_counter = document.getElementById('cart_counter').innerHTML;
            if(cart_counter==0){
                document.getElementById('empty-cart').style.display = 'block';
            }
        }

        // Update cart subtotal, tax and total
        function applyCartTotals(subtotal, tax, total){
            if(window.location.pathname == '/cart/'){
                $('#subtotal').html(subtotal);
                $('#tax').html(tax);
                $('#total').html(total);
                console.log(subtotal, tax, total)
        }
    }

    // Add opening hours

    $('.add_hour').on('click',function(e){
        e.preventDefault();
        const day = document.getElementById('id_day').value
        const from_hour = document.getElementById('id_from_hour').value
        const to_hour = document.getElementById('id_to_hour').value
        let is_closed = document.getElementById('id_is_closed').checked
        const csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        const url = document.getElementById('add_hour_url').value
        if(is_closed){
            is_closed = 'True'
            condition = "day != ''"
        }else{
            is_closed = 'False'
            condition = "day!='' && from_hour!='' && to_hour!=''"
        }
        if(eval(condition)){
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day':day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token
                },
                success: function(response){
                    if(response.status == 'success'){
                        if(response.is_closed=='Closed'){
                            html= '<tr id="day-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/vendor/openingHours/remove/'+response.id+'">Remove</a></td></tr>'
                        }else{
                            html = '<tr id="day-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/openingHours/remove/'+response.id+'">Remove</a></td></tr>'
                        }
                        
                        $('.opening_hours').append(html)
                        document.getElementById('opening_hours').reset()
                    }else{
                        Swal.fire(response.message, '', 'error')
                    }
                }
            })
        }else{
            Swal.fire('Please fill all the required fields', '', 'info')
        }
    })

    // Remove opening hours
    $(document).on('click', '.remove_hour', function(e){
        e.preventDefault();
        url = $(this).attr('data-url')

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'success'){
                    document.getElementById('day-'+response.id).remove()
                }
            },
        }) 
    })
});
