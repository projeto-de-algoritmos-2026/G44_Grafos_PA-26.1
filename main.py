import tkinter as tk
import tkinter.messagebox

from dados import ROTAS_REAIS
from grafo import MapaRotas
from telas import (
    abrir_adicionar_rota, abrir_lista_rotas,
    abrir_busca_dfs, abrir_busca_bfs,
    BG, SURFACE, SURFACE_H, BORDER, TEXT, MUTED, ACCENT, GREEN, DANGER,
    F_CARD, F_BODY, F_SMALL,
    _hover_card,
)

ARQUIVO_SALVO = 'mapa_rotas.txt'
W    = 620   # largura fixa da janela
H    = 680   # altura fixa da janela
PAD  = 48    # margem lateral generosa


def salvar_mapa(mapa):
    mapa.salvar_arquivo(ARQUIVO_SALVO)
    tk.messagebox.showinfo('Salvo', f'Mapa salvo em  {ARQUIVO_SALVO}')


def _make_card(parent, titulo, subtitulo, cor_sub, icone, cmd):
    """Card com altura fixa, borda via frame externo, hover sem bug."""
    CARD_H = 72

    # frame externo age como borda de 1px
    outer = tk.Frame(parent, bg=BORDER)
    outer.pack(fill='x', pady=(0, 2))

    inner = tk.Frame(outer, bg=SURFACE, cursor='hand2', height=CARD_H)
    inner.pack(fill='x', padx=1, pady=1)
    inner.pack_propagate(False)   # impede encolhimento

    # ícone
    lbl_ico = tk.Label(inner, text=icone,
                       font=('Helvetica', 16),
                       fg=MUTED, bg=SURFACE, width=3)
    lbl_ico.place(x=20, y=16)

    # título
    lbl_titulo = tk.Label(inner, text=titulo,
                          font=F_CARD, fg=TEXT, bg=SURFACE, anchor='w')
    lbl_titulo.place(x=68, y=14)

    # subtítulo
    lbl_sub = tk.Label(inner, text=subtitulo,
                       font=('Helvetica', 9), fg=cor_sub, bg=SURFACE, anchor='w')
    lbl_sub.place(x=68, y=40)

    # seta
    lbl_seta = tk.Label(inner, text='›',
                        font=('Helvetica', 22), fg=BORDER, bg=SURFACE)
    lbl_seta.place(relx=0.93, y=18)

    filhos = [lbl_ico, lbl_titulo, lbl_sub, lbl_seta]

    for w in [inner] + filhos:
        w.bind('<Button-1>', lambda e, c=cmd: c())

    _hover_card(inner, filhos, SURFACE_H, SURFACE)


def main():
    mapa = MapaRotas()
    for o, d, r, k in ROTAS_REAIS:
        mapa.adicionar_rota(o, d, r, k)
    mapa.carregar_arquivo(ARQUIVO_SALVO)

    # ── janela com tamanho fixo ───────────────────────────
    janela = tk.Tk()
    janela.title('Mapa de Rotas')
    janela.geometry(f'{W}x{H}')
    janela.configure(bg=BG)
    janela.resizable(False, False)

    # ── cabeçalho ────────────────────────────────────────
    header = tk.Frame(janela, bg=BG)
    header.pack(fill='x', padx=PAD, pady=(40, 0))

    tk.Label(header,
             text='Mapa de Rotas',
             font=('Helvetica', 28, 'bold'),
             fg=TEXT, bg=BG).pack(anchor='w')

    tk.Label(header,
             text='Capitais brasileiras  ·  BFS & DFS',
             font=('Helvetica', 10), fg=MUTED, bg=BG).pack(anchor='w', pady=(4, 14))

    # badges
    total_rotas = sum(len(v) for v in mapa.grafo.values()) // 2
    badges = tk.Frame(header, bg=BG)
    badges.pack(anchor='w')

    tk.Label(badges,
             text=f'  {len(mapa.grafo)} cidades  ',
             font=('Helvetica', 9, 'bold'),
             bg=ACCENT, fg='#FFFFFF',
             padx=6, pady=4).pack(side='left')

    tk.Label(badges, text='   ', bg=BG).pack(side='left')

    tk.Label(badges,
             text=f'  {total_rotas} rotas  ',
             font=('Helvetica', 9, 'bold'),
             bg=BORDER, fg=MUTED,
             padx=6, pady=4).pack(side='left')

    # divisor
    tk.Frame(janela, bg=BORDER, height=1).pack(
        fill='x', padx=PAD, pady=(22, 0))

    # ── cards ────────────────────────────────────────────
    cards_frame = tk.Frame(janela, bg=BG)
    cards_frame.pack(fill='x', padx=PAD, pady=(18, 0))

    itens = [
        ('Adicionar Rota', 'Cadastrar nova conexão entre cidades', MUTED,  '＋', lambda: abrir_adicionar_rota(mapa)),
        ('Listar Rotas',   'Ver todas as conexões do grafo',        MUTED,  '≡',  lambda: abrir_lista_rotas(mapa)),
        ('Salvar Mapa',    f'Exportar para  {ARQUIVO_SALVO}',       MUTED,  '↓',  lambda: salvar_mapa(mapa)),
        ('Busca  DFS',     'Exploração em profundidade',            ACCENT, '⬤',  lambda: abrir_busca_dfs(mapa)),
        ('Busca  BFS',     'Menor número de paradas',               GREEN,  '◎',  lambda: abrir_busca_bfs(mapa)),
    ]

    for titulo, sub, cor_sub, ico, cmd in itens:
        _make_card(cards_frame, titulo, sub, cor_sub, ico, cmd)

    # ── rodapé ───────────────────────────────────────────
    tk.Button(janela,
              text='Sair do programa',
              command=janela.destroy,
              font=('Helvetica', 9),
              fg=DANGER,
              bg=BG,
              activeforeground='#9B1C1C',
              activebackground=BG,
              relief='flat', bd=0,
              cursor='hand2').pack(pady=(20, 0))

    janela.mainloop()


if __name__ == '__main__':
    main()