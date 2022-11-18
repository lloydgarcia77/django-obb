$(document).ready(function (e) {
    // NOTE: loading of bus
    getSeats();
    function getSeats() {
        let formData = new FormData(); 

        if (localStorage.getItem('selectedDate') === null || localStorage.getItem('selectedDate') === undefined) {
            toastr.error("Please select a date!")
            return
        }
        if (localStorage.getItem('route') === null || localStorage.getItem('route')  === undefined || localStorage.getItem('route')  === '') {
            toastr.error("Please select a route!")
            return
        }
        if (localStorage.getItem('bus') === null || localStorage.getItem('bus')  === undefined) {
            toastr.error("Please select a bus!")
            return
        }

        formData.append('date', localStorage.getItem('selectedDate'));
        formData.append('route', localStorage.getItem('route'));
        formData.append('bus', localStorage.getItem('bus'));

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

                    $(".bus-seats-list-container").html(data.html_seats)

                } else {
                    toastr.error(`There's an error encountered: ${data.error}`)
                }
            },
            error: (data) => {
                toastr.error("There an error on your date, route or bus!");
            }
        })
    }


    // $(".bus-list-container").on("change", "input[type='radio']", function (e) {
    //     if ($(this).is(":checked")) {
    //         // scheduleData.setRoute = $(this).val();
    //         localStorage.setItem('bus', $(this).val())
    //     }
    // })

})