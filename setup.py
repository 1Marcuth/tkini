from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as file:
    readme_content = file.read()

setup(
    name = "tkini",
    version = "0.1.4",
    packages = find_packages(),
    install_requires = [ "pydantic" ],
    python_requires = ">=3.11",
    author = "Marcuth",
    author_email = "example@gmail.com",
    description = "TkIni é uma biblioteca construída em cima do Tkinter para simplificar a criação de GUIs em Python. Ele permite a leitura de estilos e configurações de widgets a partir de arquivos de texto e oferece uma interface para definir eventos personalizados e manipuladores de eventos para widgets.",
    long_description = readme_content,
    long_description_content_type = "text/markdown",
    url = "https://github.com/1marcuth/tkini"
)
