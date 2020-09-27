import sqlite3 as sq
import pymysql as my
import PySimpleGUI as sg
from time import sleep
from random import randint, choice

banco = 'E:\clement\cours\github\dados.cgt'


# Def para criação e conexão de um banco de dabos.
def banco_de_dados(banco_dados: str, tente=False):
    try:
        conexao = sq.connect(banco_dados)
        cursor = conexao.cursor()
        cursor.execute(
            'create table if not exists turmas(ID int, nome text, tutor text, class int, detalhes text)')
        cursor.execute(
            'create table if not exists alunos(ID int, nome text, idade int, sexo text, '
            'data1 text, turma text, data2 text, numero1 int, numero2 int, morada text,'
            ' email text, detalhes text, foto text)')
        cursor.execute(
            'create table if not exists tutor(ID int, nome text, numero text, sexo int, aulas text, detalhes text)')
        cursor.execute(
            'create table if not exists escola(nome text)')
        conexao.commit()
        cursor.close()
        conexao.close()
    except:
        sg.popup_quick_message('Erro na abertura do arquivo.', font='123')
        sleep(2)
        if tente:
            return False
    else:
        if tente:
            return True


def criar_aluno(banco_dados, turma, date2, Id=1000):
    sexo = choice(['Masculino', 'Feminino'])
    conexao = sq.connect(banco_dados)
    cursor = conexao.cursor()
    cursor.execute('''insert into alunos(ID, nome, idade, sexo, data1, turma, data2, numero1, numero2,
     morada, email, detalhes, foto) values(?, 'Desconhecido', 10, ?, 
     '00/00/0000', ?, ?, 111111, 222222, 'mundo', '<nada>', ' ', 'image1.png')''', (Id, sexo, turma, date2))
    conexao.commit()
    cursor.close()
    conexao.close()


def abrir_alunos(BancoDeDados):
    conexao = sq.connect(BancoDeDados)
    cursor = conexao.cursor()
    cursor.execute('select ID, nome, idade, sexo, data1, turma, data2, numero1, numero2, '
                   'morada, email, detalhes from alunos')
    retorna = cursor.fetchall()
    cursor.close()
    conexao.close()
    return retorna


def abrir_Turmas(BancoDeDados):
    conexao = sq.connect(BancoDeDados)
    cursor = conexao.cursor()
    cursor.execute('select ID, nome, tutor, class, detalhes from turmas')
    retorna = cursor.fetchall()
    cursor.close()
    conexao.close()
    return retorna


def criar_Turma(banco_dados, nome, tutor, classi, detalhes, ID=1000):
    conexao = sq.connect(banco_dados)
    cursor = conexao.cursor()
    cursor.execute('''insert into turmas(ID, nome, tutor, class, detalhes) values(?, ?, ?, ?, ?)''',
                   (ID, nome, tutor, classi, detalhes))
    conexao.commit()
    cursor.close()
    conexao.close()


def abrir_Tutor(BancoDeDados):
    conexao = sq.connect(BancoDeDados)
    cursor = conexao.cursor()
    cursor.execute('select ID, nome, numero, sexo, aulas, detalhes from tutor')
    retorna = cursor.fetchall()
    cursor.close()
    conexao.close()
    return retorna


def criar_Tutor(banco_dados, nome, numero, sexo, aulas, detalhes, ID=1000):
    conexao = sq.connect(banco_dados)
    cursor = conexao.cursor()
    cursor.execute('''insert into tutor(ID, nome, numero, sexo, aulas, detalhes) values(?, ?, ?, ?, ?, ?)''',
                   (ID, nome, numero, sexo, aulas, detalhes,))
    conexao.commit()
    cursor.close()
    conexao.close()


def elimar(banco_de_dados, iden, table):
    conexao = sq.connect(banco_de_dados)
    curso = conexao.cursor()
    curso.execute(f'delete from {table} where ID={iden}')
    conexao.commit()
    curso.close()
    conexao.close()


def update(banco_de_dados, table, coluna, mude, referencia, constante):
    conexao = sq.connect(banco_de_dados)
    curso = conexao.cursor()
    lista = [table, coluna, mude, referencia, constante]
    curso.execute(f'''update {lista[0]} set {lista[1]}={lista[2]} where {lista[3]}= {lista[4]}''',)
    conexao.commit()
    curso.close()
    conexao.close()
