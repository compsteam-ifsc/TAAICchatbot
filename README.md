# TAAICchatbot

## 🤖 rasa-project

Este repositório reúne o desenvolvimento do projeto PIGAS3818-2024 – Transformando o Atendimento Acadêmico com Agentes Inteligentes Conversacionais, conduzido pelo grupo de pesquisa CompSTEAM do Instituto Federal de Santa Catarina – Câmpus Gaspar (IFSC).

O objetivo principal do projeto é a criação de um chatbot baseado em inteligência artificial voltado para o atendimento de discentes de cursos de graduação. A solução busca apoiar estudantes no acesso a informações institucionais, proporcionando maior agilidade na comunicação e facilitando o esclarecimento de dúvidas frequentes.

O chatbot foi desenvolvido com Python e o framework Rasa, incluindo integração com fontes de dados externas. Além da entrega técnica, o projeto possui caráter formativo, pois contribuiu para a capacitação acadêmica e profissional dos bolsistas e voluntários envolvidos, que vivenciaram experiências práticas em programação, inteligência artificial e engenharia de software aplicada ao contexto educacional.

Para ver o repositório da página web para interação com o chatbot, acesse o repositório [rasa-frontend](https://github.com/ifscbot/rasa-frontend).

### Estrutura de arquivos

| **`/`**                  |                                                                                             |
|--------------------------|---------------------------------------------------------------------------------------------|
| **`domain.yml`**         | Define o domínio do chatbot, incluindo intenções, entidades e respostas de ações.           |
| **`config.yml`**         | Especifica as configurações do modelo RASA, como o pipeline de processamento de linguagem natural. |
| **`endpoints.yml`**      | Contém informações sobre os endpoints, como o servidor do modelo e o servidor de ações.     |
| **`credentials.yml`**    | Armazena credenciais para serviços externos, como APIs ou canais de mensagens.              |
| **`datas_e_links.csv`**  | Contém a tabela com respostas variáveis periodicamente (data de recesso escolar, data de editais, link de editais, etc.), *devendo* ser acessada constantemente para se atualizar seus dados. |

| **`data/`**              | Diretório que contém dados de treinamento e regras para o modelo.                           |
|--------------------------|---------------------------------------------------------------------------------------------|
| - **`nlu.yml`**          | Exemplos de treinamento para o processamento de linguagem natural (frases reais).           |
| - **`stories.yml`**      | Contém "histórias" de exemplo para treinar o modelo a seguir fluxos de conversação.         |
| - **`rules.yml`**        | Define regras de conversação para orientar o comportamento do chatbot.                      |

| **`actions/`**           | Diretório que contém o código fonte para ações personalizadas do chatbot.                   |
|--------------------------|---------------------------------------------------------------------------------------------|
| - **`actions.py`**       | Define as ações personalizadas que o chatbot pode realizar. Destaca-se a action de processar horário, que verifica se o câmpus está aberto no horário em que o usuário perguntou ao chatbot, e a action que consulta a tabela 'datas_e_links.csv' e retorna, de acordo com a intent identificada, a resposta adequada. |

| **`ações customizadas do projeto`**           | Descrição.                   |
|--------------------------|---------------------------------------------------------------------------------------------|
| - **`action_processar_horario_campus`**       | Ao se perguntar se o campus está aberto, invocando a intent correpondente, esta action verifica o horário de funcionamento do campus com base no dia e hora atual. Ela determina se o campus está aberto no momento, se abrirá mais tarde no mesmo dia, no próximo dia útil ou apenas na próxima segunda-feira. A action fornece respostas com base no horário regular de funcionamento (segunda a sexta, das 7h às 23h30). |
| - **`action_consultar_dados_dinamicos`**       | Esta action consulta uma tabela CSV (datas_e_links.csv) para obter informações variáveis (datas que variam em todo ano escolar, de recessos, matrículas, editais, etc.) baseadas na intent do usuário. Ela busca dados correspondentes à intent atual e preenche placeholders no texto de resposta com os valores especificados da tabela, fornecendo respostas personalizadas com informações atualizáveis sem necessidade de modificar o código. |

### Componentes fundamentais do Rasa

| **`/`**                  |                                                                                             |
|--------------------------|---------------------------------------------------------------------------------------------|
| **`intent`**             | As intenções representam o propósito ou objetivo por trás da mensagem do usuário. Elas categorizam o que o usuário está tentando alcançar com sua mensagem. |
| **`entity`**             | As entidades são informações específicas extraídas das mensagens dos usuários. Elas representam dados importantes que o chatbot precisa para processar a solicitação. |
| **`slot`**               | são variáveis que armazenam informações durante a conversa. Eles podem ser preenchidos por entidades extraídas e são usados para personalizar respostas. |
| **`mapping`**            | define como as entidades extraídas das mensagens dos usuários são mapeadas para os slots. Ele especifica a relação entre entidades e slots. |
| **`synonimous`**         | são usados para normalizar variações de valores de entidades para um valor padrão, garantindo consistência no processamento. |

### Como desenvolver

Primeiro, abra o projeto em um editor de código fonte e edite os arquivos da maneira necessária. Certifique-se de que você tem o framework [Rasa Open Source](https://rasa.com/docs/rasa/installation/installing-rasa-open-source/) instalado e a versão correta do Python em sua máquina. Dentro do diretório do projeto, no Terminal, você pode executar o seguinte:

**Para treinar o modelo usando os dados de treinamento definidos em `data/`** 
```
rasa train
```

**Para iniciar uma sessão simples de conversa para testar o comportamento do chatbot**
```bash
rasa shell
```

**Para iniciar uma sessão interativa de conversa para testar de debugar o comportamento do chatbot**
```bash
rasa interactive
```

Sempre que estiver conversando com o chatbot e precisar executar uma ação de script, certifique-se de [iniciar o servidor de ações](#rodar-o-chatbot).

#### Customizando respostas

Para customizar as respostas do chatbot, você deve editar o arquivo `domain.yml`. Caso queira implementar uma ação customizada em Python (que cheque algum tipo de serviço externo ou tenha uma lógica própria), adicione uma classe no arquivo `actions/actions.py`, como, por exemplo, a nossa action de processar o horário, onde ao usuário perguntar se o câmpus está aberto, a action compara o horário em que a mensagem foi enviada em relação ao horário de funcionamento do câmpus, e dá uma resposta de acordo. Para mais informações, veja [este documento](https://rasa.com/docs/rasa/actions/).

### Rodar o chatbot

Para iniciar uma sessão do chatbot que o exponha para os serviços externos (definidos em `endpoints.yml`), você pode rodar o seguinte comando: 

```bash
rasa run -m models --enable-api --cors "*" --debug -p 5005
```

No entanto, vale lembrar que as ações são servidas de uma maneira separada do servidor principal do chatbot. Portanto, você também deve rodar o servidor de ações da seguinte maneira.

```bash
rasa run actions
```
