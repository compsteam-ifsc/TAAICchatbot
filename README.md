# TAAICchatbot

Este projeto abriga os arquivos de configuração e o código-fonte responsável por compilar o modelo do chatbot para o projeto RASA.

Para ver o repositório da página web para interação com o chatbot, acesse o repositório rasa-frontend.

Estrutura de arquivos
/	
domain.yml	Define o domínio do chatbot, incluindo intenções, entidades e respostas de ações.
config.yml	Especifica as configurações do modelo RASA, como o pipeline de processamento de linguagem natural.
endpoints.yml	Contém informações sobre os endpoints, como o servidor do modelo e o servidor de ações.
credentials.yml	Armazena credenciais para serviços externos, como APIs ou canais de mensagens.
data/	Diretório que contém dados de treinamento e regras para o modelo.
- nlu.yml	Exemplos de treinamento para o processamento de linguagem natural (frases reais).
- stories.yml	Contém "histórias" de exemplo para treinar o modelo a seguir fluxos de conversação.
- rules.yml	Define regras de conversação para orientar o comportamento do chatbot.
actions/	Diretório que contém o código fonte para ações personalizadas do chatbot.
- actions.py	Define as ações personalizadas que o chatbot pode realizar.
Como desenvolver
Primeiro, abra o projeto em um editor de código fonte e edite os arquivos da maneira necessária. Certifique-se de que você tem o framework Rasa Open Source instalado e a versão correta do Python em sua máquina. Dentro do diretório do projeto, no Terminal, você pode executar o seguinte:

Para treinar o modelo usando os dados de treinamento definidos em data/

rasa train
Para iniciar uma sessão simples de conversa para testar o comportamento do chatbot

rasa shell
Para iniciar uma sessão interativa de conversa para testar de debugar o comportamento do chatbot

rasa interactive
Sempre que estiver conversando com o chatbot e precisar executar uma ação de script, certifique-se de iniciar o servidor de ações.

Customizando respostas
Para customizar as respostas do chatbot, você deve editar o arquivo domain.yml. Caso queira implementar uma ação customizada em Python (que cheque algum tipo de serviço externo ou tenha uma lógica própria), adicione uma classe no arquivo actions/actions.py. Para mais informações, veja este documento.

Rodar o chatbot
Para iniciar uma sessão do chatbot que o exponha para os serviços externos (definidos em endpoints.yml), você pode rodar o seguinte comando:

rasa run -m models --enable-api --cors "*" --debug -p 5005
No entanto, vale lembrar que as ações são servidas de uma maneira separada do servidor principal do chatbot. Portanto, você também deve rodar o servidor de ações da seguinte maneira.

rasa run actions
