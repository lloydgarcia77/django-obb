$(document).ready(function (e) {
    
    
    let slideNo = 0;
    const slideItem = $(".slideshow-container").find('.slide-item');
    const slideItemArray = slideItem.toArray();

    // NOTE: hide slides
    slideItem.css("display", "none");


    showSlideShow();

    var faq = document.getElementsByClassName("faq-page");
    var i;

    for (i = 0; i < faq.length; i++) {
        faq[i].addEventListener("click", function () {
            /* Toggle between adding and removing the "active" class,
            to highlight the button that controls the panel */
            this.classList.toggle("active");
            /* Toggle between hiding and showing the active panel */
            var body = this.nextElementSibling;
            if (body.style.display === "block") {
                body.style.display = "none";
            } else {
                body.style.display = "block";
            }
        });
    }
    function showSlideShow() {
        slideItem.css("display", "none");
        $(slideItemArray[slideNo]).fadeIn(500);

        if (slideNo < (slideItemArray.length-1)){
            slideNo++; 
        }else{
            slideNo=0;
        }
 

        setTimeout( showSlideShow, 3000);



    }

 
})