#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from perfis.models import Perfil
from cursos.models import Curso
from disciplinas.models import Disciplina

def create_initial_data():
    print("🔄 Criando dados iniciais...")

    if not Perfil.objects.filter(email='admin@example.com').exists():
        gerente = Perfil.objects.create(
            email='admin@example.com',
            nome='Administrador do Sistema',
            tipo='Gerente',
            ativo=True,
            is_staff=True,
            is_superuser=True
        )
        gerente.set_password('admin123')
        gerente.save()
        print(f"✅ Usuário Gerente criado: {gerente.codigo} - {gerente.email}")
    else:
        print("ℹ️  Usuário Gerente já existe")

    if not Perfil.objects.filter(email='professor@example.com').exists():
        professor = Perfil.objects.create(
            email='professor@example.com',
            nome='Professor Exemplo',
            tipo='Professor',
            ativo=True
        )
        professor.set_password('prof123')
        professor.save()
        print(f"✅ Usuário Professor criado: {professor.codigo} - {professor.email}")
    else:
        print("ℹ️  Usuário Professor já existe")

    if not Curso.objects.filter(codigo='ADS2025').exists():
        curso = Curso.objects.create(
            codigo='ADS2025',
            nome='Análise e Desenvolvimento de Sistemas',
            descricao='Curso superior de tecnologia em ADS',
            carga_horaria_total=2400,
            ativo=True
        )
        print(f"✅ Curso criado: {curso.codigo} - {curso.nome}")

        disciplinas_exemplo = [
            {'codigo': 'BD101', 'nome': 'Banco de Dados I', 'carga_horaria': 80},
            {'codigo': 'PROG101', 'nome': 'Programação I', 'carga_horaria': 120},
            {'codigo': 'WEB101', 'nome': 'Desenvolvimento Web I', 'carga_horaria': 100},
        ]

        for disc_data in disciplinas_exemplo:
            if not Disciplina.objects.filter(codigo=disc_data['codigo']).exists():
                disciplina = Disciplina.objects.create(
                    curso=curso,
                    **disc_data,
                    ativo=True
                )
                print(f"✅ Disciplina criada: {disciplina.codigo} - {disciplina.nome}")
    else:
        print("ℹ️  Curso exemplo já existe")

    print("\n🎉 Dados iniciais criados com sucesso!")
    print("\n📋 Credenciais de acesso:")
    print("   👤 Gerente: admin@example.com / admin123")
    print("   👤 Professor: professor@example.com / prof123")

if __name__ == '__main__':
    create_initial_data()