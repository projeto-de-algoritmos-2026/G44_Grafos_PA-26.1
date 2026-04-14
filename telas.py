import tkinter as tk
import tkinter.messagebox

# ── Paleta ──────────────────────────────────────────────
BG        = '#EEF4FC'
SURFACE   = '#FFFFFF'
SURFACE_H = '#DDE9F8'
BORDER    = '#BDD1ED'
TEXT      = '#0B2545'
MUTED     = '#5577A0'
ACCENT    = '#1A6FD4'
GREEN     = '#00873D'
DANGER    = '#C0392B'

# ── Fontes ───────────────────────────────────────────────
F_H1      = ('Helvetica', 20, 'bold')
F_H2      = ('Helvetica', 14, 'bold')
F_CARD    = ('Helvetica', 12, 'bold')
F_BODY    = ('Helvetica', 10)
F_SMALL   = ('Helvetica', 9)
F_MONO    = ('Courier New', 10)

PAD       = 32   # margem lateral padrão em px


def _janela(titulo, w, h):
    r = tk.Tk()
    r.title(titulo)
    r.geometry(f'{w}x{h}')
    r.configure(bg=BG)
    r.resizable(False, False)
    return r


def _hover_card(row, filhos, cor_on, cor_off):
    def on(e):
        row.configure(bg=cor_on, highlightbackground=ACCENT)
        for w in filhos:
            try: w.configure(bg=cor_on)
            except: pass
    def off(e):
        row.configure(bg=cor_off, highlightbackground=BORDER)
        for w in filhos:
            try: w.configure(bg=cor_off)
            except: pass
    for w in [row] + filhos:
        w.bind('<Enter>', on)
        w.bind('<Leave>', off)


# ─────────────────────────────────────────────────────────
# Tela: Adicionar Rota
# ─────────────────────────────────────────────────────────
class TelaAdicionarRota(tk.Frame):
    def __init__(self, parent, mapa):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.mapa   = mapa
        self._ui()

    def _ui(self):
        self.parent.configure(bg=BG)
        p = PAD

        # cabeçalho
        tk.Label(self.parent, text='Nova Rota',
                 font=F_H1, fg=TEXT, bg=BG).pack(
                 anchor='w', padx=p, pady=(28, 2))
        tk.Label(self.parent,
                 text='Preencha os dados da conexão entre cidades.',
                 font=F_SMALL, fg=MUTED, bg=BG).pack(anchor='w', padx=p)
        tk.Frame(self.parent, bg=BORDER, height=1).pack(
                 fill='x', padx=p, pady=(16, 24))

        # campos
        self.entries = {}
        campos = [
            ('origem',  'Cidade de Origem'),
            ('destino', 'Cidade de Destino'),
            ('rod',     'Rodovia  (ex: BR-116)'),
            ('km',      'Distância em km'),
        ]
        for key, label in campos:
            tk.Label(self.parent, text=label.upper(),
                     font=('Helvetica', 8, 'bold'),
                     fg=MUTED, bg=BG).pack(anchor='w', padx=p)
            e = tk.Entry(self.parent,
                         font=F_BODY,
                         bg=SURFACE, fg=TEXT,
                         insertbackground=ACCENT,
                         relief='flat', bd=0,
                         highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=ACCENT)
            e.pack(fill='x', padx=p, ipady=8, pady=(3, 14))
            self.entries[key] = e

        tk.Frame(self.parent, bg=BORDER, height=1).pack(fill='x', padx=p, pady=(4, 16))

        tk.Button(self.parent, text='Adicionar Rota  →',
                  command=self._salvar,
                  font=('Helvetica', 11, 'bold'),
                  bg=GREEN, fg='#FFFFFF',
                  activebackground='#006B30',
                  activeforeground='#FFFFFF',
                  relief='flat', bd=0,
                  cursor='hand2',
                  padx=28, pady=10).pack(anchor='e', padx=p, pady=(0, 28))

    def _salvar(self):
        origem  = self.entries['origem'].get().strip().replace(' ', '')
        destino = self.entries['destino'].get().strip().replace(' ', '')
        rod     = self.entries['rod'].get().strip()
        try:    km = int(self.entries['km'].get().strip())
        except: km = 0
        if origem and destino:
            self.mapa.adicionar_rota(origem, destino, rod, km)
            tk.messagebox.showinfo('Rota adicionada',
                f'{origem}  ↔  {destino}\n{rod}  ·  {km} km\n\n'
                'Use "Salvar Mapa" para persistir.')
        else:
            tk.messagebox.showwarning('Atenção', 'Preencha Origem e Destino.')


def abrir_adicionar_rota(mapa):
    root = _janela('Nova Rota', 520, 560)
    TelaAdicionarRota(root, mapa)
    root.mainloop()


