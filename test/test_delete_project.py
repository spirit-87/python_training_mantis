# -*- coding: utf-8 -*-
from model.project import Project
import random
import string

def test_delete_some_project(app):
    old_projects = app.project.get_project_list()
    if len(old_projects) == 0:
        new_project = Project(name=random_string("Project_", 5), status="stable", view_status="private",
                              description=random_string("Description", 10))
         # проверка, что имя нового проекта не совпадает с уже имеющимися
        for project in old_projects:
            assert project.name != new_project.name
        app.project.create(new_project)
        old_projects = app.project.get_project_list()

    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.project.get_project_list()
    old_projects.remove(project)

    assert sorted(old_projects, key = Project.id_or_max) == sorted(new_projects, key = Project.id_or_max)

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])
