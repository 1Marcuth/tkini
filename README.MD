# TkIni

TkIni é uma biblioteca construída em cima do Tkinter para simplificar a criação de GUIs em Python. Ele permite a leitura de estilos e configurações de widgets a partir de arquivos de texto e oferece uma interface para definir eventos personalizados e manipuladores de eventos para widgets.

## Funcionalidades

- Leitura de estilos de widgets a partir de um arquivo de configuração (`styles.ini`).
- Leitura de configurações de widgets a partir de um arquivo de configuração (`widgets.ini`).
- Definição de eventos personalizados para widgets.
- Definição de manipuladores de eventos para widgets.
- Atualização dinâmica dos estilos e configurações dos widgets.

## Como Usar

1. Instale a biblioteca via pip:

```bash
pip install tkini
```

2. Importe a biblioteca em seu código:

```py
from tkini import Window
```

3. Crie uma instância da classe Window e utilize seus métodos para configurar a interface gráfica:

```py
window = Window()

window.title("Minha Aplicação")
window.geometry("400x250")
window.use_styles_file("styles.ini")
window.use_widgets_file("widgets.ini")

window.mainloop()
```


## Como Contribuir

Se você quiser contribuir com este projeto, siga estas etapas:

1. Crie um fork este repositório.
2. Crie um branch para a sua feature (`git checkout -b feature/MinhaFeature`).
3. Faça commit das suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça push para o branch (`git push origin feature/MinhaFeature`).
5. Crie um novo Pull Request.

## Autor

Marcuth (@1marcuth)

## Licença

Este projeto está licenciado sob a Licença MIT.