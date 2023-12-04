# Projeto 5: Desenvolvimento de uma API junto a banco de dados NoSQL

## Introdução
Este projeto tem como objetivo desenvolver uma API que interaja com um banco de dados NoSQL MongoDB, hospedado no ambiente de nuvem da Google (GCP). A API será capaz de realizar todas as operações do CRUD (Create, Read, Update, Delete), permitindo a criação, leitura, atualização e exclusão de registros ou documentos. A proposta visa simular uma etapa do ambiente de trabalho de um engenheiro de dados, que frequentemente precisa disponibilizar dados por meio de uma API em vez de permitir acesso direto ao banco. Isso se deve às inúmeras vantagens proporcionadas, como maior segurança, abstração mais eficiente dos dados, padronização e flexibilidade na manutenção.

## Tecnologias Utilizadas
- **MongoDb:** Banco de Dados NoSQL amplamente adotado no mercado, servindo como o principal ponto de interação para todas as operações do CRUD pela API.
- **CloudRun:** Ambiente serverless que hospedará um contêiner contendo Python, FastAPI e outros requisitos essenciais. Este ambiente é responsável pela execução dinâmica da aplicação e disponibilização dos endpoints da API por meio de um link.
- **FastApi:** Framework em Python utilizado para o desenvolvimento da API. Oferece desempenho eficiente e facilidade de desenvolvimento, possibilitando a criação de endpoints eficazes.
- **Google Compute Engine:** Ambiente utilizado para provisionar o banco de dados NoSQL MongoDB. Oferece controle total sobre a configuração e escalabilidade do banco de dados, constituindo a base sólida para a aplicação.
- **Python:** Linguagem de programação utilizada no projeto, integrada ao framework FastAPI para a implementação da lógica da API.
- **SecretManger:** Serviço de armazenamento de senhas e outros dados sensíveis, utilizado para armazenar informações sobre as credencias do banco, garantindo maior segurança a API.
- **Terraform:** Ferramenta que permite o provisionamento eficiente de toda a infraestrutura necessária, seguindo a metodologia de Infraestrutura como Código (IaC). Facilita a gestão e manutenção consistente da infraestrutura.
- **Docker:** Utilizado para criar imagens que serão empregadas no CloudRun e contêineres executados dentro de uma instância para o provisionamento do banco de dados NoSQL dentro Google Compute Engine.
  
<p align="left">
<img src="/img/MongoDB-Logo.jpg" alt="mongoDB" height="50" /> 
<img src="/img/cloud-run.png" alt="cloud-run" height="50" /> 
<img src="/img/fast-api.png" alt="fastapi" height="50"/> 
<img src="/img/Google-Compute-Engine.png" alt="google-compute-engine" height="50"/> 
<img src="/img/python-logo.png" alt="python" height="50"/> 
<img src="/img/secret-manager.png" alt="secret-manager" height="50"/> 
<img src="/img/terraform.png" alt="terraform" height="50"/> 
<img src="/img/docker-logo.png" alt="docker" height="50"/> 
</p>

## Arquitetura do projeto

![Diagrama de Arquiteura do Projeto API NoSql](img/arquitetura_api_nosql.png)

## Etapas do Projeto
### 1. Provisionamento da Infraestrutura do Banco de Dados
No contexto do projeto, a escolha do MongoDB como banco de dados NoSQL foi baseada em sua ampla adoção no mercado. No entanto, ao contrário de soluções PaaS (Plataforma como Serviço) disponíveis no Google Cloud Platform (GCP) para bancos relacionais, como Postgres e MySQL dentro do CloudSql, a ausência de uma oferta específica para o MongoDB exigiu o provisionamento manual da infraestrutura na nuvem. Para realizar esse provisionamento, optou-se pela utilização do Terraform, seguindo as práticas recomendadas de Infraestrutura como Código (IaC). Isso envolveu a criação de uma instância no GCP, configurando-a como uma máquina virtual capaz de executar o MongoDB. Posteriormente, através de uma conexão SSH, o Docker foi instalado na máquina, e a execução de um contêiner MongoDB foi configurada a partir de uma imagem disponível no Docker Hub. Como medida de segurança, apenas a porta necessária para a conexão com o MongoDB foi liberada no firewall da instância, proporcionando uma camada adicional de proteção.

