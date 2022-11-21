$(document).ready(function (e) {
    // NOTE: replace gender with age!
    // ! if change route then reset step 2 to 4
    const seatDetails = {
        data: [],
        set setData(d) {

            let details = d;
            if (d === null || d === undefined) {
                details = [];
            }
            if (typeof d === 'string' || typeof d instanceof String) {
                try {
                    details = JSON.parse(details);
                    details = details.filter((e,i) => (
                        e.email && e.name && e.age && (validateEmail(e.email) && typeof parseInt(e.age) === 'number')
                    ))
                    console.log(details);
                } catch (e) {
                    details = [];
                }

            }
            this.data = details;
        },
        get getData() {
            return this.data;
        },
        set appendData(d) {
            this.data.push({
                'seat': d,
                'name': '',
                'email': '',
                'age': 0,
            })
        },
        set removeData(d) {
            this.data = this.data.filter((e, i) => e.seat !== d)
        },

        updateData: function (index, data) {
            // let objIndex = seatDetails.getData.findIndex((elem) => elem.seat === id);
            let d = this.data[index];
            if (d < 0) {
                toastr.error("Seat Not Found");
                return;
            }

            this.data[index] = { ...d, ...data };


            localStorage.setItem('seat_details', JSON.stringify(this.data))
        },
        fetchPassengerDetails: function () {
            let table_rows = this.data.map((e, i) => (
                `
                    <tr data-id="${e.seat}">
                        <td class="text-uppercase"><b>${e.seat}</b></td>
                        <td>
                            <input name="name" type="text" class="form-control" required value="${e.name}"/>
                        </td>
                        <td>
                            <input name="email" type="email" class="form-control" required value="${e.email}"/>
                        </td>
                        <td>
                            <input name="age" type="number" class="form-control" required value="${e.age}"/>
                        </td>
                        <td>
                            <button type="button" class="btn btn-primary btn-sm save">
                                <i class="fas fa-save"></i>
                            </button>
                        </td>
                    </tr>
                `
            ))
            $('table.passenger').find('tbody').html(table_rows);
        },
        loadData: function (input) {

            let ids = this.data.map((e, i) => `[value="${e.seat}"]`).toString();
            input.filter(ids).prop('checked', true);
            this.fetchPassengerDetails()
        }


    };
    const validateEmail = (email) => {
        return String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
    };

    // ! valdiate the seat details upon load 

    seatDetails.setData = localStorage.getItem('seat_details'); 

    // NOTE: loading of bus
    getSeats();
    function getSeats() {
        let formData = new FormData();

        if (localStorage.getItem('selectedDate') === null || localStorage.getItem('selectedDate') === undefined) {
            toastr.error("Please select a date!")
            return
        }
        if (localStorage.getItem('route') === null || localStorage.getItem('route') === undefined || localStorage.getItem('route') === '') {
            toastr.error("Please select a route!")
            return
        }
        if (localStorage.getItem('bus') === null || localStorage.getItem('bus') === undefined) {
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
        }).done((data) => {


            seatDetails.loadData($("input[type='checkbox'].seat"));


            $("input[type='checkbox'].seat").on("change", function (e) {
                if ($(this).is(":checked")) {

                    seatDetails.appendData = $(this).val();
                    seatDetails.fetchPassengerDetails();
                } else {
                    seatDetails.removeData = $(this).val();
                    seatDetails.fetchPassengerDetails();
                }

                localStorage.setItem('seat_details', JSON.stringify(seatDetails.getData))
            })
        })
    }

    // NOTE: Saving each row data
    $("table.passenger").on('click', 'button.save', function (e) {
        let tr = $(this).closest('tr');
        let id = tr.data('id');
        let name = tr.find('input[name="name"]');
        let email = tr.find('input[name="email"]');
        let age = tr.find('input[name="age"]');


        if (!(name.val())) {
            toastr.error("Please enter a name");
            name.removeClass('is-valid').addClass('is-invalid');

            return;
        }


        if (!(email.val()) || !(validateEmail(email.val()))) {
            toastr.error("Please enter a email");
            email.removeClass('is-valid').addClass('is-invalid');

            return;
        }

        name.removeClass('is-invalid').addClass('is-valid');
        email.removeClass('is-invalid').addClass('is-valid');
        toastr.success("Passenger details has been saved!");

        // console.log(name, email, gender)
        // NOTE: Get the index of  the object using findIndex
        let objIndex = seatDetails.getData.findIndex((elem) => elem.seat === id);
        seatDetails.updateData(objIndex, {
            'name': name.val(),
            'email': email.val(),
            'age': age.val(),
        })



    })

})