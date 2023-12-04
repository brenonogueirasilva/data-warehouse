# Projeto 6: Desenvolvimento de um DataWarehouse em ambiente Cloud

## Introdução
O Data Warehouse é uma arquitetura de armazenamento de dados que atua como um repositório central de dados integrados e estruturados, provenientes de uma ou mais fontes. Ele é especialmente direcionado para relatórios e análises de dados, sendo amplamente utilizado no contexto de Business Intelligence para fornecer informações cruciais para a tomada de decisões empresariais. 

O objetivo deste projeto é desenvolver um datawarehouse em ambiente cloud da Google, em específico no BigQuery, tendo como fonte um banco de dados relacional Mysql hospedado em um CloudSql. O banco de dados de produção por ser de natureza transacional (OLTP) é modelado orientado a entidade relacionamento, como no datawarehouse é voltado para processamento analítico (OLAP) será necessário trabalhar com modelo dimensional, junto de tabelas fatos e dimensões.

Para a transformação dos dados e consolidação das tabelas dimensionais no BigQuery, será utilizada a ferramenta DBT. Esta solução open source permite a materialização de tabelas do Data Warehouse por meio de consultas SQL, além de implementar lógica de carga incremental e tabelas de dimensão do tipo Slowly Changing Dimension (SCD). A integração entre o BigQuery e o Cloud SQL permitirá consultas federadas, possibilitando que o DBT realize toda a ETL de maneira eficiente. 

## Tecnologias Utilizadas
- **Cloud Sql:** serviço gerenciado de banco de dados relacional na Cloud do Google utilizado para o Mysql.
- **MySql:** banco de dados relacional no qual está armazenado os dados de produção utilizado para o desenvolvimento do datawarehouse.  
- **Python:** Linguagem de programação utilizada para executar os comandos do DBT;
- **Cloud Functions:** Ambiente na nuvem que executará o script python que executa os comandos DBT que transformam as tabelas do datawarehouse;
- **Cloud Scheduler:** Ferramenta na nuvem que permite agendar a execução das Cloud Functions, possibilitando automação e programação de tarefas. 
- **DBT:** Ferramenta utilizada para transformar dados por meio de consultas SQL, sendo aplicada para as cargas das tabelas do Data Warehouse. 
- **BigQuery:** Sistema de armazenamento gerenciado na nuvem voltado para análise, sendo portanto local no qual será desenvolvido o datawarehouse. 
- **Terraform:** Ferramenta que possibilita a provisionamento eficiente de toda a infraestrutura necessária, seguindo a metodologia de infraestrutura como código (IaC). 
  
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
### 1. Ingestão dos dados no banco de dados relacional
Como fonte de dados para o projeto será utilizado dados públicos disponíveis no Kaggle do Olist (https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), famosa plataforma de ecommerce brasileira. Os dados estão distribuídos através de inúmeras tabelas e por se tratarem de dados transacionais estão modelados através de entidade relacionamento (OLAP), abaixo é possível visualizar o relacionamento entre as tabelas.
Foto
Como etapa inicial do projeto será necessário criar todas estas tabelas no banco de dados Mysql,  lembrando de definir as restrições entre as tabelas, criando as chaves primários e estrangeiras e respeitando o modelo entidade relacionamento. Com as tabelas criadas no banco, basta ler os arquivos CSV disponiveis no kaggle e ingerir tais dados no banco, tal ação foi feita a partir do script data_ingestion (caminho do arquivo).

### 2. Definição do Modelo Dimensional
Com as tabelas já ingeridas no banco de dados Mysql, como forma de simular a origem de um banco de  produção, agora é o momento de estudo da tabela de um ponto de vista de negócio, buscando entender cada uma das colunas identificando quais são as informações podem agregar valor ao negócio, especialmente aquelas que são pertinentes para a extração de insights por meio de relatórios. 

Após a análise da tabela e a identificação das informações relevantes para o negócio, é hora de elaborar o modelo dimensional da tabela. Esse processo envolve a definição das dimensões, como datas, cidades e categorias de produtos, e dos fatos, que incluem informações como contagem de vendas e valor vendido. O resultado desse processo é um modelo dimensional orientado para um esquema de estrela, que pode ser visto abaixo:
Foto

