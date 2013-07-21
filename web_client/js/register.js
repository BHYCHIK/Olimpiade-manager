var url = "/cgi-bin/register_person.pl";

function prepare_vars() {
	window.empty_field_msg = "Заполните обязательное поле";
	window.incorrect_passw = "Пароли не совпадают";
	window.incorrect_email = "Неверный адрес электронной почты. " +
		"Пример:&nbsp;<div class=\"sample\">sample@mail.ru</div>";
	window.incorrect_login = "Неверный формат логина. Логин может " +
		"состоять из цифр, букв и знака подчеркивания. Он не может " +
		"начинаться c цифры. Пример:&nbsp;<div class=\"sample\">" +
		"_sample_login_111</div>";
	window.correct_field_msg = "Ок";
	window.empty_field_class = "empty_field";
	window.incorrect_passw_class = "incorrect_passw";
	window.incorrect_email_class = "incorrect_email";
	window.incorrect_login_class = "incorrect_login";
	window.correct_field_class = "ok_field";
	window.note_sign = "<span class=\"note_sign\">" +
		"&nbsp;*&nbsp;</span>";
};

var msg_type_t = {
	correct_field:   0,
	empty_field:     1,
	incorrect_passw: 2,
	incorrect_email: 3,
	incorrect_login: 4
};
var form_selector = "form.registration_form";

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
		case msg_type_t.incorrect_passw:
			msg_text = window.incorrect_passw;
			msg_class = window.incorrect_passw_class;
			break;
		case msg_type_t.incorrect_email:
			msg_text = window.incorrect_email;
			msg_class = window.incorrect_email_class;
			break;
		case msg_type_t.incorrect_login:
			msg_text = window.incorrect_login;
			msg_class = window.incorrect_login_class;
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
		case msg_type_t.incorrect_passw:
			class_name = window.incorrect_passw_class;
			break;
		case msg_type_t.incorrect_email:
			class_name = window.incorrect_email_class;
			break;
		case msg_type_t.incorrect_login:
			class_name = window.incorrect_login_class;
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
	$(form_selector + " tr.required td:first-child")
		.each(function() {
			$(this).html($(this).html() + window.note_sign);
		});
	$(form_selector + " tr.required").append(
			"<td class=\"msg\"></td>");
	$(form_selector + " tr.extra").append(
			"<td class=\"msg\"></td>");
	$(form_selector + " tr.optional").append("<td></td>");
	$(form_selector + " tr.other").append("<td></td>");
	$(form_selector).attr("onsubmit",
		"if (!validate_form(this)) clear_passw(this); return false;");
	$(form_selector + " input").change(validate_input);
}

function validate_passw($tr) {
	var selector = form_selector + " tr.required>td>.passw_textbox";
	var passwords = [];
	$(selector).each(function() {
		if ($(this).val() != "") passwords.push($(this).val());
	});
	var msg = -1;
	if (passwords.length == 0) 
		msg = msg_type_t.empty_field;
	else if (passwords[0] != passwords[1])
		msg = msg_type_t.incorrect_passw;
	else
		msg = msg_type_t.correct_field;
	$(selector).each(function() {
		change_msg($(this).parent().parent(), msg); 
	});
}

function validate_input(e) {
	var $tr = $(this).parent().parent();
	var passw_mask = "u_passw_conf";
	var pirate = true;
	var msg = msg_type_t.correct_field;
	if ($tr.attr("class") == "required" && 
		$(this).val() == "" && 
		passw_mask.indexOf($(this).attr("name")) != 0) {
		msg = msg_type_t.empty_field;
	} else if (passw_mask.indexOf($(this).attr("name")) == 0) {
		validate_passw($tr);
		pirate = false;
	} else if ($(this).attr("name") == "u_login") {
		if (!/[a-zA-Z_][\w_]*/.test($(this).val()))
			msg = msg_type_t.incorrect_login;
	} else if ($(this).attr("name") == "u_email") {
		var regexp = /^[\w\.\-_]+@([a-zA-Z_]\w*\.)+[a-zA-Z_](\w*)$/;
		if ($(this).val() != "") {
			if (!regexp.test($(this).val()))
				msg = msg_type_t.incorrect_email;
		} else {
			pirate = false;
			remove_msg($tr);
		}
	}
	if (pirate)
		change_msg($tr, msg);
}

function validate_form(form) {
	var ok = true;

	// Ampty fields at first
	$(form_selector + " tr.required>td.msg:empty").each( function() {
		ok = false;
		change_msg($(this).parent(), msg_type_t.empty_field);
	});
	if (!ok) return ok;

	// Then -- incorrect required fields
	$(form_selector + " tr.required>td.msg>div").each( function() {
		if (!$(this).hasClass(window.correct_field_class)) ok = false;
	});
	if (!ok) return ok;

	// At last -- other incorrect fields
	$(form_selector + " tr.extra>td.msg").each( function() {
		if (!($(this).is(":empty") || 
				$(this).find("div.ok_field").length != 0))
			ok = false;
	});
	if (ok)
		success(form);
	return ok;
}

function clear_passw(form) {
	form.u_passw.value = "";
	form.u_passw_conf.value = "";
	$(form_selector + " tr.required>td>input.passw_textbox").each(
		function() { 
		change_msg($(this).parent().parent(), msg_type_t.empty_field); 
	});
}

function success(form) {
	var cgi_str = url + "?";
	for (key in form) if (form[key] && /^u_/.test(form[key].name)) {
		if (form[key].value != "") {
			var f_key = form[key].name, f_value = form[key].value;
			if (f_key === "u_passw_conf") continue;
			if (f_key === "u_sex" && !form[key].checked) continue;
			cgi_str += f_key + "=" + f_value + "&";
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
	prepare_vars();
	prepare_table();
};
