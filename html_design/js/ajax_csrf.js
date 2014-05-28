
// using jQuery
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
//use like this
var csrftoken = getCookie('csrftoken');
//alert( getCookie('csrftoken') );
function csrfSafeMethod(method) {
     // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//command=add or remove
function edit_memopub(cmd_, pubid_) {
	$.ajax({
		type : 'POST',
		data : {
			pubid : pubid_,
			cmd : cmd_
		},
		url : '/add_memopub/',
		dataType : 'json',
		success : function(json) {
			alert(json['pubid']);
		},
		error : function(xhr, errmsg, err) {
			//alert(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
			alert("error");
			console.log(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
		}
	});
}

	