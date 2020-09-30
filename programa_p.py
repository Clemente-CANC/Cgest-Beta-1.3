from back import *
from datetime import datetime
import os.path
import PIL.Image
import io
import base64

# arquivo onde serão ou são guardados as definicões do programa.
nomed = 'Defi.cong'
# variavel na qual esta guardada a cofiguração padrão
definicoes_del = ['DarkBlue3', 'Português', 'dados.cgt']
# chave de incriptação serve para cifrar as definicões
chave = 5
definicoes = None
# criando um arquivo na qual serão guardados as definicões do programa.
if not exitarq(nomed):
    criararq(nomed)
    # salvando os dados pradrões do programa.
    salvar(nomed, definicoes_del, chave)
    # lendo os dados salvos para executar no programa.
    definicoes = abrirarq(nomed, chave)
    # abrindo um banco de dados
    banco_de_dados(definicoes[2])
elif exitarq(nomed):
    definicoes = abrirarq(nomed, chave)
    try:
        # verificando se tudo esta ok.
        tente = open(definicoes[2], 'r')
        tente.close()
    except:
        # em caso de erro.
        definicoes[2] = definicoes_del[2]

data = f'{datetime.today().day}/{datetime.today().month}/{datetime.today().year}'
try:
    tutores = abrir_Tutor(definicoes[2])
except:
    banco_de_dados(definicoes[2])
    tutores = abrir_Tutor(definicoes[2])

if len(tutores) == 0:
    criar_Tutor(definicoes[2], '<Desconhecio>', 123456, 1, '<nada>', '')
    tutores = abrir_Tutor(definicoes[2])

turmas = abrir_Turmas(definicoes[2])
if len(turmas) == 0:
    criar_Turma(definicoes[2], 'Todas as turmas', tutores[0][1], 0, '')
    criar_Turma(definicoes[2], 'Turma1', tutores[0][1], 1, '', ID=1001)
    turmas = abrir_Turmas(definicoes[2])

dados_dos_alunos = abrir_alunos(definicoes[2])
if len(dados_dos_alunos) == 0:
    ID = randint(1000, 9999)
    criar_aluno(definicoes[2], turmas[1][1], data, ID)
    dados_dos_alunos = abrir_alunos(definicoes_del[2])
valores = dict()
del turmas
del tutores