### 2. Desenvolvimento da Lógica da API
Com o banco de dados em pleno funcionamento, tornou-se possível iniciar o desenvolvimento local da lógica da API. Para facilitar essa interação, uma classe denominada MongoDB {colocar link} foi criada, encarregada de gerenciar as operações CRUD necessárias. Para realizar testes e validar os resultados da API, a ingestão de dados no MongoDB foi efetuada utilizando um dataset público da IMDb, que contém informações sobre filmes. A lógica da API foi implementada utilizando o framework FastAPI. Três endpoints distintos foram desenvolvidos: um para requisições do tipo POST voltadas para operações de consulta, outro também do tipo POST destinado a operações de criação, e um terceiro para requisições DELETE e PUT, permitindo deleção e edição de registros (código se encontra no arquivo imdb.py {mostrar link do arquivo}. Ainda, visando eficiência e desempenho, uma lógica de paginação foi incorporada à API. Os parâmetros de entrada foram definidos utilizando a classe BaseModel do Pydantic no arquivo models {link do arquivo}, garantindo a formatação correta das entradas dos métodos. Além disso, a documentação automática gerada pelo FastAPI proporciona uma compreensão fácil e correta do uso da API.
Foi  criado também uma classe capaz de interagir com a API em si e o banco de dados, chamada de IntegradorApi {mostrar o link}.

### 3. Criação do Container e Deploy no Cloud Run
Para viabilizar o deployment da API, um Dockerfile {mostrar link do DockerFile} foi criado. Este arquivo continha uma imagem Python com todas as bibliotecas necessárias para o projeto. Após a criação do contêiner, uma instrução foi executada para criar um serviço utilizando o Uvicorn em uma porta específica, que seria utilizada para acessar a API. A imagem do contêiner foi então enviada para o Artifactory Registry, um repositório da Google. Posteriormente, foi configurado o Cloud Run, um ambiente serverless que possibilita a execução do contêiner. O Cloud Run forneceu um link que serviria como o endpoint para interação com a API.

### 4. Segurança
Em termos de segurança, algumas práticas foram adotadas para proteger o sistema. Foi criado um usuário de serviço específico para a API no MongoDB, evitando o uso de usuários "roots". Além disso, apenas a porta essencial para a conexão com o MongoDB foi liberada no firewall da instância, proporcionando uma camada adicional de segurança. Para gerenciar o acesso às credenciais do banco, foi adotado o Secret Manager, evitando que as credenciais fossem diretamente digitadas no código. Essas etapas formam um processo abrangente, desde o provisionamento da infraestrutura até o deployment da API no Cloud Run, com atenção especial à segurança em todas as fases do projeto.

#### Observação
Todo o código é documentado através de docstrings, o que possibilita um entendimento mais profundo do código em si caso necessário.

## Pré-requisitos
Para executar o código deste projeto, é necessário possuir uma conta no Google Cloud Platform (GCP). Além disso, é necessárop ter o aplicativo Terraform e o CLI Cloud instalados localmente em sua máquina.

## Executando o projeto
1. Copie o diretório do projeto para uma pasta local em seu computador.
2. Abra o terminal do seu computador e mova até o diretório do projeto.
3. Crie uma conta de serviço no GCP com as credenciais para todos os serviços mencionados, baixe uma chave em um arquivo json e coloque o arquivo no diretório raiz com nome `apt-theme-402300-32506a51a70d`.
4. Execute o comando: `terraform init`.
5. Execute o comando: `terraform plan`.
6. Execute o comando: `terraform apply`.
7. Com a infra provicionada, através de SSH entre na instância para criar o container mongodb. E Posteriormente entre no terminal do container para criar um usuário de serviço para a API e crie o banco movies. Posteriormente de acordo com as credenciais criadas, crie um dicionário com os parâmetros necessários da API e salve no Secret Manager. Atualize eventuais valores variaveis dependendo do nome da chave criada no Secret Manager.
