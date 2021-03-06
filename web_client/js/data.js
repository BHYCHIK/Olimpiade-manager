Data = {
    main: {
        div_class_name: 'main',
        container: 'content',
    },
    register: {
        div_class_name: 'registration_form',
        handler: Registration.build,
        container: 'content',
    },
};

Data.main.data = 'Hello!';

Data.login.data = 
'    <table>' +
'        <tr><td>Логин:</td><td><input type="text" name="u_login"></td></tr>' +
'        <tr><td>Пароль:</td><td><input type="text" name"u_passw"=""></td></tr>' +
'        <tr><td colspan="2"><div id="sign_in">' +
'            <label><input type="checkbox" checked="true" id="remember_me">Запомнить</label>' +
'            <button>Войти</button></div>' +
'        </td></tr>' +
'        <tr><td colspan="2">' +
'            <a href="/html/registration.htm">Регистрация</a>' +
'        </td></tr>' +
'    </table>';

Data.register.data = 
'    <form name="reg_form" method="post" class="registration_form"> ' +
'    <h1>Регистрация нового пользователя</h1>' +
'    <table>' +
'        <tr class="required">' +
'            <td>Имя</td>' +
'            <td colspan="2"><input type="text" name="first_name" class="input_box no_spaces"></td>' +
'        </tr>' +
'        <tr class="required">' +
'            <td>Фамилия</td>' +
'            <td colspan="2"><input type="text" name="second_name" class="input_box no_spaces"></td>' +
'        </tr>' +
'        <tr class="required">' +
'            <td>Отчество</td>' +
'            <td colspan="2"><input type="text" name="surname" class="input_box no_spaces"></td>' +
'        </tr>' +
'        <tr class="required">' +
'            <td>Пол</td>' +
'            <td><label><input type="radio" name="gender" value="male" class="gender_radio">Мужской</label></td>' +
'            <td><label><input type="radio" name="gender" value="female" class="gender_radio">Женский</label></td>' +
'        </tr>' +
'        <tr class="required">' +
'            <td>Дата рождения</td>' +
'            <td colspan="2"><input type="date" name="date_of_birth" class="input_box"></td>' +
'        </tr>' +
'        <tr class="required">' +
'            <td>Адрес</td>' +
'            <td colspan="2"><input type="text" name="address" class="input_box"></td>' +
'        </tr>' +
'        <tr class="required">' +
'            <td>Номер телефона</td>' +
'            <td colspan="2"><input type="text" name="phone" class="input_box"></td>' +
'        </tr>' +
'        <tr class="required">' +
'            <td>Адрес эл. почты</td>' +
'            <td colspan="2"><input type="email" name="email" class="input_box"></td>' +
'        </tr>' +
'        <tr class="optional">' +
'            <td>Немного о себе</td>' +
'            <td colspan="2"><textarea name="description" class="input_box"></textarea></td>' +
'        </tr>' +
'        <tr class="other">' +
'            <td colspan="3">' +
'                <div class="note"><span class="note_sign">*</span>&nbsp;Поля для ' +
'                    обязательного заполнения</div>' +
'            </td>' +
'        </tr>' +
'        <tr class="other">' +
'            <td colspan="3">' +
'                <div class="buttons">' +
'                    <input type="button" class="send_btn" value="Отправить">' +
'                    <input type="button" class="clear_form_btn" value="Очистить">' +
'                </div>' +
'            </td>' +
'        </tr>' +
'    </table>' +
'    </form>';