class Cgest:
    @staticmethod
    def message(text):
        sg.popup_quick_message(text, font='123 20')
        sleep(2)
    
    def convert_to_bytes(file_or_bytes, resize=None):
        global ident
        try:
            if isinstance(file_or_bytes, str):
                img = PIL.Image.open(file_or_bytes)
            else:
                try:
                    img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
                except Exception as e:
                    dataBytesIO = io.BytesIO(file_or_bytes)
                    img = PIL.Image.open(dataBytesIO)

            cur_width, cur_height = img.size
            if resize:
                new_width, new_height = resize
                scale = min(new_height/cur_height, new_width/cur_width)
                img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
            with io.BytesIO() as bio:
                img.save(bio, format="PNG")
                del img
                return bio.getvalue() 
        except:
            update(definicoes[2], 'alunos', 'foto', '"image1.png"', 'ID', Cgest().ident)
            file_or_bytes = 'image1.png'
            if isinstance(file_or_bytes, str):
                img = PIL.Image.open(file_or_bytes)
            else:
                try:
                    img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
                except Exception as e:
                    dataBytesIO = io.BytesIO(file_or_bytes)
                    img = PIL.Image.open(dataBytesIO)

            cur_width, cur_height = img.size
            if resize:
                new_width, new_height = resize
                scale = min(new_height/cur_height, new_width/cur_width)
                img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
            with io.BytesIO() as bio:
                img.save(bio, format="PNG")
                del img
                return bio.getvalue()   
    menu_def = ['My Menu Def', ['Volta ao Cgest','---', 'Sair do Cgest']]
    ami = sg.SystemTray(menu=menu_def, data=convert_to_bytes('image1.png', resize=(300, 300)), tooltip=' Cgest beta 1.3 ')
    ami.Hide()
    ident = None
    turma = None
    alunos = None

    class Tela_p:
        def __init__(self):
            sg.theme(definicoes[0])
            self.menu = [['Ficheiros', ['Abrir CGT', '---', 'Definições', '---', 'Sair do Cgest']],
                         ['Ajuda', ['Sobre nos']]]
            self.table = ['  Id  ', 'Nome', ' Idade ', '  Sexo  ', 'Data de nascimento', '  Turma  ',
                          'Data de inscrição', 'Número de Tel.', 'Número de Tel.2', '  Morada  ', 'Endereço e-mail']

            self.layout = [
                [sg.Menu(self.menu)],
                [sg.Text('Turmar :'),
                 sg.OptionMenu([c[1] for c in abrir_Turmas(definicoes[2])], size=(122, 1), default_value='Todas as turmas',
                               key='-ListaDeTurmas-'),
                 sg.Button('Editar turma', border_width=0, size=(15, 1), key='-EditarTurma-')],
                [sg.Text('Tutor da turma:'), sg.Text('Nenhum', key='-Tutor-', size=(100, 1))],
                [sg.Text('')],
                [sg.Text('Alunos Cadastrados:'), sg.Text(len(abrir_alunos(definicoes[2])), key='-Alnum-'), sg.Text('', size=(63, 1)),sg.Text('Pesquisar:'),
                 sg.InputText('Pesquisar por nome do aluno', border_width=0, key='-Pesq-'), sg.Button('Pesquisar', border_width=0)],
                [sg.Table(values=dados_dos_alunos[:], headings=self.table, justification='left', size=(60, 25),
                          vertical_scroll_only=False,
                          right_click_menu=['Detalhes',
                                            ['Adicionar um novo aluno', 'Ver detalhes do aluno',
                                             'Remover aluno', 'Actualizar dados']], key='-Alunos-')],
                [sg.Button('Atualizar dados', border_width=0, key='-Actualizar-'),
                 sg.Button('Remover aluno', border_width=0),
                 sg.Button('Adicionar um novo aluno', border_width=0),
                 sg.Button('Minimizar', border_width=0),
                 sg.Text('', size=(73, 1)),
                 sg.Button('Sair do Cgest', border_width=0,
                           button_color=('white', 'red'), pad=(8, 1),
                           size=(15, 2))]
            ]

            self.window = sg.Window('Cgest Beta 1.3', self.layout, size=(1240, 700),
                                    font='Calibri',finalize=True, icon='image1.ico')

        def star(self):
            global dados_dos_alunos
            while True:
                self.window.read(timeout=1)
                sg.theme(definicoes[0])
                button, values = self.window.read()
                if button in ('Sair do Cgest', None) or button == sg.WIN_CLOSED:
                    self.window.close()
                    break

                if values['-ListaDeTurmas-'] == 'Todas as turmas' and self.window['-Tutor-'] != 'Nenhum':
                    self.window.find_element('-Tutor-').update('Nenhum')
                    dados_dos_alunos = abrir_alunos(definicoes[2])
                    self.window.find_element('-Alunos-').update(values=dados_dos_alunos)
                    self.window['-Alnum-'].update(len(dados_dos_alunos))
                else:
                    for c in abrir_Turmas(definicoes[2]):
                        if c[1] == values['-ListaDeTurmas-']:
                            self.window.find_element('-Tutor-').update(c[2])
                            dados_dos_alunos = []
                            for a in abrir_alunos(definicoes[2]):
                                if a[5] == c[1]:
                                    dados_dos_alunos.append(a)
                            self.window.find_element('-Alunos-').update(values=dados_dos_alunos)
                            self.window['-Alnum-'].update(len(dados_dos_alunos))

                if True:
                    valores['NomeDaTurma'] = values['-ListaDeTurmas-']

                if button == '-Actualizar-':
                    pass
                
                elif button == '-EditarTurma-':
                    if values['-ListaDeTurmas-'] == 'Todas as turmas':
                        Cgest.message('Por favor selecione uma turma.')
                    else:
                        Cgest.turma = values['-ListaDeTurmas-']
                        self.window.Hide()
                        Cgest.Editar_turma().star()
                        self.window.UnHide()
                        dados_dos_alunos = []
                        for c in abrir_alunos(definicoes[2]):
                            if c[5] == Cgest.turma:
                                dados_dos_alunos.append(c)
                        self.window['-ListaDeTurmas-'].update(values=[c[1] for c in abrir_Turmas(definicoes[2])])
                        self.window.find_element('-Alunos-').update(values=dados_dos_alunos)

                elif button == 'Ver detalhes do aluno':
                    if not values['-Alunos-']:
                        Cgest().message('Selecione um(a) aluno(a).')
                    else:
                        Cgest.ident = None
                        Cgest.turma = values['-ListaDeTurmas-']
                        indice = [i for i in values['-Alunos-']]
                        Cgest.ident = dados_dos_alunos[indice[0]][0]
                        self.window.Hide()
                        Cgest.Alunos().star()
                        self.window.UnHide()
                        dados_dos_alunos = []
                        for c in abrir_alunos(definicoes[2]):
                            if Cgest.turma != 'Todas as turmas':
                                if c[5] == Cgest.turma:
                                    dados_dos_alunos.append(c)
                            else:
                                dados_dos_alunos.append(c)
                        self.window['-Alunos-'].Update(values=dados_dos_alunos)
                        self.window['-ListaDeTurmas-'].Update(values=[c[1] for c in abrir_Turmas(definicoes[2])])
                elif button == 'Definições':
                    self.window.Hide()
                    Cgest.Deficoes().star()
                    self.window.UnHide()
                elif button == 'Sobre nos':
                    self.window.Hide()
                    Cgest.Sobre().star()
                    self.window.UnHide()
                elif button == 'Abrir CGT':
                    self.window.Hide()
                    Cgest.Abrir().star()
                    dados_dos_alunos = abrir_alunos(definicoes[2])
                    self.window.UnHide()
                    self.window.find_element('-Alunos-').update(dados_dos_alunos)
                elif button == 'Adicionar um novo aluno':
                    if values['-ListaDeTurmas-'] == 'Todas as turmas':
                        Cgest.message('Por favor selecione uma turma.')
                    else:
                        cancela = 0
                        while cancela == 0:
                            for c in abrir_alunos(definicoes[2]):
                                id = randint(1000, 9999)
                                if c[5] == values['-ListaDeTurmas-']:
                                    if id != c[0]:
                                        criar_aluno(definicoes[2], values['-ListaDeTurmas-'], data, id)
                                        for c in abrir_Turmas(definicoes[2]):
                                            if c[1] == values['-ListaDeTurmas-']:
                                                self.window.find_element('-Tutor-').update(c[2])
                                                dados_dos_alunos = []
                                                for a in abrir_alunos(definicoes[2]):
                                                    if a[5] == c[1]:
                                                        dados_dos_alunos.append(a)
                                        self.window['-Alunos-'].Update(values=dados_dos_alunos)
                                        self.window['-Alnum-'].update(len(dados_dos_alunos))
                                        cancela = 1
                                        break
                elif button == 'Remover aluno':
                    if not values['-Alunos-']: 
                        Cgest.message('Selecione um ou varios alunos.')
                    else:
                        if values['-ListaDeTurmas-'] == 'Todas as turmas':
                            indice = [i for i in values['-Alunos-']]
                            alunos = dict()
                            for c in indice:
                                alunos[dados_dos_alunos[c][0]] = dados_dos_alunos[c][5]
                            print(alunos)
                            for ident, turma in alunos.items():
                                numero_de_alunos=[]
                                for a in abrir_alunos(definicoes[2]):
                                    if a[5] == turma:
                                        numero_de_alunos.append(a[1])
                                if len(numero_de_alunos) > 1:
                                    elimar(definicoes[2], ident, 'alunos')
                                else:
                                    Cgest.message('Não é possivel deletar o(a) ultimo(a) aluno(a).')
                            dados_dos_alunos = abrir_alunos(definicoes[2])
                            self.window.find_element('-Alunos-').update(values=dados_dos_alunos)
                            self.window['-Alnum-'].update(len(dados_dos_alunos))
                        else:
                            indice = [i for i in values['-Alunos-']]
                            print(indice)
                            numero_de_alunos=[]
                            for c in abrir_alunos(definicoes[2]):
                                        if values['-ListaDeTurmas-'] == c[5]:
                                            numero_de_alunos.append(c)
                            for c in indice:
                                if len(numero_de_alunos) > 1:
                                    elimar(definicoes[2], dados_dos_alunos[c][0], 'alunos')
                                    numero_de_alunos=[]
                                    for c in abrir_alunos(definicoes[2]):
                                        if values['-ListaDeTurmas-'] == c[5]:
                                            numero_de_alunos.append(c)
                                else:
                                    Cgest.message('Não é possivel deletar o(a) ultimo(a) aluno(a).')
                                    break
                            dados_dos_alunos = []
                            for a in abrir_alunos(definicoes[2]):
                                if a[5] == values['-ListaDeTurmas-']:
                                    dados_dos_alunos.append(a)
                            self.window.find_element('-Alunos-').update(values=dados_dos_alunos)
                            self.window['-Alnum-'].update(len(dados_dos_alunos))
                elif button == 'Pesquisar':
                    dados_dos_alunos = []
                    conte = 0
                    for c in abrir_alunos(definicoes[2]):
                        if values['-Pesq-'].lower() in c[1].lower():
                            if values['-ListaDeTurmas-'] == 'Todas as turmas':
                                dados_dos_alunos.append(c)
                                conte += 1
                            else:
                                if c[5] == values['-ListaDeTurmas-']:
                                    dados_dos_alunos.append(c)
                                    conte += 1
                    if conte == 0:
                        Cgest.message('Nenhum(a) aluno(a) encontrado(a).')
                    self.window.find_element('-Alunos-').update(values=dados_dos_alunos)
                    self.window['-Alnum-'].update(len(dados_dos_alunos))

                elif button == 'Minimizar':
                    visi_janela = False
                    self.window.Hide()
                    Cgest.ami.UnHide()
                    visi_janela = True
                    closed = False
                    if visi_janela:
                        while True:
                            menu_item = Cgest.ami.Read()
                            if menu_item == 'Volta ao Cgest' or menu_item == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
                                Cgest.ami.Hide()
                                visi_janela = False
                                self.window.UnHide()
                                break
                            elif menu_item == 'Sair do Cgest':
                                Cgest.ami.Hide()
                                visi_janela = False
                                self.window.close()
                                closed = True
                                break
                                
    class Editar_turma:
        def __init__(self):
            self.iden1 = None
            self.iden2 = None 
            self.maior = 0
            cont = 0
            for c in abrir_Turmas(definicoes[2]):
                if cont == 1:
                    self.maior = c[3]
                elif cont > 1:
                    if self.maior < c[3]:
                        self.maior = c[3]
                cont += 1

            self.layout_1 = [
                [sg.Button('Adicionar uma turma', border_width=0)],
                [sg.Text('Editar nome da turma: '), sg.Combo([c[1] for c in abrir_Turmas(definicoes[2])[1:]], size=(43, 1),
                                                             key='-NDT-', default_value=valores['NomeDaTurma'])],
                [sg.Text('Tutor da turma: '), sg.OptionMenu([c[1] for c in abrir_Tutor(definicoes[2])], size=(46, 1),
                                                            key='-TDT-')],
                [sg.Checkbox('Definir classificação da turma', key='-CLASS-'),
                 sg.Spin([c for c in range(1, self.maior + 1)], size=(6, 1), key='-Num-', disabled=True)],
                [sg.Text('Detalhes da turma.')],
                [sg.MLine('', size=(48, 7), key='-DETALHE-'),
                 sg.Column([[sg.Frame('', [
                     [sg.Button('Atulizar', size=(13, 1), border_width=0)],
                     [sg.Button('Eliminar Turma', size=(13, 1), border_width=0)],
                     [sg.Button('Editar', size=(13, 1), border_width=0)],
                     [sg.Button('Cancelar', border_width=0, size=(13, 1))]], border_width=0, key='-LAY1-')]])]
            ]
            self.layout_2 = [
                [sg.Button('Adicionar um tutor', border_width=0)],
                [sg.Text('Editar nome da tutor:'), sg.Combo([a[1] for a in abrir_Tutor(definicoes[2])], size=(44, 1), key='-NT-')],
                [sg.Text('Número de tel.:'), sg.Input('', size=(51, 1), border_width=0, key='-NUME-')],
                [sg.Text('Sexo:'),
                 sg.Radio('Masculino', 3, key='-SEX1-'), sg.Radio('Feminino', 3, key='-SEX2-')],
                [sg.Text('Professor de:'), sg.Input('', border_width=0, size=(53, 1), key='-PD-')],
                [sg.Text('Detalhes do tutor.')],
                [sg.MLine('', size=(48, 6), key='-ALL-'),
                 sg.Column([[sg.Frame('', [
                     [sg.Button('Atualizar', size=(13, 1), border_width=0, key='-atua-')],
                     [sg.Button('Eliminar tutor', size=(13, 1), border_width=0, key='-elim-')],
                     [sg.Button('Editar dados', size=(13, 1), border_width=0, key='-EDIT-')]],
                                      border_width=0)]])]]
            self.layout_5 = [[sg.Tab('Turma', self.layout_1)],
                             [sg.Tab('Editar dados do Tutor', self.layout_2)],
                             ]
            self.layout = [[sg.TabGroup(self.layout_5)]]
            self.window = sg.Window('Turma/Tutor', self.layout, size=(509, 300), margins=(0, 0), icon='image1.ico')

        def star(self):
            while True:
                botton, values = self.window.read()
                if botton in ('Cancelar', '-Sair-', None, sg.WIN_CLOSED):
                    self.window.close()
                    break
                if not values['-CLASS-']:
                    self.window['-Num-'].update(disabled=True)
                else:
                    self.window['-Num-'].update(disabled=False)
                    self.window['-CLASS-'].update(True)
                if botton == 'Atulizar' or botton == 'Eliminar Turma':
                    for c in abrir_Turmas(definicoes[2]):
                        if c[1] == values['-NDT-']:
                            self.iden1 = c[0]
                            self.window['-NDT-'].update(c[1])
                            lista = [c[2]]
                            for a in abrir_Tutor(definicoes[2]):
                                if a[1] != c[2]:
                                    lista.append(a[1])
                            self.window['-TDT-'].update(values=lista)
                            self.window['-NT-'].update(values['-TDT-'])
                            self.window['-NT-'].update(values=lista)
                            del lista
                            self.window['-Num-'].update(c[3])
                            self.window['-DETALHE-'].update(c[4])
                            if not values['-CLASS-']:
                                self.window['-CLASS-'].update(False)
                            else:
                                self.window['-CLASS-'].update(True)
                            for a in abrir_Tutor(definicoes[2]):
                                if a[1] == values['-TDT-']:
                                    self.iden2 = a[0]
                                    self.window['-NUME-'].update(a[2])
                                    if a[3] == 1:
                                        self.window['-SEX1-'].update(True)
                                    else:
                                        self.window['-SEX2-'].update(True)
                                    self.window['-PD-'].update(a[4])
                                    self.window['-ALL-'].update(a[5])
                # Opção para adicionar uma turma
                if botton == 'Adicionar uma turma':
                        cancela = 0
                        while cancela == 0:
                            for c in abrir_Turmas(definicoes[2]):
                                # Criando um id para turma.
                                id = randint(1000, 9999)
                                # Verificando se existe um id parecido para não gerar erro no programa.
                                if id != c[0]:
                                    # Verificando se existe uma turma com o mesmo nome para não gerar erro no programa.
                                    if values['-NDT-'] not in [f[1] for f in abrir_Turmas(definicoes[2])]:
                                        criar_Turma(definicoes[2], f'Nenhum nome definido {self.maior + 1}'
                                        if values['-NDT-'] == ''
                                        else values['-NDT-'], values['-TDT-'],
                                                    int(values['-Num-']) if values['-CLASS-'] else self.maior + 1, values['-DETALHE-'], ID=id)
                                        criar_aluno(definicoes[2],
                                                    f'Nenhum nome definido {self.maior + 1}'
                                                    if values['-NDT-'] == ''
                                                    else values['-NDT-'].title().strip(), data, id)
                                        cancela = 1
                                        break
                                    # Se já existir uma turma com o mesmo nome o programa dá-nos um mensagem.
                                    else:
                                        self.window['-NDT-'].update('')
                                        Cgest.message('Esta turma já existe')
                                        cancela = 1
                                        break
                        self.window['-NDT-'].update(values=[c[1] for c in abrir_Turmas(definicoes[2])[1:]])
                        self.maior = 0
                        cont = 0
                        for c in abrir_Turmas(definicoes[2]):
                            if cont == 1:
                                self.maior = c[3]
                            elif cont > 1:
                                if self.maior < c[3]:
                                    self.maior = c[3]
                            cont += 1
                        self.window['-Num-'].update(values=[c for c in range(1, self.maior + 1)])
                # Opção para elinminar uma turma.
                elif botton == 'Eliminar Turma':
                    if values['-NDT-'] == '' or len(abrir_Turmas(definicoes[2])[1:]) == 1:
                        Cgest.message('Nome não definido' if values['-NDT-'] == '' else 'Operação invalida')
                    else:
                        for c in abrir_Turmas(definicoes[2]):
                            if c[1] == values['-NDT-']:
                                for k in abrir_Turmas(definicoes[2]):
                                    # Actulizar as classifições de todas as turmas.
                                    if c[3] < k[3]:
                                        update(definicoes[2], 'turmas', 'class', k[3] - 1, 'ID', k[0])
                                for d in abrir_alunos(definicoes[2]):
                                    if c[1] == d[5]:
                                        elimar(definicoes[2], d[0], 'alunos')
                                elimar(definicoes[2], c[0], 'turmas')
                                break
                        self.window['-NDT-'].update(values=[c[1] for c in abrir_Turmas(definicoes[2])[1:]])
                        self.window['-NDT-'].update('')
                        self.window['-TDT-'].update(tutores[0][1])
                        self.window['-Num-'].update('')
                        self.window['-DETALHE-'].update('')
                        if not values['-CLASS-']:
                            self.window['-CLASS-'].update(False)
                        else:
                            self.window['-CLASS-'].update(True)
                elif botton == 'Editar':
                    for c in abrir_Turmas(definicoes[2]):
                        if self.iden1 == c[0]:
                            if '' != values['-NDT-'] not in [f[1] if f[1] != c[1] else 'blaaaa' for f in abrir_Turmas(definicoes[2])]:
                                for k in abrir_alunos(definicoes[2]):
                                    # Actulizar a turma de todas os alunos.
                                    if c[1] == k[5]:
                                        update(definicoes[2], 'alunos', 'turma', '"{}"'.format(values['-NDT-'].title().strip()), 'ID', k[0])
                                update(definicoes[2], 'turmas', 'nome', '"{}"'.format(values['-NDT-'].title().strip()), 'ID', c[0])
                                update(definicoes[2], 'turmas', 'tutor', '"{}"'.format(values['-TDT-']), 'ID', c[0])
                                update(definicoes[2], 'turmas', 'class', int(values['-CLASS-'])
                                    if values['-CLASS-']
                                    else c[3], 'ID', c[0])
                                update(definicoes[2], 'turmas', 'detalhes', '"{}"'.format(values['-DETALHE-']), 'ID', c[0])
                                self.window['-NDT-'].update(values=[c[1] for c in abrir_Turmas(definicoes[2])[1:]])
                                break
                            else:
                                Cgest.message('Erro: não introduziu nenhum nome' if values['-NDT-'] == '' 
                                              else 'Esta turma já existe')
                                self.window['-NDT-'].update('')
                                cancela = 1
                                break
                elif botton == 'Adicionar um tutor':
                    cancela = 0
                    while cancela == 0:
                        for c in abrir_Tutor(definicoes[2]):
                            # Criando um id para tutor.
                            id = randint(1000, 9999)
                             # Verificando se existe um id parecido para não gerar erro no programa.
                            if id != c[0]:
                                 # Verificando se existe um tutor com o mesmo nome para não gerar erro no programa.
                                if '' != values['-NT-'] not in [f[1] for f in abrir_Tutor(definicoes[2])]:
                                    if values['-SEX1-'] or values['-SEX2-']:
                                        # Criando um tutor apartir das informações introduzidas pelo usuário. 
                                        criar_Tutor(definicoes[2], values['-NT-'].title().strip(), values['-NUME-'], 1 if values['-SEX1-'] else 2,
                                        values['-PD-'], values['-ALL-'],ID=id)  
                                        cancela = 1
                                        self.window['-NT-'].update(values=[f[1] for f in abrir_Tutor(definicoes[2])])
                                        self.window['-TDT-'].update(values=[f[1] for f in abrir_Tutor(definicoes[2])])
                                        break
                                    else:
                                        # Criando um tutor apartir das informações introduzidas pelo usuário.
                                        criar_Tutor(definicoes[2], values['-NT-'].title().strip(), values['-NUME-'], 1,
                                        values['-PD-'], values['-ALL-'],ID=id)   
                                        cancela = 1
                                        self.window['-NT-'].update(values=[f[1] for f in abrir_Tutor(definicoes[2])])
                                        self.window['-TDT-'].update(values=[f[1] for f in abrir_Tutor(definicoes[2])])
                                        break 
                                else:
                                    Cgest.message('Erro: não introduziu nenhum nome' if values['-NT-'] == '' 
                                    else 'Este tutor já existe')
                                    self.window['-NT-'].update('')
                                    cancela = 1
                                    break
                                
                elif botton == '-atua-':
                    for a in abrir_Tutor(definicoes[2]):
                        if a[1] == values['-NT-']:
                            self.iden2 = a[0]
                            self.window['-NUME-'].update(a[2])
                            if a[3] == 1:
                                self.window['-SEX1-'].update(True)
                            else:
                                self.window['-SEX2-'].update(True)
                            self.window['-PD-'].update(a[4])
                            self.window['-ALL-'].update(a[5])
                            self.window['-NT-'].update(values=[f[1] for f in abrir_Tutor(definicoes[2])])
                            self.window['-TDT-'].update(values=[f[1] for f in abrir_Tutor(definicoes[2])])
                elif botton == '-EDIT-':
                    for c in abrir_Tutor(definicoes[2]):
                        print(self.iden2)
                        if self.iden2 == c[0]:
                            print(self.iden2, c[0])
                            if '' != values['-NT-'] not in [f[1] if f[1] != c[1] else 'blaaaa' for f in abrir_Tutor(definicoes[2])]:
                                for k in abrir_Turmas(definicoes[2]):
                                    # Actulizar o tutor para todas as turmas.
                                    if c[1] == k[2]:
                                        update(definicoes[2], 'turmas', 'tutor', '"{}"'.format(values['-NT-'].title().strip()), 'ID', k[0])
                                update(definicoes[2], 'tutor', 'nome', '"{}"'.format(values['-NT-'].title().strip()), 'ID', c[0])
                                update(definicoes[2], 'tutor', 'numero', '"{}"'.format(values['-NUME-']), 'ID', c[0])
                                update(definicoes[2], 'tutor', 'sexo', 1
                                    if values['-SEX1-']
                                    else 2, 'ID', c[0])
                                update(definicoes[2], 'tutor', 'aulas', '"{}"'.format(values['-PD-']), 'ID', c[0])
                                update(definicoes[2], 'tutor', 'detalhes', '"{}"'.format(values['-ALL-']), 'ID', c[0])
                                self.window['-NT-'].update(values=[c[1] for c in abrir_Tutor(definicoes[2])])
                                self.window['-TDT-'].update(values=[c[1] for c in abrir_Tutor(definicoes[2])])
                                break
                            else:
                                Cgest.message('Erro: não introduziu nenhum nome' if values['-NDT-'] == '' 
                                              else 'Este(a) tutor(a) já existe')
                                self.window['-NT-'].update('')
                                cancela = 1
                                break
                
                elif botton == '-elim-':
                    if values['-NT-'] == '' or len(abrir_Tutor(definicoes[2])) == 1:
                        Cgest.message('Nome não definido' if values['-NDT-'] == '' else 'Operação invalida')
                    else:
                        for c in abrir_Tutor(definicoes[2]):
                            if c[1] == values['-NT-']:
                                for k in abrir_Tutor(definicoes[2]):
                                    # Actulizar as classifições de todas as turmas.
                                    if c[1] != k[1]:
                                        for g in abrir_Turmas(definicoes[2]):
                                            if g[2] == c[1]:
                                                update(definicoes[2], 'turmas', 'tutor', '"{}"'.format(k[1]), 'ID', g[0])
                                                break
                                        break
                                elimar(definicoes[2], c[0], 'tutor')
                                break
                    self.window['-NT-'].update(values=[f[1] for f in abrir_Tutor(definicoes[2])])
                    self.window['-TDT-'].update(values=[f[1] for f in abrir_Tutor(definicoes[2])])

    class Alunos:
        def __init__(self):
            self.aluno = None
            self.lista = None
            self.image = None
            for c in abrir_alunos(definicoes[2]):
                if c[0] == Cgest.ident:
                    self.aluno = c
                    self.image = c[12]
                    break
                #sg.Image(size=(300, 300), data=Cgest.convert_to_bytes(self.aluno[12], (500,300)),
            self.layout_1 = [
                [sg.Column([[sg.Frame('Foto de perfil',[[sg.Image(size=(300, 300), data=Cgest.convert_to_bytes(self.aluno[12], (500,300)),
                                                    background_color='black',key='-FotoDePerfil-', tooltip=r' {} '.format(self.aluno[12]))],
                                                        [sg.Button('Pré-visualizar a imagem', size=(37, 1))]])]]),
                 sg.Column([[sg.Frame('', [
                     [sg.Text(f'{self.aluno[1]}' if len(self.aluno[1]) < 19 else f'{self.aluno[1][:19]}...', font='Calibri 30', tooltip=f' {self.aluno[1]} ', key='-TITULO-')],
                     [sg.FilesBrowse('Carregar uma foto', file_types=(('Png', '.png'), ('Jpng', '.jpg')), key='-PesFoto-'),
                      sg.Button('Repor a imagem padrão'), sg.Button('Atualizar'), sg.Button('Editar dados')],
                     [sg.Text('ID do(a) aluno(a):'), sg.Text(f'{Cgest.ident}', key='-ID-')],
                     [sg.Text('Nome do(a) aluno(a):'), sg.InputText(self.aluno[1],
                                                              border_width=0, size=(50, 1), key='-Nome-')],
                     [sg.Text('Idade atual:'), sg.InputText(self.aluno[2], border_width=0, size=(50, 1), key='-Idade-')],
                     [sg.Text('Data de nascimento:'), sg.InputText(self.aluno[4], border_width=0, size=(47, 1), key='-Nasci-')],
                     [sg.Text('Número de telefone 1:'), sg.InputText(self.aluno[7], border_width=0, key='-Num1-')],
                     [sg.Text('Número de telefone 2:'), sg.InputText(self.aluno[8], border_width=0, key='-Num2-')],
                     [sg.Text('Turma:'), sg.Text('', size=(11, 1)), sg.Text(self.aluno[5], key='-Turma-')],
                     [sg.Text('E-mail:'), sg.InputText(self.aluno[10], size=(57, 1), border_width=0, key='-Email-')],
                     [sg.Text('Morada:'), sg.InputText(self.aluno[9], size=(57, 1), border_width=0, key='-Morada-')],
                     [sg.Text('Sexo do(a) aluno(a):'), sg.Radio('Masculino', 1, True if self.aluno[3] == 'Masculino' else False, key='-SEX1-'), sg.Radio('Feminino', 1, True if self.aluno[3] == 'Feminino' else False, key='-SEX2-')]
                 ], border_width=0)]])],
                [sg.Text('Detalhes adicionas do(a) aluno(a)')],
                [sg.MLine(self.aluno[11], size=(100, 8), key='-Detalhe-')]
            ]
            self.window = sg.Window('Detalhes do aluno', self.layout_1, margins=(0, 0),
                                    size=(850, 620), element_justification='center', 
                                    font='Calibri 12', icon='image1.ico')

        def star(self):
            global dados_dos_alunos
            while True:
                button, values = self.window.read()
                if button in (None, sg.WIN_CLOSED):
                    self.window.close()
                    break
                if button == 'Pré-visualizar a imagem':
                    if values['-PesFoto-']:
                        self.image = values['-PesFoto-']
                        self.window['-FotoDePerfil-'].Update(data=Cgest.convert_to_bytes(r'{}'.format(self.image), (500, 300)), size=(300, 300))
                if button == 'Atualizar':
                    for c in dados_dos_alunos:
                        if c[0] == Cgest.ident:
                            self.window['-TITULO-'].Update(f'{c[1]}' if len(c[1]) < 19 else f'{c[1][:19]}...')
                            self.window['-FotoDePerfil-'].Update(data=Cgest.convert_to_bytes(r'{}'.format(c[12]), (500, 300)), size=(300, 300))
                            self.window['-Nome-'].Update(c[1])
                            self.window['-Idade-'].Update(c[2])
                            self.window['-Nasci-'].Update(c[4])
                            self.window['-Num1-'].Update(c[7])
                            self.window['-Num2-'].Update(c[8])
                            self.window['-Email-'].Update(c[10])
                            self.window['-Morada-'].Update(c[9])
                            if c[3] == 'Masculino':
                                self.window['-SEX1-'].Update(True)
                            else:
                                self.window['-SEX2-'].Update(True)
                            self.window['-Detalhe-'].Update(c[11])
                            self.image = c[12]
                if button == 'Editar dados':
                    update(definicoes[2], 'alunos', 'nome', '"{}"'.format(values['-Nome-'].strip().title()) if values['-Nome-'] else '"<Desconhecido>"', 'ID', Cgest().ident)
                    update(definicoes[2], 'alunos', 'data1', '"{}"'.format(values['-Nasci-'].strip()) if values['-Nasci-'] else '"11/03/2011"', 'ID', Cgest().ident)
                    update(definicoes[2], 'alunos', 'email', '"{}"'.format(values['-Email-'].strip().capitalize()) if values['-Email-'] else '"Nada"', 'ID', Cgest().ident)
                    update(definicoes[2], 'alunos', 'morada', '"{}"'.format(values['-Morada-'].strip().title()) if values['-Morada-'] else '"Nada"', 'ID', Cgest().ident)
                    update(definicoes[2], 'alunos', 'sexo', '"Masculino"' if values['-SEX1-'] else '"Feminino"', 'ID', Cgest().ident)
                    update(definicoes[2], 'alunos', 'detalhes', '"{}"'.format(values['-Detalhe-']), 'ID', Cgest().ident)
                    update(definicoes[2], 'alunos', 'foto', r'"{}"'.format(self.image), 'ID', Cgest().ident)
                    try:    
                        update(definicoes[2], 'alunos', 'numero1', int(values['-Num1-'].strip()), 'ID', Cgest().ident)
                        update(definicoes[2], 'alunos', 'numero2', int(values['-Num2-'].strip()), 'ID', Cgest().ident)
                    except:
                        Cgest.message('verifique o número de telefone 1 ou 2 ')
                    try:    
                        update(definicoes[2], 'alunos', 'idade', int(values['-Idade-'].strip()), 'ID', Cgest().ident)
                    except:
                        Cgest.message('verifique a idade')
                    dados_dos_alunos = abrir_alunos(definicoes[2])
                
    class Deficoes:
        def __init__(self):
            self.layout = [
                [sg.Text('Defina a lingua:'), sg.OptionMenu(['Português', 'Inglês', 'Francês'],
                                                       size=(23, 1), default_value=definicoes[1])],
                [sg.Text('Defina um Tema:'), sg.OptionMenu(['TanBlue', 'LightGreen3', 'LightBlue3',
                                                       'GreenTan', 'GreenMono', 'DarkTeal9', 'LightBrown11',
                                                       'LightGrey6',
                                                       'LightGreen2', 'DarkBlue3', 'LightGrey3'],
                                                      size=(22, 1), default_value=definicoes[0], key='-CorDeFundo-')],
                [sg.Button('Salvar', border_width=0, size=(10, 2)), sg.Button('Cancelar', border_width=0, size=(10, 2))]
            ]
            self.Window = sg.Window('Definições', self.layout, element_justification='center', icon='image1.ico')

        def star(self):
            while True:
                button, value = self.Window.read()
                if button in (None, 'Salvar', 'Cancelar', sg.WIN_CLOSED):
                    if button == 'Salvar':
                        lista_de_tema = ['TanBlue', 'LightGreen3', 'LightBlue3', 'GreenTan', 'GreenMono', 'DarkTeal9',
                                         'LightBrown11', 'LightGrey6', 'LightGreen2', 'DarkBlue3', 'LightGrey3']
                        while True:
                            if value['-CorDeFundo-'] in lista_de_tema:
                                definicoes[0] = value['-CorDeFundo-']
                                salvar(nomed, definicoes, chave)
                                Cgest.message('Por favor reinicie o programa')
                                break
                            elif value['-CorDeFundo-'] not in lista_de_tema:
                                Cgest.message('Por favor introduze um tema valido')
                                break
                            elif button == 'Cancelar':
                                break
                        sg.theme(definicoes[0])
                    self.Window.close()
                    break

    class Sobre:
        def __init__(self):
            self.layout = [[sg.Text('Cgest Beta 1.3 é sistema de greciemento\n'
                                    'alunos de uma escola.'
                                    '\nTodos os direito reservados a Canc Design.\n'
                                    'Programado por: Clement Alberto N. Cazadi.\n'
                                    'Agradecimento especial:'
                                    '\nGustavo guanabara.'
                                    '\nAlison pares.'
                                    '\nRamiro Ngando.\nEntre em contacto com agente em:\n'
                                    'Www.facebook.com/CANC-design')], [sg.Button('Ok', border_width=0, size=(6, 2))]]
            self.window = sg.Window('About', self.layout, element_justification='center', disable_minimize=True, icon='image1.ico')

        def star(self):
            while True:
                button, value = self.window.read()
                if button in (None, 'Ok', sg.WIN_CLOSED):
                    self.window.close()
                    break

    class Abrir:
        def __init__(self):
            self.layout = [[sg.Text(f'Arquivo de dados actual: {definicoes[2]}')],
                           [sg.Text('Precure pelo diretorio do arquivo cgt'), sg.Text('', size=(21, 1))],
                           [sg.InputText('', border_width=0, key='-Caminho-'),
                            sg.FilesBrowse('Procurar', file_types=(('Arquivos Cgest (.cgt)', '.cgt'),),
                                           key='-Procurar-')],
                           [sg.Button('Conluir', border_width=0, size=(13, 2))]
                           ]
            self.window = sg.Window('Abrir CGT', self.layout, element_justification='center', disable_minimize=True, icon='image1.ico')

        def star(self):
            while True:
                global tente
                button, value = self.window.read()
                if button in (None, 'Conluir', sg.WIN_CLOSED):
                    if button == 'Conluir':
                        try:
                            # verificando se o arquivo existe.
                            tente = open(value['-Caminho-'], 'r')
                            tente.close()
                            # verificando se o banco de dados e valido ou operaçional
                            tente = banco_de_dados(value['-Caminho-'], tente=True)
                            if tente:
                                definicoes[2] = value['-Caminho-']
                                salvar(nomed, definicoes, chave)
                            if not tente:
                                pass
                        except:
                            Cgest.message('O arquivo não existe.')
                        self.window.close()
                    break
                if value['-Procurar-']:
                    self.window.find_element('-Caminho-').update(value['-Procurar-'])

Cgest().Tela_p().star()
#Cgest().Alunos().star()
