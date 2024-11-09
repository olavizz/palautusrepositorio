class Project:
    def __init__(self, name, description, license, authors, dependencies, dev_dependencies):
        self.name = name
        self.description = description
        self.license = license
        self.authors = authors
        self.dependencies = dependencies
        self.dev_dependencies = dev_dependencies

    def __repr__(self):
        return f"Name: {self.name}\n" \
               f"Description: {self.description}\n" \
               f"License: {self.license}\n" \
               f"Authors:\n" + "\n".join(f"- {author}" for author in self.authors) + "\n" \
               f"Dependencies:\n" + "\n".join(f"- {dep}" for dep in self.dependencies) + "\n" \
               f"Development dependencies:\n" + "\n".join(f"- {dev_dep}" for dev_dep in self.dev_dependencies)