from selenium.webdriver.support.ui import Select
from model.project import Project
import re


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_newproject_page(self):
        wd = self.app.wd

        if not wd.current_url.endswith("/manage_proj_create_page.php") > 0:
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()

    def create(self, project):
        wd = self.app.wd
        self.open_newproject_page()
        self.change_project_info(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        # self.return_to_groups_page()
        self.project_cashe = None
        # self.app.return_to_home_page()


    def change_project_info(self, project):
        wd = self.app.wd
        # fill project form
        self.change_field_value("name", project.name)
        self.change_statuses_value("status", project.status)
        if project.IGC == False:
            self.find_element_by_name("inherit_global").click()
        self.change_statuses_value("view_state", project.view_status)
        self.change_field_value("description", project.description)

    def change_statuses_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(text)


    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def open_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    project_cashe = None

    def get_project_list(self):
        # будем возвращать кеш.значение, если оно доступно
        # надо проверять, валидно ли значение кеша (в случае изменений в группах, надо обновлят кеш - сброс кеша в методах,
        # изменяющих список групп)
        if self.project_cashe is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cashe = []
            # rows = wd.find_elements_by_xpath("//table[tr[starts-with(@class,'row')]")
            rows = wd.find_elements_by_css_selector("table.width100 tr[class^='row-'")
            # удаляю первую строку - шапку таблицы
            rows.pop(0)
            for row in rows:
                cells = row.find_elements_by_tag_name("td")
                id = re.search("=(\d+)", cells[0].find_element_by_tag_name("a").get_attribute("href"))
                name = cells[0].find_element_by_tag_name("a").text
                status = cells[1].text
                view_status = cells[3].text
                description = cells[4].text
                self.project_cashe.append(Project(id = id.group(1), name=name,  status = status, view_status = view_status,
                                                  description = description))

        return list(self.project_cashe)


    def select_project_by_id(self, id):
        wd = self.app.wd
        id_string = "manage_proj_edit_page.php?project_id="+str(id)
        # select first group = click first checkbox
        wd.find_element_by_css_selector("a[href='%s']" % id_string).click()

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_projects_page()
        self.select_project_by_id(id)
        # submit group deletion
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()

        self.project_cashe = None

