function kita(){ alert("kita");}

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
			//alert(json['pubid']);
		},
		error : function(xhr, errmsg, err) {
			//alert(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
			//alert("error");
			console.log(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
		}
	});
}

function edit_memovideo(cmd_, videoid_) {
	$.ajax({
		type : 'POST',
		data : {
			videoid : videoid_,
			cmd : cmd_
		},
		url : '/handle_ajax/',
		dataType : 'json',
		success : function(json) {
			//alert(json['videoid']);
		},
		error : function(xhr, errmsg, err) {
			//alert(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
			//alert("error");
			console.log(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
		}
	});
}

function edit_watch(cmd_, username_){
	$.ajax({
		type : 'POST',
		data : {
			username : username_,
			cmd : cmd_
		},
		url : '/handle_ajax/',
		dataType : 'json',
		success : function(json) {
			//alert(json['username']);
		},
		error : function(xhr, errmsg, err) {
			//alert(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
			//alert("error");
			console.log(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
		}
	});	
}

function edit_mypub(cmd_, pubid_){
	$.ajax({
		type : 'POST',
		data : {
			pubid : pubid_,
			cmd : cmd_
		},
		url : '/handle_ajax/',
		dataType : 'json',
		success : function(json) {
			//alert(json['pubid']);
		},
		error : function(xhr, errmsg, err) {
			//alert(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
			//alert("error");
			console.log(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
		}
	});		
}

function edit_video(cmd_, videoid_, pubid_){
	
	alert("hoge" + cmd_ + "\n" + videoid_ + "\n" + pubid_);
	$.ajax({
		type : 'POST',
		data : {
			videoid : videoid_,
			cmd : cmd_,
			pubid: pubid_
		},
		url : '/handle_ajax/',
		dataType : 'json',
		success : function(json) {
			alert(json['videoid'] + ": " + json['pubid']);
		},
		error : function(xhr, errmsg, err) {
			//alert(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
			//alert("error");
			console.log(xhr.status + ": " + xhr.responseText + '/ ' + errmsg + '/ ' + err);
		}
	});	
	
}

function kita(){
	alert("hello kita");
}
	