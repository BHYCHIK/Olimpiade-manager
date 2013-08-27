var url = "/cgi-bin/register_person.pl";
var form_selector = "form.registration_form";

function prepare_vars() {
	window.empty_field_msg = "Заполните обязательное поле";
	window.incorrect_email = "Неверный адрес электронной почты. " +
		"Пример:&nbsp;<div class=\"sample\">sample@mail.ru</div>";
	window.correct_field_msg = "Ок";
	window.empty_field_class = "empty_field";
	window.incorrect_email_class = "incorrect_email";
	window.incorrect_login_class = "incorrect_login";
	window.correct_field_class = "ok_field";
	window.note_sign = "<span class=\"note_sign\">" +
		"&nbsp;*&nbsp;</span>";
};

var msg_type_t = {
	correct_field:    0,
	empty_field:      1,
	incorrect_email:  2,
};

function get_msg(msg_type) {
	var msg_class, msg_text;
	switch (msg_type) {
		case msg_type_t.correct_field:
			msg_text = window.correct_field_msg;
			msg_class = window.correct_field_class;
			break;
		case msg_type_t.empty_field:
			msg_text = window.empty_field_msg;
			msg_class = window.empty_field_class;
			break;
		case msg_type_t.incorrect_email:
			msg_text = window.incorrect_email;
			msg_class = window.incorrect_email_class;
			break;
		default:
			return "Error msg_type: " + msg_type;
	}
	return "<div class=\"" + msg_class + "\">" + 
			msg_text + "</div>";
}

function has_type($elem, msg_type) {
	var class_name;
	switch (msg_type) {
		case msg_type_t.correct_field:
			class_name = window.correct_field_class;
			break;
		case msg_type_t.empty_field:
			class_name = window.empty_field_class;
			break;
		case msg_type_t.incorrect_email:
			class_name = window.incorrect_email_class;
			break;
		default:
			return false;
	}
	var $row;
	if (($row = $elem.find("." + class_name)).length) // td passed
		return $row;
	if ($elem.hasClass(class_name)) // div passed
		return true;
	return false;
}

function change_msg($tr, msg_type) {
	var $td = $tr.find(".msg"),
		$div, pirate = false;
	if (!$td.length) $td = $tr;	// td already passed

	if (($div = $td.find("div")).length) {
		if (has_type($div, msg_type)) 
			pirate = true;
		else $div.remove();
	}
	if (!pirate)
		$td.append(get_msg(msg_type));
}

function remove_msg($tr) {
	var $td = $tr.find(".msg"), $div;
	if (!$td.length) $td = $tr;
	if (($div = $td.find("div")).length)
		$div.remove();
}

function prepare_table() {
    var today = new Date();
    var m = today.getMonth() + 1;
    today = today.getFullYear() + "-" + (m > 9 ? m : "0" + m) + "-" + today.getDate();
	form_selector.find("tr.required td:first-child").each(function() {
		$(this).html($(this).html() + window.note_sign); });
	form_selector.find("tr.required").append(
			"<td class=\"msg\"></td>");
	form_selector.find("tr.extra").append(
			"<td class=\"msg\"></td>");
	form_selector.find("tr.optional").append("<td></td>");
	form_selector.find("tr.other").append("<td></td>");
    form_selector.find(".send_btn").click(validate_form);
    form_selector.find(".clear_form_btn").click(clear_form);
    form_selector.find("input").keydown(validate_input);
    form_selector.find("input[type='date']").attr("value", today).attr("max", today);
}

function validate_input(e) {
    var name = $(this).attr("name");
    var text = $(this).val();
    if (name === 'email') {
        return;
    }
    if ($(this).hasClass("no_spaces") && e.which === 32) { 
        e.preventDefault();
        return;
    }
    if (name === 'phone' && e.which != 9 && (e.which < 48 || e.which > 57)) {
        e.preventDefault();
        return;
    }
}

function clear_form() {
    console.log("clear");
}

function validate_form() {
	// Empty fields at first
    var ok = true;
	form_selector.find("tr.required .input_box").each( function() {
        if (!/\S/.test($(this).val())) {
            ok = false;
            change_msg($(this).parent().parent(), msg_type_t.empty_field);
        } else {
            remove_msg($(this).parent().parent());
        }
	});
	if (!ok) return;
    
    ok = false;
    form_selector.find(".gender_radio").each( function() {
        if (ok) return;
        if ($(this)[0].checked) ok = true; });
    if (!ok) {
        change_msg(form_selector.find(".gender_radio").parent().parent().parent(),
                   msg_type_t.empty_field);
        return;
    } else {
        remove_msg(form_selector.find(".gender_radio").parent().parent().parent());
    }
    
    form_selector.find("[name='email']").each( function() {
        if (!ok) return;
        ok = /^\w[\w.\d]*@([\w\d]*\.)+[\w\d]+$/.test($(this).val());
        if (!ok) change_msg($(this).parent().parent(), msg_type_t.incorrect_email);
        else remove_msg($(this).parent().parent());
    });
    if (!ok) 
        return;

    success(form_selector);
}

function success(form) {
	var cgi_str = url + "?";
    var keys = ['first_name', 'second_name', 'surname', 'gender',
                'date_of_birth', 'address', 'phone', 'email',
                'description'];
    for (var i = 0; i < keys.length; i++) {
        var field = form.find('[name="' + keys[i] + '"]')[0];
        if (field.value != '') {
            if (keys[i] === 'gender' && !field.checked) continue;
            cgi_str += keys[i] + '=' + field.value + '&';
        }
    }
	$.getJSON(cgi_str.replace(/&$/, ""), check_results)
		.fail(function( jqxhr, textStatus, error ) {
			var err = textStatus + ', ' + error;
			console.log( "Request Failed: " + err);
		});
}

function check_results(data) {
	console.log(data);
}

window.onload = function() {
    form_selector = $(form_selector);
	prepare_vars();
	prepare_table();
};
