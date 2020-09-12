from arquivo import *


# função para ver se o arquivo onde estõ guardadas as definições do programa existe
def exitarq(arquivo, mg=False):
    try:
        red = open(arquivo, 'r')
    except:
        if mg:
            sg.popup_quick_message('Erro na abertura do arquivo de definições', font='123')
            sleep(2)
        return False
    else:
        red.close()
        return True


def criararq(arquivo):
    try:
        red = open(arquivo, 'w+')
    except:
        sg.popup_quick_message('Erro na criação do arquivo', font='123')
        sleep(2)
    else:
        sg.popup_quick_message('Arquivo salvo com sucesso!', font='123')
        sleep(2)
        red.close()


# função para salvar dados do programa.
def salvar(arquivo, defini, chave):
    lista = '''aAbBcCdDeEêfFgGrRsStTuUvVwWxXyYzZ1234567890 {([])}\/,.:;'"@hHiIjJkKlLmMnNoOpPqQ'''
    defini = f'{defini[0]}@{defini[1]}@{defini[2]}'
    nova = [lista[(lista.index(c) + chave) % (len(lista) - 2)] for c in defini]
    nova = ''.join(nova)
    try:
        red = open(arquivo, 'w+')
    except:
        sg.popup_quick_message('Erro ao salvar as definicões', font='123')
        sleep(2)
    else:
        red.write(f'{nova}')


def abrirarq(arquivo, chave):
    try:
        re = open(arquivo, 'r')
    except:
        sg.popup_quick_message('Erro na leitura do arquivo', font='123')
        sleep(2)
    else:
        lista = '''aAbBcCdDeEêfFgGrRsStTuUvVwWxXyYzZ1234567890 {([])}\/,.:;'"@hHiIjJkKlLmMnNoOpPqQ'''
        return ''.join([lista[(lista.index(c) - chave) % (len(lista) - 2)] for c in re.read()]).split('@')
