# Backend do Projeto do Site de Leilão da Apae

Bem-vindo ao repositório do backend do projeto do site de Leilão da Apae (Associação de Pais e Amigos de Pessoas Excepcionais). Neste repositório, você encontrará o código-fonte e informações sobre as tecnologias e serviços utilizados para criar o backend deste projeto.

## Visão Geral

Este repositório contém o código-fonte do backend do site de Leilão da Apae, que é um sistema de leilões online para arrecadar fundos para a Associação de Pais e Amigos de Pessoas Excepcionais. O backend é construído utilizando as seguintes tecnologias e serviços:

- [AWS CDK (Cloud Development Kit)](https://aws.amazon.com/cdk/): O AWS CDK é uma ferramenta que permite definir infraestrutura como código em várias linguagens, incluindo Python. Ele facilita a criação de recursos na AWS.

- [AWS Serverless](https://aws.amazon.com/serverless/): Este projeto é baseado na arquitetura serverless, o que significa que não é necessário provisionar servidores. A AWS gerencia automaticamente a escalabilidade e a disponibilidade dos recursos.

- [AWS Lambda](https://aws.amazon.com/lambda/): Os Lambda functions são usados para executar código sem servidor em resposta a eventos. Neste projeto, as funções Lambda desempenham um papel central no processamento de solicitações e execução de lógica de negócios.

- [Amazon API Gateway](https://aws.amazon.com/api-gateway/): O Amazon API Gateway é usado para criar e gerenciar APIs RESTful. Ele atua como uma interface entre o cliente e as funções Lambda, permitindo que as solicitações HTTP sejam roteadas para as funções apropriadas.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): O DynamoDB é um serviço de banco de dados NoSQL gerenciado pela AWS. É usado para armazenar dados do leilão, como informações de itens e lances.

- [Amazon S3 (Simple Storage Service)](https://aws.amazon.com/s3/): O Amazon S3 é usado para armazenar ativos estáticos, como imagens e documentos relacionados ao leilão.

- Python: A linguagem de programação Python é usada para escrever o código das funções Lambda e para automatizar o provisionamento de recursos por meio do AWS CDK.

- Diagrama de Infraestrutura de nosso Produto em Nuvem AWS:

![image](https://github.com/FelipeCarillo/apaeleilao_mss/assets/63021830/3177a46c-ada9-481c-b5e5-92daf1f40db7)

## Estrutura do Projeto

O projeto é organizado em diretórios que correspondem a diferentes componentes e recursos. Aqui está uma visão geral da estrutura do projeto:

- `src/`: Este diretório contém o código-fonte das funções Lambda que executam a lógica de negócios do leilão.

- `iac/`: Este diretório contém os arquivos do AWS CDK para provisionar os recursos na AWS. Você pode usar o CDK para implantar e atualizar a infraestrutura do projeto.

## Contato

Se você tiver alguma dúvida ou precisar de assistência, entre em contato com a equipe de desenvolvimento do projeto de Leilão da Apae. Você também pode acompanhar o progresso do projeto e contribuir por meio de nossa conta no GitHub:

- GitHub: [Felipe Carillo](https://github.com/FelipeCarillo)

Agradecemos sua contribuição e apoio à causa da Apae!

## Equipe de Desenvolvimento

- Felipe Carillo - [FelipeCarillo](https://github.com/FelipeCarillo)
- Felipe Taewoo Moon - [MelipeFoon](https://github.com/MelipeFoon)
- Edgar Kodjoglamian Messias - [edkod](https://github.com/edkod)

## Agradecimentos

Gostaríamos de expressar nossa gratidão à seguintes fontes de inspiração que contribuíram para o sucesso deste projeto:

- [Dev. Community Mauá](https://github.com/Maua-Dev): Este projeto foi baseado no código-fonte do projeto [clean_mss_template](https://github.com/Maua-Dev/clean_mss_template).
- [Institute Mauá of Technology](https://www.maua.br/)

Agradecemos a todos os envolvidos, direta ou indiretamente, e à comunidade de código aberto por suas contribuições e apoio contínuo.
