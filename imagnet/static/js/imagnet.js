/**
 * Created with PyCharm.
 * User: djakson
 * Date: 5/18/13
 * Time: 1:02 PM
 * To change this template use File | Settings | File Templates.
 */
var now_edit = null;
$(function(){
    $('a.upload').on('click', function(event){
        $(this).next('form').find('.uploadcare-widget-buttons-file').trigger('click');
        return false;
    });

    $('a.edit').on('click', function(event){
        now_edit = $(this).parents('.order_add');
        $('form').find('.uploadcare-widget-buttons-file').trigger('click');
        return false;
    });

}());

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(function(){

    function set_total_price(price){
        $('.total_cost strong').text(price + ' грн.');
    }

    function updatePrices(with_cost_on_delivery){
        var el_magnet_cost = $('.magnet_cost').text(),
            el_delivery_cost = $('.delivery_cost').text(),
            el_cost_on_delivery = $('.cost_on_delivery').text();
        if (with_cost_on_delivery){
            set_total_price(parseFloat(el_magnet_cost) + parseFloat(el_delivery_cost) + parseFloat(el_cost_on_delivery));
            return
        }
        set_total_price(parseFloat(el_magnet_cost) + parseFloat(el_delivery_cost));
        return
    }

    $('.order_box').on('mouseenter', '.order_magnit_shell, .overlay', function(ev){
        $(this).parent().find('.overlay').removeClass('hidden');
    }).on('mouseout', '.order_magnit_shell, .overlay', function(ev){
        $(this).parent().find('.overlay').addClass('hidden');
    });

    $('.order_box').on('click', 'a.duplicate', function(ev){
        var magnet = $(this).parents('.order_add');
        iMagnet.duplicate(magnet);
    });

    $('.order_box').on('click', 'a.delete', function(ev){
        var magnet = $(this).parents('.order_add');
        iMagnet.delete(magnet);
    });

    $('form input[name=payment_type]').on('change', function(ev){
        if ($(this).attr('value') == 'after_delivery'){
            $('.order_list .after_delivery').removeClass('hidden');
            updatePrices(true);
        }else{
            $('.order_list .after_delivery').addClass('hidden');
            updatePrices();
        }
    });
}());