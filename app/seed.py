import uuid
from datetime import date, datetime

import click
from flask.cli import with_appcontext
from flask_security.utils import hash_password

from app import db
from app.models import (
    Aluno,
    Empresa,
    Estagio,
    Professor,
    Role,
    StatusEstagio,
    Supervisor,
    User,
)


def _ensure_roles() -> None:
    role_names = ["professor", "empresa", "supervisor", "aluno", "admin"]

    for role_name in role_names:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            db.session.add(Role(name=role_name, description=f"{role_name.capitalize()} Role"))

    db.session.commit()


def _ensure_user(username: str, email: str, password: str, roles: list[str]) -> User:
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            username=username,
            email=email,
            password=hash_password(password),
            active=True,
            fs_uniquifier=str(uuid.uuid4()),
            confirmed_at=datetime.utcnow(),
        )
        db.session.add(user)
        db.session.commit()

    role_objects = Role.query.filter(Role.name.in_(roles)).all()
    current_roles = {role.name for role in user.roles}
    for role in role_objects:
        if role.name not in current_roles:
            user.roles.append(role)

    db.session.commit()
    return user


@click.command("seed")
@with_appcontext
def seed_command() -> None:
    _ensure_roles()

    admin_user = _ensure_user("admin", "admin@admin.com", "Admin123!", ["admin"])
    empresa_user = _ensure_user("empresa.demo", "empresa.demo@estagios.com", "Demo123!", ["empresa"])
    professor_user = _ensure_user("professor.demo", "professor.demo@estagios.com", "Demo123!", ["professor"])
    aluno_user = _ensure_user("aluno.demo", "aluno.demo@estagios.com", "Demo123!", ["aluno"])
    supervisor_user = _ensure_user("supervisor.demo", "supervisor.demo@estagios.com", "Demo123!", ["supervisor"])

    empresa = Empresa.query.filter_by(cnpj="12.345.678/0001-90").first()
    if not empresa:
        empresa = Empresa(
            cnpj="12.345.678/0001-90",
            qsa="QSA de exemplo",
            rg_responsavel="1234567",
            cpf_responsavel="123.456.789-00",
            nome_empresa="Empresa Demo Ltda",
            nome_responsavel="Maria Responsavel",
            email_empresa="contato@empresademo.com",
            email_responsavel="maria@empresademo.com",
            telefone_empresa="(49) 3333-0000",
            telefone_responsavel="(49) 99999-0000",
            user_id=empresa_user.id,
            is_approved=True,
        )
        db.session.add(empresa)
        db.session.commit()

    professor = Professor.query.filter_by(cpf="987.654.321-00").first()
    if not professor:
        professor = Professor(
            nome="Professor Demo",
            email="professor.demo@ifc.edu.br",
            cpf="987.654.321-00",
            user_id=professor_user.id,
            is_approved=True,
        )
        db.session.add(professor)
        db.session.commit()
    
    professores = [
        {
            "nome": "Fabricio Bizotto",
            "email": "fabricio.bizotto@ifc.edu.br",
            "cpf": "067.569.199-03",
            "is_approved": True,
        },
        {
            "nome": "Wanderson Rigo",
            "email": "wanderson.rigo@ifc.edu.br",
            "cpf": "067.569.199-04",
            "is_approved": True,
        }
    ]

    for prof in professores:
        existing_professor = Professor.query.filter_by(cpf=prof["cpf"]).first()
        if not existing_professor:
            new_professor = Professor(
                nome=prof["nome"],
                email=prof["email"],
                cpf=prof["cpf"],
                user_id=professor_user.id,
                is_approved=prof["is_approved"],
            )
            db.session.add(new_professor)
            db.session.commit()

    aluno = Aluno.query.filter_by(matricula="20260001").first()
    if not aluno:
        aluno = Aluno(
            nome="Aluno Demo",
            matricula="20260001",
            data_de_nascimento=date(2006, 1, 1),
            rg="7654321",
            cpf="111.222.333-44",
            email="aluno.demo@ifc.edu.br",
            celular="(49) 99999-1111",
            user_id=aluno_user.id,
            is_approved=True,
        )
        db.session.add(aluno)
        db.session.commit()

    supervisor = Supervisor.query.filter_by(cpf="222.333.444-55").first()
    if not supervisor:
        supervisor = Supervisor(
            cpf="222.333.444-55",
            nome="Supervisor Demo",
            formacao="Tecnologo em TI",
            telefone="(49) 99999-2222",
            email="supervisor.demo@empresademo.com",
            empresa_id=empresa.id,
            user_id=supervisor_user.id,
            is_approved=True,
        )
        db.session.add(supervisor)
        db.session.commit()

    estagio_existente = Estagio.query.filter_by(
        aluno_id=aluno.id,
        professor_id=professor.id,
        supervisor_id=supervisor.id,
        empresa_id=empresa.id,
    ).first()

    if not estagio_existente:
        db.session.add(
            Estagio(
                aluno_id=aluno.id,
                professor_id=professor.id,
                supervisor_id=supervisor.id,
                empresa_id=empresa.id,
                modalidade="Obrigatorio",
                carga_horaria=400,
                atividades="Atividades de desenvolvimento e suporte de sistemas.",
                setor="TI",
                remuneracao=True,
                valor_remuneracao=1200.00,
                horario_estagio="08:00 as 12:00",
                data_inicio=date(2026, 3, 1),
                data_conclusao=date(2026, 7, 31),
                is_approved=True,
                status=StatusEstagio.EM_ANDAMENTO,
            )
        )
        db.session.commit()

    click.echo("Seed concluido com sucesso.")