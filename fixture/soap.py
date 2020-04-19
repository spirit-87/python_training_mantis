from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:

    def __init__(self,app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost:8080/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login( username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self):
        client = Client("http://localhost:8080/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        projects_array = client.service.mc_projects_get_user_accessible(self.app.config['webadmin']['username'],
                                                                        self.app.config['webadmin']['password'])
        list = []
        for item in projects_array:
            id = item ['id']
            name = item ['name']
            # статусы закомментировала, так как надо искать соответствие числового кода и названия статуса
            # status = item ['status']
            # view_status = item ['view_state']
            description = item ['description']
            list.append(Project(id=id, name=name, #status=status, view_status=view_status,
                                              description=description))

        return list



