# e-stagio

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
- Arquivo `.env` na raiz do projeto com as variáveis necessárias (incluindo conexão com banco e chaves da aplicação).

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

### Seed de dados

O projeto possui o comando `flask seed` para criar dados iniciais (idempotente):

```bash
docker compose exec estagios-web flask seed
```