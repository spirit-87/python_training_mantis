import string
import random

def random_username(prefix, maxlen):
    symbols = string.ascii_letters #+ string.digits + " "*5
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def test_sign_up_new_account(app):
    # проверяем, что такой пользователь зарегистрирован
    username = random_username('user_', 10)
    password = "test"
    email = username + "@localhost"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)

    # проверка, что авторизация прошла успешно
    # app.session.login(username, password)
    # assert app.session.is_logged_in_as(username)
    # app.session.logout()

    # проверка, что авторизация прошла успешно, через soap
    assert app.soap.can_login(username, password)