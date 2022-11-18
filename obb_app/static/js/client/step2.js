$(document).ready(function (e) {
    // NOTE: loading of bus
    getBus();
    function getBus() {
        let formData = new FormData();
        

        if (localStorage.getItem('selectedDate') === null || localStorage.getItem('selectedDate') === undefined) {
            toastr.error("Please select a date!")
            return
        }
        if (localStorage.getItem('route') === null || localStorage.getItem('route')  === undefined || localStorage.getItem('route')  === '') {
            toastr.error("Please select a route!")
            return
        }

        formData.append('date', localStorage.getItem('selectedDate'));
        formData.append('route', localStorage.getItem('route'));

        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            processData: false,
            contentType: false,
            type: 'POST',
            data: formData,
            dataType: 'json',
            beforeSend: (data) => {

            },
            success: (data) => {
                if (data.is_valid) {
                    toastr.success("You bus has been laoded!")

                    $(".bus-list-container").html(data.html_buses)

                } else {
                    toastr.error(`There's an error encountered: ${data.error}`)
                }
            },
            error: (data) => {
                toastr.error("There an error on your date or route!");
            }
        }).done((data) => {
            $(".bus-list-container").find("input:radio[name='bus']").filter(`[value='${localStorage.getItem('bus')}']`).prop('checked', true)
        })
    }


    $(".bus-list-container").on("change", "input[type='radio']", function (e) {
        if ($(this).is(":checked")) {
            // scheduleData.setRoute = $(this).val();
            localStorage.setItem('bus', $(this).val())
        }
    })
    
    
})