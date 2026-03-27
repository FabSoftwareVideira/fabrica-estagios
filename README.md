# Gerenciamento de Estágios - Fábrica de Software do IFC Videira

Projeto de Extensão do IFC-Videira intitulado "Uma ferramenta computacional para gerenciar os estágios supervisionados do curso técnico em Informática do IFC Videira e otimizar o fluxo de trabalho dos servidores envolvidos." sob a coordenação do prof. Wanderson Rigo e tendo o aluno de CCO Bruno Vinícus Pergher (https://github.com/BrunoPergher) como bolsista.

- Objetivos Gerais:
Desenvolver uma plataforma web para gerir, otimizar e automatizar os processos de estágios supervisionados no IFC Videira, visando: 
- simplificar as tarefas burocráticas; 
- promover uma comunicação eficiente entre estagiários, supervisores e orientadores; 
- oferecer um acompanhamento contínuo das atividades dos estagiários, melhorando assim a gestão e o controle das atividades; 
- aperfeiçoar a seleção de orientadores e a formação de bancas de avaliação; 

Tudo isso com o propósito de aprimorar a experiência dos envolvidos e a eficácia do programa de estágios. 


Está executando em https://estagios.fsw-ifc.brdrive.net

## Rodando com Docker (modo desenvolvimento)

Pré-requisitos:
- Docker e Docker Compose instalados.
- Copie o arquivo `.env.sample` para `.env` e ajuste as variáveis conforme necessário

Variáveis de metadados do app:
- `APP_VERSION`: versão publicada para a aplicação e para as imagens/containers Docker.
- `APP_ENV`: ambiente padrão do `.env`; o Compose de desenvolvimento força `development` e o Compose de produção força `production`.

Subir o ambiente:

```bash
docker compose up --build
```

Parar o ambiente:

```bash
docker compose down
```

No modo dev:
- A aplicação sobe em `http://localhost:5000`.
- O código é montado via volume (`.:/app`), então alterações locais recarregam automaticamente.
- As migrações são aplicadas automaticamente na inicialização (`flask db upgrade`).

### Migrations (Alembic/Flask-Migrate)

Aplicar migrations pendentes:

```bash
docker compose exec estagios-web flask db upgrade
```

Ver histórico de migrations:

```bash
docker compose exec estagios-web flask db history
```

Criar uma nova migration (quando alterar modelos):

```bash
docker compose exec estagios-web flask db migrate -m "descricao_da_migration"
docker compose exec estagios-web flask db upgrade
```

Em produção:

```bash
docker exec -it estagios-prod-web flask db upgrade
```

### Seed de dados

O projeto possui o comando `flask seed` para criar dados iniciais (idempotente):

```bash
docker compose exec estagios-web flask seed
```

Em produção:

```bash
docker exec -it estagios-prod-web flask seed
```

## Publicação no GHCR

O projeto publica a imagem de produção no GitHub Container Registry e o deploy em produção faz `pull` dessa imagem, em vez de gerar o build no servidor.

Imagem publicada:
- `ghcr.io/fabsoftwarevideira/fabrica-estagios:latest`
- `ghcr.io/fabsoftwarevideira/fabrica-estagios:sha-<commit>`
- `ghcr.io/fabsoftwarevideira/fabrica-estagios:<versao>` quando houver tag Git no formato `v*`

Workflows:
- [.github/workflows/publish-image.yml](.github/workflows/publish-image.yml): builda a stage `prod` do Dockerfile e publica no GHCR.
- [.github/workflows/deploy.yml](.github/workflows/deploy.yml): após a publicação, autentica no GHCR, faz `pull` da imagem e sobe os containers com o Compose de produção.

Para o deploy automático funcionar:
- o package do GHCR deve estar acessível para o repositório ou para o token usado pelo workflow;
- o runner self-hosted precisa conseguir acessar `ghcr.io`;
- o secret `ENV_FILE` continua sendo a fonte das variáveis sensíveis do ambiente.

Deploy manual da imagem publicada:

```bash
docker login ghcr.io
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --remove-orphans
```

## Rodando localmente (modo desenvolvimento)
