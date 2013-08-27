var Registration = {};

Registration.url = "/cgi-bin/register_person.pl";
Registration.form_selector = "form.registration_form";

Registration.prepare_vars = function () {
	Registration.empty_field_msg = "Заполните обязательное поле";
	Registration.incorrect_email = "Неверный адрес электронной почты. " +
		"Пример:&nbsp;<div class=\"sample\">sample@mail.ru</div>";
	Registration.correct_field_msg = "Ок";
	Registration.empty_field_class = "empty_field";
	Registration.incorrect_email_class = "incorrect_email";
	Registration.incorrect_login_class = "incorrect_login";
	Registration.correct_field_class = "ok_field";
	Registration.note_sign = "<span class=\"note_sign\">" +
		"&nbsp;*&nbsp;</span>";
};

Registration.msg_type_t = {
	correct_field:    0,
	empty_field:      1,
	incorrect_email:  2,
};

Registration.keys = ['first_name', 'second_name', 'surname', 'gender',
                     'date_of_birth', 'address', 'phone', 'email',
                     'description'];

Registration.get_msg = function (msg_type) {
	var msg_class, msg_text;
	switch (msg_type) {
		case Registration.msg_type_t.correct_field:
			msg_text = Registration.correct_field_msg;
			msg_class = Registration.correct_field_class;
			break;
		case Registration.msg_type_t.empty_field:
			msg_text = Registration.empty_field_msg;
			msg_class = Registration.empty_field_class;
			break;
		case Registration.msg_type_t.incorrect_email:
			msg_text = Registration.incorrect_email;
			msg_class = Registration.incorrect_email_class;
			break;
		default:
			return "Error msg_type: " + msg_type;
	}
	return "<div class=\"" + msg_class + "\">" + 
			msg_text + "</div>";
}

Registration.has_type = function ($elem, msg_type) {
	var class_name;
	switch (msg_type) {
		case Registration.msg_type_t.correct_field:
			class_name = Registration.correct_field_class;
			break;
		case Registration.msg_type_t.empty_field:
			class_name = Registration.empty_field_class;
			break;
		case Registration.msg_type_t.incorrect_email:
			class_name = Registration.incorrect_email_class;
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

Registration.change_msg = function ($tr, msg_type) {
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

Registration.remove_msg = function ($tr) {
	var $td = $tr.find(".msg"), $div;
	if (!$td.length) $td = $tr;
	if (($div = $td.find("div")).length)
		$div.remove();
}

Registration.prepare_table = function () {
    var today = new Date();
    var m = today.getMonth() + 1;
    today = today.getFullYear() + "-" + (m > 9 ? m : "0" + m) + "-" + today.getDate();
	Registration.form_selector.find("tr.required td:first-child").each(function() {
		$(this).html($(this).html() + Registration.note_sign); });
	Registration.form_selector.find("tr.required").append(
			"<td class=\"msg\"></td>");
	Registration.form_selector.find("tr.extra").append(
			"<td class=\"msg\"></td>");
	Registration.form_selector.find("tr.optional").append("<td></td>");
	Registration.form_selector.find("tr.other").append("<td></td>");
    Registration.form_selector.find(".send_btn").click(Registration.validate_form);
    Registration.form_selector.find(".clear_form_btn").click(Registration.clear_form);
    Registration.form_selector.find("input").keydown(Registration.validate_input);
    Registration.form_selector.find("input[type='date']").attr("value", today).attr("max", today);
}

Registration.validate_input = function (e) {
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

Registration.clear_form = function () {
    var keys = Registration.keys;
    for (var i = 0; i < keys.length; i++) {
        var field = form.find('[name="' + keys[i] + '"]');
        if (keys[i] === 'gender') {
            field.each(function () { $(this)[0].checked = false; });
        } else {
            field[0].val('');
        }
    }
}

Registration.validate_form = function () {
	// Empty fields at first
    var ok = true;
	Registration.form_selector.find("tr.required .input_box").each( function() {
        if (!/\S/.test($(this).val())) {
            ok = false;
            Registration.change_msg($(this).parent().parent(), Registration.msg_type_t.empty_field);
        } else {
            Registration.remove_msg($(this).parent().parent());
        }
	});
	if (!ok) return;
    
    ok = false;
    Registration.form_selector.find(".gender_radio").each( function() {
        if (ok) return;
        if ($(this)[0].checked) ok = true; });
    if (!ok) {
        change_msg(Registration.form_selector.find(".gender_radio").parent().parent().parent(),
                   Registration.msg_type_t.empty_field);
        return;
    } else {
        remove_msg(Registration.form_selector.find(".gender_radio").parent().parent().parent());
    }
    
    Registration.form_selector.find("[name='email']").each( function() {
        if (!ok) return;
        ok = /^\w[\w.\d]*@([\w\d]*\.)+[\w\d]+$/.test($(this).val());
        if (!ok) Registration.change_msg($(this).parent().parent(), Registration.msg_type_t.incorrect_email);
        else Registration.remove_msg($(this).parent().parent());
    });
    if (!ok) 
        return;

    success(Registration.form_selector);
}

Registration.success = function (form) {
	var cgi_str = url + "?";
    var keys = Registration.keys;
    for (var i = 0; i < keys.length; i++) {
        var field = form.find('[name="' + keys[i] + '"]')[0];
        if (field.value != '') {
            if (keys[i] === 'gender' && !field.checked) continue;
            cgi_str += keys[i] + '=' + field.value + '&';
        }
    }
    console.log(cgi_str);
	$.getJSON(cgi_str.replace(/&$/, ""), check_results)
		.fail(function( jqxhr, textStatus, error ) {
			var err = textStatus + ', ' + error;
			console.log( "Request Failed: " + err);
		});
}

Registration.check_results = function (data) {
	console.log(data);
}

Registration.show = function () {
    Registration.form_selector = $(Registration.form_selector);
	Registration.prepare_vars();
	Registration.prepare_table();
};
