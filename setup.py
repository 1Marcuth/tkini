from setuptools import setup, find_packages

setup(
    name = "tkini",
    version = "0.1.3",
    packages = find_packages(),
    install_requires = [ "pydantic" ],
    python_requires = ">=3.11",
    author = "Marcuth",
    author_email = "marcuth2006@gmail.com",
    description = "TkIni é uma biblioteca construída em cima do Tkinter para simplificar a criação de GUIs em Python. Ele permite a leitura de estilos e configurações de widgets a partir de arquivos de texto e oferece uma interface para definir eventos personalizados e manipuladores de eventos para widgets.",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/1marcuth/tkini"
)
