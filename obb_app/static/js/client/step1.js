$(document).ready(function (e) {

    let eventData = [
        {
            "date": formatDate(localStorage.getItem('selectedDate')),
            "badge": false,
            "title": "Selected Schedule",
            "classname": "selected-date"
            // "classname":"full-schedule-date"

        }

    ]


    let zab_cal_settings = {
        legend: [
            { type: "block", label: "With Scheduled" },
            { type: "block", label: "Selected Date", classname: "selected-date" },
            { type: "block", label: "Full Schedule", classname: "full-schedule-date" },
            { type: "block", label: "Today", classname: "current-date" },
        ],
        action: function () {
            var date = $("#" + this.id).data("date");
            var selectedDate = new Date(date);
            var dateNow = new Date(Date.now());
            selectedDate.setHours(0, 0, 0, 0);
            dateNow.setHours(0, 0, 0, 0);
            $(this).closest('table.table').find('.selected-date').removeClass('selected-date');
            $(this).find('div').addClass("selected-date");

            if (selectedDate < dateNow) {
                // appointmentData.setDate = selectedDate;
                toastr.error("Invalid Date!");
            } else {
                localStorage.setItem('selectedDate', selectedDate.toISOString());
                // scheduleData.setDate = selectedDate; 
                // loadSchedules();
            }
        },
        action_nav: function () {
            var id = this.id;
            var nav = $("#" + id).data("navigation");
            var to = $("#" + id).data("to");
        },
        data: eventData,
        cell_border: true,
        today: true,
        show_days: false,
        weekstartson: 0,
        nav_icon: {
            prev: '<i class="fa fa-chevron-circle-left"></i>',
            next: '<i class="fa fa-chevron-circle-right"></i>'
        }
    };

    $("#table-routes").on("change", "input[type='radio']", function (e) {
        if ($(this).is(":checked")) {
            // scheduleData.setRoute = $(this).val();
            Swal.fire({
                title: 'Do you want to change route?',
                html: `By changing routes all of your details setted on the current route will be <b class="text-danger">deleted</b>!`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Change Route'
            }).then((result) => {
                if (result.isConfirmed) {

                    localStorage.clear();
                    localStorage.setItem('route', $(this).val())

                }
            })
        }
    })

    let zab_cal = $("#cal-schedule").zabuto_calendar(zab_cal_settings);

    $("input:radio[name='route']").filter(`[value='${localStorage.getItem('route')}']`).prop('checked', true)
    function formatDate(date) {
        let pDate = new Date(date);
        // NOTE YYYY-MM-DD 
        let newDate = `${pDate.getFullYear()}-${pDate.getMonth() + 1}-${pDate.getDate()}`;
        return newDate;
    }
})  