# Проект по Дизајн на Интеракцијата Човек Компјутер - 2022/23 

### Django веб апликација за купување и продавање на видео игри ####


## 1.Dependencies
За да се стартува апликацијата потребни се 

`Django > 4.2.2`<br>
`Pillow`<br>
`Django-filter`<br>
`Django-star-ratings`

Пред почетокот може да се искористи командата `pip freeze -r requirements.txt` за да се инсталираат потребните dependencies.

## 2. Стартување на апликацијата ##
Со `manage.py runserver [IP address]:[PORT]` се стартува серверот. <br>

Постои предефиниран `superadmin` профил на кој може да се пристапи со 

`username:admin` <br>
`password:admin`

## 3. Користење на апликацијата ##

При стартување на апликацијата на `/` се прикажува почетната страна на апликацијата од каде што можеме да пристапиме на сите можности кои ги нуди.

Тоа вклучува:
* Креирање на сопствени кориснички профили
* Разгледување на целиот каталог на игри
* Филтрирање на каталогот во однос на име, име на развивач, tag-ови и сортирање на истата листа
* Прикажување на детални информации и слики и видеа за игрите
* Купување на игри (во моментот прикажана е dummy страна без валидација на податоците за платежната картичка)
* Симнување на игри
* Поставување на сопствени игри
* Рецензија на игри

и друго.

При поставување на играта таа треба прво да биде валидирана од администраторите на страната, тоа се прави со пристапување на admin панелот од Django на `/admin/`, прегледување на играта и поставување на променливата `Validated = True`


