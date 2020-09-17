from back import *
from datetime import datetime

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
ID_dos_alunos = abrir_ID(definicoes[2])
valores = dict()


class Cgest:
    @staticmethod
    def message(text):
        sg.popup_quick_message(text, font='123 20')
        sleep(2)


    class Tela_p:
        global turmas

        def __init__(self):
            sg.theme(definicoes[0])
            self.menu = [['Ficheiros', ['Abrir CGT', '---', 'Definições', '---', 'Sair do Cgest']],
                         ['Ajuda', ['Sobre nos']]]
            self.table = ['  Id  ', 'Nome', ' Idade ', '  Sexo  ', 'Data de nascimento', '  Turma  ',
                          'Data de inscrição', 'Número de Tel.', 'Número de Tel.2', '  Morada  ', 'Endereço e-mail']

            self.layout = [
                [sg.Menu(self.menu)],
                [sg.Text('Turmar :'),
                 sg.OptionMenu([c[1] for c in turmas], size=(122, 1), default_value='Todas as turmas',
                               key='-ListaDeTurmas-'),
                 sg.Button('Editar turma', border_width=0, size=(15, 1), key='-EditarTurma-', disabled=True)],
                [sg.Text('Tutor da turma:'), sg.Text('Nenhum', key='-Tutor-', size=(100, 1))],
                [sg.Text('')],
                [sg.Text('Alunos Cadastrados'), sg.Text('Nenhum', size=(7, 1)),
                 sg.Text('Ordena por:'), sg.Combo(['Nome', 'Idade', 'Id', 'Data de inscrição'], default_value='Nome'),
                 sg.Text('Pesquisar:'),
                 sg.InputText('Pesquisar por nome do aluno', border_width=0)],
                [sg.Table(values=dados_dos_alunos[:], headings=self.table, justification='left', size=(60, 25),
                          vertical_scroll_only=False,
                          right_click_menu=['Detalhes',
                                            ['Ver detalhes do aluno', 'Passar aluno para Turma seginte',
                                             'Remover aluno', 'Actualizar dados']], key='-Alunos-')],
                [sg.Button('Actualizar dados', border_width=0, key='-Actualizar-'),
                 sg.Button('Remover aluno', border_width=0),
                 sg.Button('Adicionar um novo aluno', border_width=0),
                 sg.Text('', size=(83, 1)),
                 sg.Button('Sair do Cgest', border_width=0,
                           button_color=('white', 'red'), pad=(8, 1),
                           size=(15, 2))]
            ]

            self.window = sg.Window('Cgest Beta 1.3', self.layout, size=(1240, 700),
                                    font='Calibri',
                                    right_click_menu=['Actualizar dados', ['Editar turma', 'Adicionar um novo aluno',
                                                                           'Editar o tutor da sala', 'Sair do Cgest']],
                                    finalize=True)

        def star(self):
            global turmas, dados_dos_alunos, ID_dos_alunos
            while True:
                self.window.read(timeout=1)
                sg.theme(definicoes[0])
                button, values = self.window.read()
                if button in ('Sair do Cgest', None) or button == sg.WIN_CLOSED:
                    self.window.close()
                    break

                if values['-ListaDeTurmas-'] == 'Todas as turmas' and self.window['-Tutor-'] != 'Nenhum':
                    self.window.find_element('-Tutor-').update('Nenhum')
                    self.window['-EditarTurma-'].update(disabled=True)

                else:
                    for c in turmas:
                        if c[1] == values['-ListaDeTurmas-']:
                            self.window.find_element('-Tutor-').update(c[2])
                            self.window['-EditarTurma-'].update(disabled=False)
                if True:
                    dados_dos_alunos = abrir_alunos(definicoes[2])
                    ID_dos_alunos = abrir_ID(definicoes[2])
                    self.window.find_element('-Alunos-').update(values=dados_dos_alunos)
                    valores['NomeDaTurma'] = values['-ListaDeTurmas-']

                if button == '-EditarTurma-':
                    if values['-ListaDeTurmas-'] == 'Todas as turmas':
                        Cgest.message('Por favor selecione uma turma')
                    else:
                        self.window.Disable()
                        Cgest.Editar_turma().star()
                        self.window.Enable()
                        dados_dos_alunos = abrir_alunos(definicoes[2])
                        turmas = abrir_Turmas(definicoes[2])
                        ID_dos_alunos = abrir_ID(definicoes[2])
                        self.window['-ListaDeTurmas-'].update(values=[c[1] for c in turmas])
                        self.window.find_element('-Alunos-').update(values=dados_dos_alunos)

                elif button == 'Ver detalhes do aluno':
                    self.window.Disable()
                    Cgest.Alunos().star()
                    self.window.Enable()
                    dados_dos_alunos = abrir_alunos(definicoes[2])
                    self.window['-Alunos-'].Update(values=dados_dos_alunos)
                elif button == 'Definições':
                    self.window.Disable()
                    Cgest.Deficoes().star()
                    self.window.Enable()
                elif button == 'Sobre nos':
                    self.window.Disable()
                    Cgest.Sobre().star()
                    self.window.Enable()
                elif button == 'Abrir CGT':
                    self.window.Disable()
                    Cgest.Abrir().star()
                    dados_dos_alunos = abrir_alunos(definicoes[2])
                    self.window.Enable()
                    self.window.find_element('-Alunos-').update(dados_dos_alunos)
                elif button == 'Adicionar um novo aluno':
                    if values['-ListaDeTurmas-'] == 'Todas as turmas':
                       Cgest.message('Por favor selecione uma turma')
                    else:
                        cancela = 0
                        while cancela == 0:
                            for c in ID_dos_alunos:
                                id = randint(1000, 9999)
                                if c[1] == values['-ListaDeTurmas-']:
                                    if id != c[0]:
                                        criar_aluno(definicoes[2], values['-ListaDeTurmas-'], data, id)
                                        dados_dos_alunos = abrir_alunos(definicoes[2])
                                        self.window['-Alunos-'].Update(values=dados_dos_alunos)
                                        cancela = 1
                                        break
                elif button == 'Remover aluno':
                    r = values['-Alunos-'][:][:]
                    print(r)
                    if not values['-Alunos-']:
                        Cgest.message('Selecione um ou varios alunos.')

                    
    class Editar_turma:
        def __init__(self):
            self.maior = 0
            cont = 0
            for c in ID_Turmas(definicoes[2]):
                if cont == 1:
                    self.maior = c[2]
                elif cont > 1:
                    if self.maior < c[2]:
                        self.maior = c[2]
                cont += 1

            self.layout_1 = [
                [sg.Radio('Editar Turmar', 1, True, key='-EDT-'),
                 sg.Radio('Adicionar uma nova turma', 1, key='-ADT-'), sg.Text('', size=(6, 1)),
                 sg.Button('Adicionar uma turma', border_width=0)],
                [sg.Text('Editar nome da turma: '), sg.Combo([c[1] for c in turmas[1:]], size=(43, 1),
                                                             key='-NDT-', default_value=valores['NomeDaTurma'])],
                [sg.Text('Tutor da turma: '), sg.OptionMenu([c[1] for c in tutores[:]], size=(46, 1),
                                                            key='-TDT-', default_value=tutores[0][1])],
                [sg.Checkbox('Definir classificação da turma', key='-CLASS-'),
                 sg.Spin([c for c in range(1, self.maior + 1)], size=(6, 1), key='-Num-', disabled=True)],
                [sg.Text('Detalhes da turma.')],
                [sg.MLine('', size=(48, 7), key='-DETALHE-'),
                 sg.Column([[sg.Frame('', [
                     [sg.Button('Actulizar', size=(13, 1), border_width=0)],
                     [sg.Button('Eliminar Turma', size=(13, 1), border_width=0)],
                     [sg.Button('Editar', size=(13, 1), border_width=0)],
                     [sg.Button('Cancelar', border_width=0, size=(13, 1))]], border_width=0)]])]
            ]
            self.layout_2 = [
                [sg.Radio('Editar Tutor', 2, True),
                 sg.Radio('Adicionar um novo tutor', 2), sg.Text('', size=(11, 1)),
                 sg.Button('Adicionar um tutor', border_width=0)],
                [sg.Text('Editar nome da tutor:'), sg.Combo(['nomes'], size=(44, 1))],
                [sg.Text('Número de tel.:'), sg.Input('nomes', size=(51, 1), border_width=0)],
                [sg.Text('Sexo:'),
                 sg.Radio('Masculino', 3), sg.Radio('Feminino', 3)],
                [sg.Text('Professor de:'), sg.Input('', border_width=0, size=(53, 1))],
                [sg.Text('Detalhes da turma.')],
                [sg.MLine('', size=(48, 6)),
                 sg.Column([[sg.Frame('', [
                     [sg.Button('Eliminar tutor', size=(13, 1), border_width=0)],
                     [sg.Button('Editar', size=(13, 1), border_width=0)],
                     [sg.Button('Cancelar', border_width=0, size=(13, 1), key='-Sair-')]],
                                      border_width=0)]])]]
            self.layout_5 = [[sg.Tab('Turma', self.layout_1)],
                             [sg.Tab('Editar dados do Tutor', self.layout_2)],
                             ]
            self.layout = [[sg.TabGroup(self.layout_5)]]
            self.window = sg.Window('Turma/Tutor', self.layout, size=(509, 300), margins=(0, 0))

        def star(self):
            global turmas
            while True:
                botton, values = self.window.read()
                print(botton, values)
                if botton in ('Cancelar', '-Sair-', None, sg.WIN_CLOSED):
                    self.window.close()
                    break
                if not values['-CLASS-']:
                    self.window['-Num-'].update(disabled=True)
                else:
                    self.window['-Num-'].update(disabled=False)
                    self.window['-CLASS-'].update(True)
                if botton == 'Actulizar' or botton == 'Eliminar Turma' and values['-EDT-']:
                    if values['-EDT-']:
                        for c in turmas:
                            if c[1] == values['-NDT-']:
                                print(c)
                                self.window['-NDT-'].update(c[1])
                                self.window['-TDT-'].update(c[2])
                                self.window['-Num-'].update(c[3])
                                self.window['-DETALHE-'].update(c[4])
                                if not values['-CLASS-']:
                                    self.window['-CLASS-'].update(False)
                                else:
                                    self.window['-CLASS-'].update(True)

                if botton == 'Adicionar uma turma':
                    if values['-EDT-']:
                        sg.popup_quick_message('Por favor va para a opção ADICIONAR UMA TURMA', font='123 15')
                        sleep(2)
                    else:
                        cancela = 0
                        while cancela == 0:
                            for c in ID_Turmas(definicoes[2]):
                                id = randint(1000, 9999)
                                if id != c[0]:
                                    if values['-NDT-'] not in [f[1] for f in ID_Turmas(definicoes[2])]:
                                        if values['-CLASS-']:
                                            criar_Turma(definicoes[2], f'Nenhum nome definido {self.maior + 1}'
                                                        if values['-NDT-'] == ''
                                                        else values['-NDT-'], values['-TDT-'],
                                                        int(values['-Num-']), values['-DETALHE-'], ID=id)
                                            criar_aluno(definicoes[2],
                                                        f'Nenhum nome definido {self.maior + 1}'
                                                        if values['-NDT-'] == ''
                                                        else values['-NDT-'], data, id)
                                            cancela = 1
                                        elif not values['-CLASS-']:
                                            criar_Turma(definicoes[2],
                                                        f'Nenhum nome definido {self.maior + 1}'
                                                        if values['-NDT-'] == ''
                                                        else values['-NDT-'], values['-TDT-'],
                                                        self.maior + 1,
                                                        values['-DETALHE-'], ID=id)
                                            criar_aluno(definicoes[2],
                                                        f'Nenhum nome definido {self.maior + 1}'
                                                        if values['-NDT-'] == ''
                                                        else values['-NDT-'], data, id)
                                            cancela = 1
                                            break

                                    else:
                                        self.window['-NDT-'].update('')
                                        sg.popup_quick_message('Esta turma já existe', font='123 15')

                                        sleep(2)
                                        cancela = 1
                                        break
                        turmas = abrir_Turmas(definicoes[2])
                        self.window['-NDT-'].update(values=[c[1] for c in turmas[1:]])
                        self.maior = 0
                        cont = 0
                        for c in ID_Turmas(definicoes[2]):
                            if cont == 1:
                                self.maior = c[2]
                            elif cont > 1:
                                if self.maior < c[2]:
                                    self.maior = c[2]
                            cont += 1
                        self.window['-Num-'].update(values=[c for c in range(1, self.maior + 1)])
                elif botton == 'Eliminar Turma':
                    if values['-NDT-'] == '' or len(turmas[1:]) == 1:
                        Cgest.message('Nome não definido' if values['-NDT-'] == '' else 'Operação invalida')
                    else:
                        for c in turmas:
                                if c[1] == values['-NDT-']:
                                    elimar(definicoes[2], c[0], 'turmas')
                                    turmas = abrir_Turmas(definicoes[2])
                                    break
                        self.window['-NDT-'].update(values=[c[1] for c in turmas[1:]])
                        self.window['-NDT-'].update('')
                        self.window['-TDT-'].update(tutores[0][1])
                        self.window['-Num-'].update('')
                        self.window['-DETALHE-'].update('')
                        if not values['-CLASS-']:
                            self.window['-CLASS-'].update(False)
                        else:
                            self.window['-CLASS-'].update(True)

                        

    class Alunos:
        def __init__(self):
            self.layout_1 = [
                [sg.Image('image1.png', size=(300, 300)),
                 sg.Column([[sg.Frame('', [
                     [sg.Text('Clement A. N. Cazadi', font='Calibri 30')],
                     [sg.FilesBrowse('Carregar uma foto', file_types=(('Png', '.png'), ('Jpng', '.jpng'))),
                      sg.Button('Repor a imagem padrão')],
                     [sg.CBox('Editar os dados do aluno.'), sg.Text('', size=(25, 1)), sg.Button('Salvar dados')],
                     [sg.Text('ID do(a) aluno(a):'), sg.Text('8932')],
                     [sg.Text('Nome do aluno:'), sg.InputText('Clement Albert Nsangani Cazadi',
                                                              border_width=0, size=(50, 1))],
                     [sg.Text('Data de nasimento:'), sg.InputText('03/03/2003', border_width=0, size=(47, 1))],
                     [sg.Text('Número de telefone 1:'), sg.InputText('97856670', border_width=0)],
                     [sg.Text('Número de telefone 2:'), sg.InputText('03/03/2003', border_width=0)],
                     [sg.Text('Data de inscrição: '), sg.InputText('03/03/2003', border_width=0, size=(48, 1))],
                     [sg.Text('Defina a Turma:'), sg.Combo(['Português', 'Ingleis'])],
                     [sg.Text('Morada:'), sg.InputText('', )],
                     [sg.Text('Sexo do aluno(a):'), sg.Radio('Masculino', 1, True), sg.Radio('Feminino', 1)]
                 ], border_width=0)]])],
                [sg.Text('Detalhes adicionas do aluno')],
                [sg.MLine('', size=(100, 10))]
            ]

            self.window = sg.Window('Detalhes do aluno', self.layout_1, margins=(0, 0),
                                    size=(850, 620), element_justification='center', font='Calibri 12')

        def star(self):
            while True:
                buttons, values = self.window.read()
                if buttons in (None, sg.WIN_CLOSED):
                    self.window.close()
                    break

    class Deficoes:
        def __init__(self):
            self.layout = [
                [sg.Text('Defina a lingua:'), sg.Combo(['Português', 'Ingleis', 'Franceis'],
                                                       size=(23, 1), default_value=definicoes[1])],
                [sg.Text('Defina um Tema:'), sg.Combo(['TanBlue', 'LightGreen3', 'LightBlue3',
                                                       'GreenTan', 'GreenMono', 'DarkTeal9', 'LightBrown11',
                                                       'LightGrey6',
                                                       'LightGreen2', 'DarkBlue3', 'LightGrey3'],
                                                      size=(22, 1), default_value=definicoes[0], key='-CorDeFundo-')],
                [sg.Button('Salvar', border_width=0, size=(10, 2)), sg.Button('Cancelar', border_width=0, size=(10, 2))]
            ]
            self.Window = sg.Window('Definições', self.layout, element_justification='center')

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
            self.window = sg.Window('About', self.layout, element_justification='center', disable_minimize=True)

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
            self.window = sg.Window('Abrir CGT', self.layout, element_justification='center', disable_minimize=True)

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


Cgest.Tela_p().star()
