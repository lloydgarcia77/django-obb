$(document).ready(function (e) {
    // ! validate all the details from step 1 and data types
    // ! make this a validation before submit
    // ! add validation to step 3 add validation on reload
    // ! check if a gmail
    let seat_details = localStorage.getItem('seat_details');

    validateAllDetails();

    const validateEmail = (email) => {
        return String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
    };

    
    function validateAllDetails(){
        let route = localStorage.getItem('route');
        let bus = localStorage.getItem('bus');
        let seat_details = localStorage.getItem('seat_details');
        let selectedDate = localStorage.getItem('selectedDate');
        let parsedSelectedDate = new Date(selectedDate)
        if(!(route)){
            toastr.error("Invalid Route Detected!");
            return;
        }

        if(!(bus)){
            toastr.error("Invalid Bus Detected!");
            return;
        }
 
        if(parsedSelectedDate === NaN){
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
                seat_details = seat_details.filter((e,i) => (
                    e.email && e.name && e.age && (validateEmail(e.email) && typeof parseInt(e.age) === 'number')
                )) 
            } catch (e) {
                seat_details = [];
            }

        }
    }


})