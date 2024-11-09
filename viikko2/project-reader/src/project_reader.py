import toml
from urllib import request
from project import Project  # Oletetaan, että Project-luokka on määritelty projektissa

class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # Haetaan TOML-muotoista sisältöä URL:stä
        content = request.urlopen(self._url).read().decode("utf-8")
    

        # Deserialisoi TOML-muotoista dataa
        project_data = toml.loads(content)

        # Oletetaan, että TOML-tiedostossa on osio 'tool.poetry', joka sisältää projektin tiedot
        project_info = project_data.get("tool", {}).get("poetry", {})
        dev_dependencies = project_info.get("group", {}).get("dev", {}).get("dependencies", {})
        # Muodostetaan Project-olio TOML-datan perusteella
        project = Project(
            name=project_info.get("name", "Default name"),
            description=project_info.get("description", "No description"),
            license=project_info.get("license", "No license"),  # Tässä lisätään license
            authors=project_info.get("authors", []),
            dependencies=list(project_info.get("dependencies", {}).keys()),
            dev_dependencies=list(dev_dependencies.keys())  # Lisätään kehityksenvaiheen riippuvuudet
    )
        return project

