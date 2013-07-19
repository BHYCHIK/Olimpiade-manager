window.onload = function() {
	$("form.registration_form").attr("action", "#");
	$("form.registration_form").attr("onsubmit", 
			"return validate_form_onsubmit(this);");
	$("form.registration_form tr.required").append(function(){
			var name = $(this).find("input").attr("name");
			var res = "<td id=\"" + name +
			"\"><div class=\"invalid_msg\" style=\"display: " +
			"none;\">Заполните обязательное поле!</div>";
			if ("u_passw_conf".indexOf(name) == 0) {
				res += "<div class=\"invalid_msg invalid_passw\" " +
					"style=\"display: none;\">Пароли не совпадают</div>"
			}
			return res + "<div class=\"valid_msg\" style=\"" +
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
	window.password_ok = true;
}

function text_changed() {
	var $tr = $(this).parent().parent();
	var f = function(cond, $tr, extra_class){
		if (!extra_class) extra_class = "";
		if (cond) { 
			$tr.find(".invalid_msg" + extra_class).css("display", "block");
			$tr.find(".valid_msg").css("display", "none");
		} else {
			$tr.find(".valid_msg").css("display", "block");
			$tr.find(".invalid_msg" + extra_class).css("display", "none");
		}
	}

	if ("u_passw_conf".indexOf($(this).attr("name")) == 0) {
		var passw = $(this).val(), pirate = false, flag = false;
		$tr.parent().find(".passw_textbox").each(function() {
			if ($(this).val() != passw) pirate = true; 
			if ($(this).val() != "") flag = true; });
		$tr.parent().find(".passw_textbox").each(function() {
			var $p = $(this).parent().parent();
			f(pirate, $p, ".invalid_passw");
			window.password_ok = !flag || !pirate;
			if (!flag) {
				f(true, $p);
				$p.find(".invalid_passw").css("display", "none");
			} else {
				$p.find(".invalid_msg:not(.invalid_passw)").css("display", "none");
			}
		});
	} else if ($tr.attr("class") == "required") {
		f($(this).val() == "", $tr);
	} else if ($(this).attr("name") == "u_email") {
		f($(this).val() != "" && 
			!/^[a-zA-Z](\w*)@[a-zA-Z](\w*)\.[a-zA-Z](\w*)$/
				.test($(this).val()), $tr);
	}
}

function validate_form_onsubmit(form) {
	var $table = $("form.registration_form tbody");
	$table.find(".required .valid_msg").each(function(){
		if ($(this).css("display") == "none") {
			$(this).parent().find(".invalid_msg").css("display", function() {
				if (!$(this).hasClass("invalid_passw") && 
					$(this).parent().children(".invalid_passw").size() &&
					$(this).parent().find(".invalid_passw").css("display") != "none") 
					return "none"; 
				else if ($(this).hasClass("invalid_passw") && window.password_ok) return "none";
				return "block";
			});
		} });

	var flag = true;
	$table.find(".invalid_msg").each(function() {
		if ($(this).css("display") != "none") flag = false; 
	});

	if (flag) success(form);

	return false;
}

function success(form) {
	alert("Success");
}
