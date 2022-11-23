$(document).ready(function (e) {

    let previousSelectedRoute = "";
    let eventData = [
        {
            "date": formatDate(localStorage.getItem('selectedDate')),
            "badge": false,
            "title": "Selected Schedule",
            "classname": "selected-date" 

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
                localStorage.setItem('selectedDate', `${selectedDate.getMonth() + 1}/${selectedDate.getDate()}/${selectedDate.getFullYear()}`);
                
                window.location.reload();
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

    let zab_cal = $("#cal-schedule").zabuto_calendar(zab_cal_settings);

    getRoutes();


    function getRoutes() {
        let form = new FormData();
        form.append('date', localStorage.getItem('selectedDate'))
        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            processData: false,
            contentType: false,
            data: form,
            type: 'POST',
            dataType: 'json',
            beforeSend: (data) => {

            },
            success: (data) => {
                if (data.is_valid) { 
                    zab_cal_settings = { ...zab_cal_settings, data: [...data.eventData, ...eventData] }; 
                    toastr.success("Routes has been loaded!");
                    $("#table-routes").find('tbody').html(data.html_routes);

                } else {
                    toastr.error(`There's an error encountered: ${data.error}`)
                }
            },
            error: (data) => {
                toastr.error("There an error on your date or route!");
            }
        }).done((data) => {
            previousSelectedRoute = localStorage.getItem('route');
            $("input:radio[name='route']").filter(`[value='${previousSelectedRoute}']`).prop('checked', true);
             
            $(zab_cal).empty().zabuto_calendar(zab_cal_settings);
        })
    }

    $("#table-routes").on("change", "input[type='radio']", function (e) {
        if ($(this).is(":checked")) {
            // scheduleData.setRoute = $(this).val();

            if (previousSelectedRoute) {
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
                        previousSelectedRoute = $(this).val();
                        $(zab_cal).empty().zabuto_calendar(zab_cal_settings);
                    } else {
                        $("input:radio[name='route']").filter(`[value='${previousSelectedRoute}']`).prop('checked', true);
    
                    }
                })
            }else{
                localStorage.setItem('route', $(this).val())
                previousSelectedRoute = $(this).val();
            }
            
        }
    })


    function formatDate(date) {
        let pDate = new Date(date);
        // NOTE YYYY-MM-DD 
        let newDate = `${pDate.getFullYear()}-${pDate.getMonth() + 1}-${pDate.getDate()}`;
        return newDate;
    }
})  