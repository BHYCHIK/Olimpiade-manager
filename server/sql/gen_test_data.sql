INSERT INTO iu7_step.person(first_name, second_name, surname, gender, email, date_of_birth, description, address, phone) VALUES
    ('Иван', 'Валерьевич', 'Ремень', 'male', 'remen@ya.ru', '1990-01-01', 'Студент ИУ7-73', 'Зеленоград, ул. Фучика д.73', '89261600768'),
    ('Петр', 'Петрович', 'Лысков', 'male', 'remen@ya.ru', '1990-01-01', 'Студент ИУ7-73', 'Зеленоград, ул. Фучика д.73', '89261600768'),
    ('Олег', 'Петрович', 'Исайкин', 'male', 'remen@ya.ru', '1990-01-01', 'Студент ИУ7-73', 'Зеленоград, ул. Фучика д.73', '89261600768'),
    ('Денис', 'Сергеевич', 'Исаев', 'male', 'idenx@ya.ru', '1993-01-01', 'Студент ИУ7-73', 'Москва, ул. Басманная д.4', '89269072780');

INSERT INTO iu7_step.account(login, password_hash, person_id, admin_priv) VALUES
    ('remen', md5('123123a'), 1, 1),
    ('denis', md5('123'), 2, 1);

INSERT INTO iu7_step.city_type(short_title, full_title) VALUES
    ('Город', 'Город'),
    ('Деревня', 'Деревня');

INSERT INTO iu7_step.school_type(short_title, full_title) VALUES
    ('Школа', 'Школа'),
    ('Гимназия', 'Гимназия');

INSERT INTO iu7_step.criteria_title(short_name, full_name) VALUES
    ('Актуальность', 'Насколько работа актуальна'),
    ('Качество', 'Качество выполненной работы'),
    ('Самостоятельность', 'Насколько ученик самостоятелньо выполнил работу');

INSERT INTO iu7_step.city(name, city_type_id) VALUES
    ('Москва', 1),
    ('Санкт-Петербург', 1);

INSERT INTO iu7_step.competition(year) VALUES
    (2010),
    (2011),
    (2012),
    (2013),
    (2014);

INSERT INTO iu7_step.role(person_id, competition_id, role) VALUES
    (1, 1, 'participant'),
    (2, 1, 'participant'),
    (3, 1, 'expert'),
    (1, 2, 'participant'),
    (2, 2, 'participant'),
    (2, 2, 'participant');

INSERT INTO iu7_step.school(title, number, address, city_id, type_id) VALUES
    ('Гимназия имени Ломоносова', NULL, 'ул. Ленина, д.6', 2, 1),
    (NULL, 56, 'ул. Комсомольская, д.6', 1, 2);
