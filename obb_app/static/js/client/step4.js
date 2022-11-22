$(document).ready(function (e) {
    // ! validate all the details from step 1 and data types
    // ! make this a validation before submit
    // ! add validation to step 3 add validation on reload
    // ! check if a gmail 
    let bookid = "";


    const validateEmail = (email) => {
        return String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
    };


    validateAllDetails(({ route, bus, selectedDate, seat_details }) => {

        let formData = new FormData();
        formData.append('route', route);
        formData.append('bus', bus);
        formData.append('selectedDate', selectedDate);
        formData.append('seat_details', JSON.stringify(seat_details));

        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            // url: '/administrator/appointment/appointments-list/',
            processData: false,
            contentType: false,
            type: 'POST',
            data: formData,
            dataType: 'json',
            beforeSend: (data) => {

            },
            success: (data) => {
                if (data.is_valid) {

                    $("#booking-details").html(data.html_booking_confirmation);
                    bookid = data.bookid;
                    localStorage.setItem('seat_details', JSON.stringify(data.passenger_details.map((e, i) => ({ ...e, discount_type: e.discount_type ? e.discount_type : "regular" }))));

                } else {
                    toastr.error(`There's an error encountered: ${data.message}`);
                }
            },
            error: (data) => {
                toastr.error(data);
            }
        }).done((data) => {
            if (data.is_valid) {

                let passenger_details = JSON.parse(localStorage.getItem('seat_details'));

                let rows = passenger_details.reduce((pv, cv, i) => (
                    pv += `
                    <tr>
                        <td>${cv.seat}</td>
                        <td>${cv.name}</td>
                        <td>${cv.email}</td>
                        <td>${cv.age}</td> 
                        <td>
                            <select name="" class="form-control discount-type" data-id=${cv.seat}>
                                ${['regular', 'senior', 'student'].reduce((pv, cvi, i) => (
                        pv += `
                                        <option value="${cvi}" ${cvi === cv.discount_type ? 'selected' : ''}> ${cvi.toUpperCase()}</option>
                                        `
                    ), '')
                    } 
                            </select>
                        </td>
                    </tr>
                    `
                ), '')

                $("#booking-details")
                    .find("#table-passenger-details")
                    .find('tbody')
                    .html(rows)
                    .on('change', 'select.discount-type', function (e) {
                        let val = $(this).val();
                        let id = $(this).data('id');
                        let index = passenger_details.findIndex((e, i) => e.seat === id);


                        if (index < 0) {
                            toastr.error("Invalid ID Detected!")
                            return;
                        }

                        let pd = passenger_details[index];

                        passenger_details[index] = { ...pd, discount_type: val }

                        localStorage.setItem('seat_details', JSON.stringify(passenger_details))
                    })
            }

        })

    });

    function validateAllDetails(ajax_func) {
        let route = localStorage.getItem('route');
        let bus = localStorage.getItem('bus');
        let seat_details = localStorage.getItem('seat_details');
        let selectedDate = localStorage.getItem('selectedDate');
        let parsedSelectedDate = new Date(selectedDate)
        if (!(route)) {
            toastr.error("Invalid Route Detected!");
            return;
        }

        if (!(bus)) {
            toastr.error("Invalid Bus Detected!");
            return;
        }

        if (parsedSelectedDate === NaN) {
            toastr.error("Invalid Date Detected!");
            return;
        }


        // NOTE: Validating the seat deails
        if (seat_details === null || seat_details === undefined) {
            seat_details = [];
        }

        if (typeof seat_details === 'string' || typeof seat_details instanceof String) {

            try {
                seat_details = JSON.parse(seat_details);
                seat_details = seat_details.filter((e, i) => (
                    e.email && e.name && e.age && (validateEmail(e.email) && typeof parseInt(e.age) === 'number')
                ))
            } catch (e) {
                seat_details = [];
            }

        }

        ajax_func({ route, bus, selectedDate, seat_details })



    }
    // NOTE: submitting step 5 and final

    $("#booking-details").on('click', 'button[btn-file-booking]', function (e) {
        let button = $(this);
        validateAllDetails(({ route, bus, selectedDate, seat_details }) => {
            let formData = new FormData();
            formData.append('route', route);
            formData.append('bus', bus);
            formData.append('selectedDate', selectedDate);
            formData.append('seat_details', JSON.stringify(seat_details));
            formData.append('booking', bookid);

            $.ajax({
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                url: '/step/5',
                processData: false,
                contentType: false,
                type: 'POST',
                data: formData,
                dataType: 'json',
                beforeSend: (data) => {

                },
                success: (data) => {
                    if (data.is_valid) { 
                        button.prop('disabled', true); 
                        localStorage.clear();  
                        toastr.success('Booking has been successful!', 'Success', {
                            timeOut: 1000,
                            preventDuplicates: true, 
                            // Redirect 
                            onHidden: function() {
                                window.location.replace("/step/5");
                            }
                        });
                    } else {
                        toastr.error(`There's an error encountered: ${data.message}`);

                    }
                },
                error: (data) => {
                    toastr.error(data);
                }
            })

        })
    })


    // NOTE: copy to clip board

    $("#booking-details").on("click", "button.btn-ctc", function (e) {
        copyToClipboard();
    })

    function copyToClipboard() {
        var copyText = $("#booking-id").text();


        navigator.permissions.query({ name: "clipboard-write" }).then((result) => {
            if (result.state == "granted" || result.state == "prompt") {
                toastr.info("Write access ranted!");
            }
        });

        navigator.permissions.query({ name: "clipboard-read" }).then((result) => {
            if (result.state == "granted" || result.state == "prompt") {
                toastr.info("Read access ranted!");
            }
        });
        navigator.clipboard.writeText(copyText).then(() => {
            toastr.info("Copied to clipboard");
        });
    }

})