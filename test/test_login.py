
# def test_login(app):
#     app.session.login("administrator","root")
#     assert app.session.is_logged_in_as("administrator")


def test_login(app):
    username ="administrator"
    password ="root"
    app.session.login(username, password)
    # assert app.soap.can_login(username, password)
    assert app.session.is_logged_in_as(username)

