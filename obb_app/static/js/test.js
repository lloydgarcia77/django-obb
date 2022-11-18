function isToday(date){
    const today = new Date();

    if (today.toDateString() === date.toDateString()){
        return true;
    }
    return false;

}

function convert12Hourseto24Hours(uftime){
    
    const [time, modifier] = uftime.trim().split(' ');
    const [hours, mins] = time.split(":");

  
    if(modifier.toLowerCase() === 'pm'){
        return parseInt(hours) + 12;
    }

    return parseInt(hours);
}

const time = "8:00 AM - 08:00 AM";
let lastHour = time.split("-")[1];
const dateToday = new Date();
 

let h24f = convert12Hourseto24Hours(lastHour);
dateToday.setHours(0,0,0)
dateToday.setHours(h24f)
console.log(dateToday.toTimeString())