$(document).ready(function() {
    $('.nav-toggler').click(function() {
        $(this).toggleClass('change');
        $('.nav-items').stop().slideToggle(500);
    });

    $('#search-btn').click(function() {
        $('#search-btn > i').toggleClass('fa-search fa-times');
        $('#search-dropdown').toggle();
        $('body').toggleClass('no-scroll');
    });

    //Scroll Progress Bar
    $(window).scroll(() => {
        let scrollTop = $(window).scrollTop();
        let docHeight = $(document).height();
        let winHeight = $(window).height();
        let scrollPercent = (scrollTop) / (docHeight - winHeight);
        let scrollPercentRounded = Math.round(scrollPercent*100);
        //console.log(scrollPercentRounded);
        $('#scroll-progress-bar').css('width', scrollPercentRounded+'%');
    });

    //Make div clicakble
    $('.card').click(function() {
        window.location = $(this).find("a").attr("href"); 
        return false;
    })
})

// Share links
let shareFacebook = function() {
    let shareUrl = "https://www.facebook.com/sharer/sharer.php?u="+window.location.href;
    window.open(shareUrl);
}

let shareTwitter = function() {
    let shareUrl = "https://twitter.com/home?status="+window.location.href;
    window.open(shareUrl);
}

let sharePinterest = function() {
    let shareUrl = "https://pinterest.com/pin/create/button/?url="+window.location.href+"/&media=&description=";
    window.open(shareUrl);
}

let shareGoogle = function() {
    let shareUrl = "mailto:info@example.com?&subject=&body="+window.location.href;
    window.open(shareUrl);
}

// Lazy load image
const images = document.querySelectorAll("img[data-src]");

let preloadImage = function(img) {
    const src = img.getAttribute("data-src");
    if (!src)
        return;
    
    img.src = src;
}

const imgOptions = {};

const imgObserver = new IntersectionObserver((entries, imgObserver) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting)
            return;
        else {
            preloadImage(entry.target);
            imgObserver.unobserve(entry.target);
        }
    })
}, imgOptions);

images.forEach(image => {
    imgObserver.observe(image);
})