# ─────────────────────────────────────────────────────────
# Tela: Listar Rotas
# ─────────────────────────────────────────────────────────
def abrir_lista_rotas(mapa):
    root = _janela('Rotas Cadastradas', 680, 620)
    p = PAD

    tk.Label(root, text='Rotas Cadastradas',
             font=F_H1, fg=TEXT, bg=BG).pack(anchor='w', padx=p, pady=(28, 2))
    total = sum(len(v) for v in mapa.grafo.values()) // 2
    tk.Label(root, text=f'{len(mapa.grafo)} cidades  ·  {total} conexões',
             font=F_SMALL, fg=MUTED, bg=BG).pack(anchor='w', padx=p)
    tk.Frame(root, bg=BORDER, height=1).pack(fill='x', padx=p, pady=(14, 0))

    frame = tk.Frame(root, bg=BG)
    frame.pack(fill='both', expand=True, padx=p, pady=14)

    sb = tk.Scrollbar(frame, bg=SURFACE, troughcolor=BG,
                      relief='flat', bd=0)
    sb.pack(side='right', fill='y')

    lb = tk.Listbox(frame,
                    bg=SURFACE, fg=TEXT,
                    font=F_MONO,
                    selectbackground=ACCENT,
                    selectforeground='#FFFFFF',
                    relief='flat', bd=0,
                    highlightthickness=1,
                    highlightbackground=BORDER,
                    yscrollcommand=sb.set,
                    activestyle='none')
    lb.pack(side='left', fill='both', expand=True)
    sb.config(command=lb.yview)

    vistos = set()
    for cidade in sorted(mapa.grafo.keys()):
        for dest in mapa.grafo[cidade]:
            par = tuple(sorted([cidade, dest]))
            if par not in vistos:
                rod, km = mapa.detalhes.get((cidade, dest), ('', 0))
                lb.insert('end', f'  {cidade:<22}  ↔  {dest:<22}  {rod:<10}  {km} km')
                lb.insert('end', '')
                vistos.add(par)

    root.mainloop()


# ─────────────────────────────────────────────────────────
# Tela: Busca (DFS / BFS)
# ─────────────────────────────────────────────────────────
class TelaBusca(tk.Frame):
    def __init__(self, parent, mapa, modo):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.mapa   = mapa
        self.modo   = modo
        self._ui()

    def _ui(self):
        is_dfs   = self.modo == 'dfs'
        sigla    = 'DFS' if is_dfs else 'BFS'
        subtit   = 'Exploração em profundidade' if is_dfs else 'Menor número de paradas'
        cor_sigla = MUTED if is_dfs else GREEN
        p = PAD

        self.parent.configure(bg=BG)

        # sigla grande
        tk.Label(self.parent, text=sigla,
                 font=('Helvetica', 42, 'bold'),
                 fg=cor_sigla, bg=BG).pack(anchor='w', padx=p, pady=(28, 0))
        tk.Label(self.parent, text=subtit,
                 font=F_SMALL, fg=MUTED, bg=BG).pack(anchor='w', padx=p)
        tk.Frame(self.parent, bg=BORDER, height=1).pack(
                 fill='x', padx=p, pady=(14, 20))

        # cidades disponíveis
        tk.Label(self.parent, text='CIDADES DISPONÍVEIS',
                 font=('Helvetica', 8, 'bold'), fg=MUTED, bg=BG).pack(
                 anchor='w', padx=p)
        cidades = ', '.join(sorted(self.mapa.grafo.keys()))
        tk.Label(self.parent, text=cidades,
                 font=('Helvetica', 8), fg=MUTED, bg=BG,
                 wraplength=460, justify='left').pack(
                 anchor='w', padx=p, pady=(2, 18))

        tk.Frame(self.parent, bg=BORDER, height=1).pack(fill='x', padx=p, pady=(0, 20))

        # campos
        self.entries = {}
        for key, label in [('inicio', 'Cidade de Origem'), ('fim', 'Cidade de Destino')]:
            tk.Label(self.parent, text=label.upper(),
                     font=('Helvetica', 8, 'bold'),
                     fg=MUTED, bg=BG).pack(anchor='w', padx=p)
            e = tk.Entry(self.parent,
                         font=F_BODY,
                         bg=SURFACE, fg=TEXT,
                         insertbackground=ACCENT,
                         relief='flat', bd=0,
                         highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=ACCENT)
            e.pack(fill='x', padx=p, ipady=8, pady=(3, 14))
            self.entries[key] = e

        tk.Frame(self.parent, bg=BORDER, height=1).pack(fill='x', padx=p, pady=(4, 16))

        cor_btn = GREEN if not is_dfs else ACCENT
        tk.Button(self.parent, text=f'Buscar com {sigla}  →',
                  command=self._buscar,
                  font=('Helvetica', 11, 'bold'),
                  bg=cor_btn, fg='#FFFFFF',
                  activebackground='#006B30' if not is_dfs else '#1459A8',
                  activeforeground='#FFFFFF',
                  relief='flat', bd=0,
                  cursor='hand2',
                  padx=28, pady=10).pack(anchor='e', padx=p, pady=(0, 28))

    def _buscar(self):
        inicio = self.entries['inicio'].get().strip().replace(' ', '')
        fim    = self.entries['fim'].get().strip().replace(' ', '')
        if not inicio or not fim:
            tk.messagebox.showwarning('Atenção', 'Preencha os dois campos.')
            return
        if inicio not in self.mapa.grafo:
            tk.messagebox.showwarning('Cidade não encontrada',
                f'"{inicio}" não está no mapa.\n'
                'Use os nomes exatos, sem espaços e sem acentos.')
            return
        if self.modo == 'dfs':
            if not self.mapa.dfs(inicio, fim):
                tk.messagebox.showinfo('Sem resultado',
                    f'Nenhuma rota encontrada:\n{inicio}  →  {fim}')
        else:
            self.mapa.bfs(inicio, fim)


def abrir_busca_dfs(mapa):
    root = _janela('Busca DFS', 520, 580)
    TelaBusca(root, mapa, 'dfs')
    root.mainloop()


def abrir_busca_bfs(mapa):
    root = _janela('Busca BFS', 520, 580)
    TelaBusca(root, mapa, 'bfs')
    root.mainloop()