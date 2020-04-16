# -*- coding: utf-8 -*-
from model.project import Project
import random
import string

def test_add_project(app):
    # statuses: development, release, stable, obsolete
    # view_statuses: public, private
    new_project = Project (name=random_string("Project_", 5), status="stable", view_status="private",
                           description=random_string("Description", 10))
    old_projects = app.project.get_project_list()

    # проверка, что имя нового проекта не совпадает с уже имеющимися
    for project in old_projects:
        assert project.name != new_project.name

    app.project.create(new_project)
    new_projects = app.project.get_project_list()
    old_projects.append(new_project)
    assert sorted(old_projects, key = Project.id_or_max) == sorted(new_projects, key = Project.id_or_max)

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])