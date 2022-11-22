$(document).ready(function() {
    let booking_id = ""
    $("#form-book-id-search").on('submit', function(e){
        e.preventDefault();
        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            url: '/step/final',
            // processData: false,
            // contentType: false,
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            beforeSend: (data) => {

            },
            success: (data) => {
                if (data.is_valid) { 
                    
                    toastr.success(data.message);
                    $("div.booking-details").html(data.html_booking_details)
                } else {
                    toastr.error(data.message);
                    $("div.booking-details").empty();
                }
               
            },
            error: (data) => {
                toastr.error(data);
            }
        }).done((data) => {
            booking_id = data.booking_id;
           

        })



    });


    $("div.booking-details").on('submit', '#form-g-cash-ref-id', function(e){
        e.preventDefault();

        let form = $(this);

        let gcash_ref = form.find('input[name="g_cash_ref_id"]');

        if (!(gcash_ref).val()){

            gcash_ref.removeClass('is-valid').addClass('is-invalid');
            toastr.error("Please enter the Reference ID of your GCash Payment");

            return;
        }
 
        if(!(booking_id)){
            toastr.error("Please enter your booking ID")
            return;
        }

        gcash_ref.removeClass('is-invalid').addClass('is-valid');

        let formData = new FormData();
        formData.append('booking_id', booking_id);
        formData.append('payment_ref_id', gcash_ref.val());
        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            url: '/update-reference-id/',
            processData: false,
            contentType: false,
            type: 'POST',
            data: formData,
            dataType: 'json',
            beforeSend: (data) => {

            },
            success: (data) => {
                if (data.is_valid) { 
                     
                    form.find(':input, :button').prop('disabled', true)
                    toastr.success('Your booking payment has been successful! Thank you', 'Success', {
                        timeOut: 1500,
                        preventDuplicates: true, 
                        // Redirect 
                        onHidden: function() {
                            window.location.replace("/");
                        }
                    });
                } else {
                    toastr.error(data.message); 
                }
               
            },
            error: (data) => {
                toastr.error(data);
            }
        })
        
    })
})