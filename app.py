from PowerFlask import create_app

# Cria a instância do aplicativo Flask
# A função create_app é responsável por configurar e inicializar o aplicativo Flask,
# incluindo a configuração de Blueprints e extensões utilizadas no projeto.
app = create_app()

# Configura o logging
# O logging.basicConfig define o nível de log como DEBUG, o que significa que todas as mensagens
# de log a partir deste nível serão capturadas. Isso é útil para depuração e monitoramento do aplicativo.
import logging
logging.basicConfig(level=logging.DEBUG)

# Executa o aplicativo
# O bloco abaixo verifica se o arquivo está sendo executado diretamente (e não importado como um módulo),
# e, se for o caso, inicia o servidor Flask na porta 5000 com o modo de depuração ativado.
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