### 3. Criação da conexão para as consultas federadas
Considerando que o banco de produção está no Cloud SQL e o Data Warehouse está no BigQuery, será necessário criar uma conexão dentro do BigQuery com o Cloud SQL. Isso será possível por meio de consultas federadas, permitindo que consultas dentro do BigQuery sejam realizadas no Cloud SQL. As consultas do DBT também serão federadas, funcionando como transformações e extrações simultâneas, sem a necessidade de criar pipelines externos para mover os dados. 

### 4. Desenvolvimento das Tabelas no DBT
O DBT será a solução escolhida para a transformação dos dados neste projeto. Por meio do DBT, é possível materializar tabelas por meio de consultas SQL, as quais serão federadas e terão como origem dados do Cloud SQL, embora estejam sendo processadas no BigQuery. Esse processo unificado realiza de uma única vez as etapas de Extração, Transformação e Carregamento (ETL). Vale ressaltar que o DBT é uma ferramenta amplamente utilizada no contexto de data warehouse, especialmente para as fases de transformação e carregamento, e não para extração. Portanto, se a fonte de dados fosse proveniente de APIs ou de um banco de dados diferente do Cloud SQL, seria necessário implementar pipelines externos para extrair e carregar os dados no BigQuery. 

Com o modelo dimensional já definido, avançamos para a criação dos modelos dentro do DBT, que consistem essencialmente em consultas SQL. Como prática recomendada em um data warehouse, é interessante utilizar surrogate keys, ou chaves substitutas, em vez das chaves primárias originais das tabelas. Essas novas chaves são específicas para o data warehouse e são geradas por meio de funções hash aplicadas a colunas que não se repetem. A implementação de funções hash no DBT é simples e pode ser realizada com a importação de bibliotecas disponíveis na própria ferramenta. 

As tabelas de dimensões e fatos, em sua maioria, são agregações das próprias tabelas originais. Portanto, as consultas SQL que utilizam agregadores representam de maneira eficaz as transformações necessárias nas tabelas. Esse é um dos motivos que justificam a escolha do DBT como ferramenta para esta etapa do projeto. 

Com as consultas SQL prontas, agora é o momento de pensar como será realizado a carga dos dados, sendo de forma incremental ou completa. Pensando em tabelas fatos em alguns casos de dimensões, será utilizada cargas incrementais, que a partir da data do ultimo registro sera utilziada como referncias, a logica incremental pode tambem ser feito no DBT, possibiltiando que a cada execução somente sejam acrescentando dados novos.

No entanto, para algumas dimensões, como a categoria de produtos, podem ocorrer mudanças nas categorias ou até mesmo nos nomes. Portanto, é necessário armazenar o histórico dessas mudanças. Para esse fim, será utilizada uma técnica conhecida como Slowly Changing Dimension do Tipo 2. Essa técnica realiza o versionamento das tabelas de dimensões, permitindo o armazenamento do histórico. A implementação dessa técnica será realizada no DBT com o uso de tabelas do tipo snapshot. 

### 5. Orquestrando a execução do DBT
Com os modelos SQL já pronto no DBT e as tabelas do datawarehouse já materializadas, é necessario criar uma rotina de execução intervalada que execute comandos do DBT para realizar cargas incremental no Datawarehouse dentro de intervalos de tempo definidos. Para isso, será utilziado o Cloud Function, que executará uma rotina que executa comandos do DBT, já que ele tambem é um biblioteca do python, através de horarios definidos no Cloud Scheduler. Tudo isso sendo provisionado seguindo boas praticas de Dev Ops com o uso de Terraform.

## Pré-requisitos
Para execução do codigo é necessário possuir terraform instalado na máquina local, uma conta no GCP com criação de um usuário de serviço com acesso a todos os serviços mencionados no projeto. 

## Executando o projeto
1. Copie o diretório do projeto para uma pasta local em seu computador.
2. Abra o terminal do seu computador e mova até o diretório do projeto.
3. Crie uma conta de serviço no GCP com as credenciais para todos os serviços mencionados, baixe uma chave em um arquivo json e coloque o arquivo no diretório raiz com nome `apt-theme-402300-32506a51a70d`.
4. Execute o comando: `terraform init`.
5. Execute o comando: `terraform plan`.
6. Execute o comando: `terraform apply`.
7. Com a infra provicionada, através de SSH entre na instância para criar o container mongodb. E Posteriormente entre no terminal do container para criar um usuário de serviço para a API e crie o banco movies. Posteriormente de acordo com as credenciais criadas, crie um dicionário com os parâmetros necessários da API e salve no Secret Manager. Atualize eventuais valores variaveis dependendo do nome da chave criada no Secret Manager.
