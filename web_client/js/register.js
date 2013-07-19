window.onload = function() {
	$("form.registration_form").attr("action", "#");
	$("form.registration_form").attr("onsubmit", 
			"return validate_form_onsubmit(this);");
	$("form.registration_form tr.required").append(function(){
			return "<td id=\"" +
			$(this).find("input").attr("name") +
			"\"><div class=\"invalid_msg\" style=\"display: " +
			"none;\">Заполните обязательное поле!</div>" +
			"<div class=\"valid_msg\" style=\"" +
			"display: none;\">Ок</div></td>"; });
	$("form.registration_form tr.extra").append(function(){
			return "<td id=\"email_textbox\"><div class=\"" +
			"invalid_msg\" style=\"display: none;\">" +
			"Неверный формат адреса. Пример:" +
			"<div class=\"email_sample\">" +
			"qwerty@mail.ru</div></div><div class=\"" +
			"valid_msg\" style=\"display: none;\">Ок</div></td>";});
	$("form.registration_form tr.optional").append("<td></td>");
	$("form.registration_form tr.required input").
		change(text_changed);
	$("form.registration_form tr.extra input").
		change(text_changed);
}

function text_changed() {
	var $tr = $(this).parent().parent();
	var f = function(cond){
		if (cond) { 
			$tr.find(".invalid_msg").css("display", "block");
			$tr.find(".valid_msg").css("display", "none");
		} else {
			$tr.find(".valid_msg").css("display", "block");
			$tr.find(".invalid_msg").css("display", "none");
		}
	}
	if ($tr.attr("class") == "required")
		f($(this).val() == "");
	else if ($(this).attr("name") == "u_email") 
		f($(this).val() != "" && 
			!/^[a-zA-Z](\w*)@[a-zA-Z](\w*)\.[a-zA-Z](\w*)/
				.test($(this).val()));
}

function validate_form_onsubmit(form) {
	var $table = $("form.registration_form tbody");
	$table.find(".required .valid_msg").each(function(){
		if ($(this).css("display") == "none") {
			$(this).parent().find(".invalid_msg").
				css("display", "block");
		}
	});
	
	if (form.u_passw.value() != form.u_passw_conf.value()) {
		// invalid passw
	}

	var flag = true;
	$table.find(".invalid_msg").each(function(){
		if ($(this).css("display") != "none") flag = false; });

	if (flag) success(form);

	return false;
}

function success(form) {
	alert("Success");
}
