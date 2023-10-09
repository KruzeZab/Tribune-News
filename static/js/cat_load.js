$(document).ready(function() {
    let start, end;
    start = 25;
    end = 35;
    var flag = true;
    //Ajax Load images
    $(window).scroll(function() {
        if( ($(window).scrollTop() >= $(document).height() - $(window).height() - 400) && flag) {
            $.ajax({
                url: '/cat-show-content/',
                type: 'GET',
                async: false,
                data: {
                    'start': start,
                    'end': end,
                    'cat': window.location.pathname.split('/')[2]
                },
                beforeSend: function() {
                    $('#main-list').append('<h2 id="load-icon">Loading...</h2>');
                },
                success: function(data) {
                    content = $.trim(data);
                    if (content!='True') {
                        $('#main-list').append(content);
                        console.log('yes');
                    }
                    else
                        flag = false;
                },
                complete: function() {
                    start=end+1;
                    end+=start;
                   $('#load-icon').remove();
                }
            })
        }
    })
})