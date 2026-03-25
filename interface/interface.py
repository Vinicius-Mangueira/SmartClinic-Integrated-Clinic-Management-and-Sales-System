import tkinter as tk
from tkinter import ttk, messagebox, font
import tkinter.font as tkfont

# ─────────────────────────────────────────────
#  PALETA DE CORES
# ─────────────────────────────────────────────
BG_DARK      = "#0F1117"
BG_PANEL     = "#161B27"
BG_CARD      = "#1E2535"
BG_INPUT     = "#252D40"
BG_ROW_ALT   = "#1A2030"

ACCENT       = "#4F8EF7"
ACCENT_HOVER = "#3A7AE0"
ACCENT_GREEN = "#3DDC84"
ACCENT_RED   = "#F75F5F"
ACCENT_YEL   = "#F7C948"

TEXT_PRI     = "#EEF1F8"
TEXT_SEC     = "#8A94AB"
TEXT_MUT     = "#4E5A72"

BORDER       = "#2A3248"
SIDEBAR_W    = 210

# ─────────────────────────────────────────────
#  DADOS DEMO (simula banco de dados)
# ─────────────────────────────────────────────
demo_pacientes = [
    ("001", "Ana Souza",       "31", "F", "(83) 99811-2233", "ana@email.com",    "Ativa"),
    ("002", "Carlos Lima",     "45", "M", "(83) 98722-3344", "carlos@email.com", "Ativa"),
    ("003", "Maria Fernanda",  "28", "F", "(83) 97633-4455", "mf@email.com",     "Inativa"),
    ("004", "João Pedro",      "52", "M", "(83) 96544-5566", "jp@email.com",     "Ativa"),
    ("005", "Lucia Alves",     "37", "F", "(83) 95455-6677", "lucia@email.com",  "Ativa"),
]

demo_produtos = [
    ("P001", "Consulta Geral",     "Serviço",  "R$ 150,00", "—",   "Ativo"),
    ("P002", "Luva Cirúrgica (cx)", "Produto",  "R$  35,00", "120", "Ativo"),
    ("P003", "Seringa 5ml (cx)",   "Produto",  "R$  22,00", "85",  "Ativo"),
    ("P004", "Exame de Sangue",    "Serviço",  "R$  80,00", "—",   "Ativo"),
    ("P005", "Curativo Simples",   "Serviço",  "R$  60,00", "—",   "Inativo"),
]

demo_vendas = [
    ("V001", "Ana Souza",     "Consulta Geral",     "R$ 150,00", "Pago",    "Dr. Silva",  "15/03/2026"),
    ("V002", "Carlos Lima",   "Exame de Sangue",    "R$  80,00", "Pago",    "Dra. Costa", "16/03/2026"),
    ("V003", "Maria Fernanda","Curativo Simples",   "R$  60,00", "Pendente","Dr. Silva",  "18/03/2026"),
    ("V004", "João Pedro",    "Consulta Geral",     "R$ 150,00", "Pago",    "Dra. Costa", "20/03/2026"),
    ("V005", "Lucia Alves",   "Luva Cirúrgica (cx)","R$  35,00", "Pago",    "Dr. Silva",  "22/03/2026"),
]

# ─────────────────────────────────────────────
#  HELPER — botão estilizado
# ─────────────────────────────────────────────
def styled_btn(parent, text, bg=ACCENT, fg=TEXT_PRI, cmd=None, w=None):
    kw = dict(
        text=text, bg=bg, fg=fg, relief="flat", cursor="hand2",
        font=("Segoe UI", 9, "bold"), bd=0, padx=14, pady=7,
        activebackground=ACCENT_HOVER, activeforeground=TEXT_PRI,
        command=cmd or (lambda: None)
    )
    if w:
        kw["width"] = w
    btn = tk.Button(parent, **kw)

    def on_enter(e):
        darken = {"bg": ACCENT_HOVER} if bg == ACCENT else \
                 {"bg": "#D94F4F"} if bg == ACCENT_RED else \
                 {"bg": "#30B870"} if bg == ACCENT_GREEN else {"bg": BG_INPUT}
        btn.config(**darken)

    def on_leave(e):
        btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


# ─────────────────────────────────────────────
#  HELPER — Entry estilizado com placeholder
# ─────────────────────────────────────────────
class PlaceholderEntry(tk.Entry):
    def __init__(self, master, placeholder="", *args, **kwargs):
        kwargs.setdefault("bg", BG_INPUT)
        kwargs.setdefault("fg", TEXT_PRI)
        kwargs.setdefault("insertbackground", ACCENT)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("font", ("Segoe UI", 10))
        kwargs.setdefault("bd", 0)
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self._ph_active = False
        self._show_ph()
        self.bind("<FocusIn>",  self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _show_ph(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=TEXT_MUT)
            self._ph_active = True

    def _on_focus_in(self, _):
        if self._ph_active:
            self.delete(0, "end")
            self.config(fg=TEXT_PRI)
            self._ph_active = False

    def _on_focus_out(self, _):
        if not self.get():
            self._show_ph()

    def get_value(self):
        return "" if self._ph_active else self.get()


# ─────────────────────────────────────────────
#  HELPER — Treeview estilizado
# ─────────────────────────────────────────────
def build_treeview(parent, columns):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("SC.Treeview",
        background=BG_CARD, foreground=TEXT_PRI,
        fieldbackground=BG_CARD, rowheight=34,
        font=("Segoe UI", 10), borderwidth=0
    )
    style.configure("SC.Treeview.Heading",
        background=BG_INPUT, foreground=TEXT_SEC,
        font=("Segoe UI", 9, "bold"), relief="flat", borderwidth=0
    )
    style.map("SC.Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", "#FFFFFF")]
    )
    style.layout("SC.Treeview", [
        ("SC.Treeview.treearea", {"sticky": "nswe"})
    ])

    frame = tk.Frame(parent, bg=BG_CARD)

    tv = ttk.Treeview(frame, columns=columns, show="headings",
                      style="SC.Treeview", selectmode="browse")

    sb = tk.Scrollbar(frame, orient="vertical", command=tv.yview,
                      bg=BG_INPUT, troughcolor=BG_CARD,
                      activebackground=ACCENT, width=8, relief="flat")
    tv.configure(yscrollcommand=sb.set)

    tv.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    tv.tag_configure("alt", background=BG_ROW_ALT)
    tv.tag_configure("pago", foreground=ACCENT_GREEN)
    tv.tag_configure("pendente", foreground=ACCENT_YEL)
    tv.tag_configure("inativo", foreground=TEXT_MUT)

    return frame, tv


# ═══════════════════════════════════════════════════════════════════════
#  PÁGINAS
# ═══════════════════════════════════════════════════════════════════════

class PacientesPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)
        self._build()

    def _build(self):
        # ── Título
        hdr = tk.Frame(self, bg=BG_DARK)
        hdr.pack(fill="x", padx=28, pady=(24, 0))
        tk.Label(hdr, text="Pacientes", bg=BG_DARK,
                 fg=TEXT_PRI, font=("Segoe UI", 20, "bold")).pack(side="left")
        tk.Label(hdr, text=f"  {len(demo_pacientes)} registros", bg=BG_DARK,
                 fg=TEXT_SEC, font=("Segoe UI", 11)).pack(side="left", pady=4)
        styled_btn(hdr, "+ Novo Paciente", cmd=self._open_form).pack(side="right")

        # ── Barra de busca
        bar = tk.Frame(self, bg=BG_DARK)
        bar.pack(fill="x", padx=28, pady=12)

        search_frame = tk.Frame(bar, bg=BG_INPUT, bd=0)
        search_frame.pack(side="left", fill="x", expand=True)
        tk.Label(search_frame, text="🔍", bg=BG_INPUT, fg=TEXT_SEC,
                 font=("Segoe UI", 11)).pack(side="left", padx=8)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter)
        tk.Entry(search_frame, textvariable=self.search_var,
                 bg=BG_INPUT, fg=TEXT_PRI, insertbackground=ACCENT,
                 relief="flat", font=("Segoe UI", 10),
                 bd=0).pack(side="left", fill="x", expand=True, ipady=8)

        for status, clr in [("Todos", TEXT_SEC), ("Ativos", ACCENT_GREEN), ("Inativos", TEXT_MUT)]:
            styled_btn(bar, status, bg=BG_CARD, fg=clr, w=9).pack(side="right", padx=3)

        # ── Tabela
        cols = ("Cód.", "Nome", "Idade", "Gênero", "Telefone", "E-mail", "Status")
        tv_frame, self.tv = build_treeview(self, cols)
        tv_frame.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        widths = (60, 180, 60, 70, 140, 200, 80)
        for col, w in zip(cols, widths):
            self.tv.heading(col, text=col)
            self.tv.column(col, width=w, anchor="center" if col not in ("Nome", "E-mail") else "w")

        self._populate(demo_pacientes)

        # ── Rodapé de ações
        actions = tk.Frame(self, bg=BG_PANEL)
        actions.pack(fill="x", padx=28, pady=(0, 20))
        styled_btn(actions, "✏  Editar",  bg=ACCENT,       cmd=self._edit).pack(side="left", padx=(0, 8))
        styled_btn(actions, "🗑  Excluir", bg=ACCENT_RED,   cmd=self._delete).pack(side="left", padx=(0, 8))
        styled_btn(actions, "↺  Limpar",  bg=BG_CARD, fg=TEXT_SEC, cmd=self._clear).pack(side="left")

    def _populate(self, data):
        self.tv.delete(*self.tv.get_children())
        for i, row in enumerate(data):
            tag = "inativo" if row[-1] == "Inativa" else ("alt" if i % 2 else "")
            self.tv.insert("", "end", values=row, tags=(tag,))

    def _filter(self, *_):
        q = self.search_var.get().lower()
        filtered = [r for r in demo_pacientes if q in " ".join(r).lower()]
        self._populate(filtered)

    def _open_form(self):
        _PacienteForm(self)

    def _edit(self):
        sel = self.tv.selection()
        if not sel:
            messagebox.showinfo("SmartClinic", "Selecione um paciente.")
            return
        vals = self.tv.item(sel[0])["values"]
        _PacienteForm(self, vals)

    def _delete(self):
        sel = self.tv.selection()
        if not sel:
            messagebox.showinfo("SmartClinic", "Selecione um paciente.")
            return
        nome = self.tv.item(sel[0])["values"][1]
        if messagebox.askyesno("Confirmar", f"Excluir '{nome}'?"):
            self.tv.delete(sel[0])

    def _clear(self):
        self.search_var.set("")
        self._populate(demo_pacientes)


class _PacienteForm(tk.Toplevel):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self.title("Paciente" if not data else "Editar Paciente")
        self.configure(bg=BG_PANEL)
        self.geometry("440x420")
        self.resizable(False, False)
        self.grab_set()

        tk.Label(self, text="Novo Paciente" if not data else "Editar Paciente",
                 bg=BG_PANEL, fg=TEXT_PRI,
                 font=("Segoe UI", 15, "bold")).pack(pady=(20, 16), padx=24, anchor="w")

        fields = [("Nome completo", data[1] if data else ""),
                  ("Idade",         data[2] if data else ""),
                  ("Telefone",      data[4] if data else ""),
                  ("E-mail",        data[5] if data else "")]

        self.entries = {}
        for label, val in fields:
            row = tk.Frame(self, bg=BG_PANEL)
            row.pack(fill="x", padx=24, pady=5)
            tk.Label(row, text=label, bg=BG_PANEL, fg=TEXT_SEC,
                     font=("Segoe UI", 9)).pack(anchor="w")
            inp = tk.Frame(row, bg=BG_INPUT)
            inp.pack(fill="x", pady=(2, 0))
            e = tk.Entry(inp, bg=BG_INPUT, fg=TEXT_PRI, relief="flat",
                         font=("Segoe UI", 10), insertbackground=ACCENT, bd=0)
            e.pack(fill="x", ipady=8, padx=8)
            if val:
                e.insert(0, val)
            self.entries[label] = e

        btns = tk.Frame(self, bg=BG_PANEL)
        btns.pack(fill="x", padx=24, pady=20)
        styled_btn(btns, "Salvar",   bg=ACCENT_GREEN, cmd=self.destroy).pack(side="right", padx=(8, 0))
        styled_btn(btns, "Cancelar", bg=BG_CARD, fg=TEXT_SEC, cmd=self.destroy).pack(side="right")


# ── Produtos ─────────────────────────────────────────────────────────

class ProdutosPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_DARK)
        hdr.pack(fill="x", padx=28, pady=(24, 0))
        tk.Label(hdr, text="Produtos & Serviços", bg=BG_DARK,
                 fg=TEXT_PRI, font=("Segoe UI", 20, "bold")).pack(side="left")
        styled_btn(hdr, "+ Novo Item", cmd=lambda: messagebox.showinfo("SmartClinic", "Formulário de novo item.")).pack(side="right")

        bar = tk.Frame(self, bg=BG_DARK)
        bar.pack(fill="x", padx=28, pady=12)
        sf = tk.Frame(bar, bg=BG_INPUT)
        sf.pack(side="left", fill="x", expand=True)
        tk.Label(sf, text="🔍", bg=BG_INPUT, fg=TEXT_SEC,
                 font=("Segoe UI", 11)).pack(side="left", padx=8)
        tk.Entry(sf, bg=BG_INPUT, fg=TEXT_PRI, relief="flat",
                 font=("Segoe UI", 10), insertbackground=ACCENT,
                 bd=0).pack(side="left", fill="x", expand=True, ipady=8)

        for tab in ("Todos", "Produtos", "Serviços"):
            styled_btn(bar, tab, bg=BG_CARD, fg=TEXT_SEC, w=10).pack(side="right", padx=3)

        cols = ("Cód.", "Descrição", "Tipo", "Preço", "Estoque", "Status")
        tv_frame, tv = build_treeview(self, cols)
        tv_frame.pack(fill="both", expand=True, padx=28, pady=(0, 8))

        for col, w, anch in zip(cols, (70, 200, 90, 100, 80, 80),
                                 ("center", "w", "center", "e", "center", "center")):
            tv.heading(col, text=col)
            tv.column(col, width=w, anchor=anch)

        for i, row in enumerate(demo_produtos):
            tag = "inativo" if row[-1] == "Inativo" else ("alt" if i % 2 else "")
            tv.insert("", "end", values=row, tags=(tag,))

        # cards de resumo
        cards = tk.Frame(self, bg=BG_DARK)
        cards.pack(fill="x", padx=28, pady=(8, 24))

        totais = [
            ("Total de Itens",  str(len(demo_produtos)),  ACCENT),
            ("Produtos",        "2",                      ACCENT_YEL),
            ("Serviços",        "3",                      ACCENT_GREEN),
            ("Inativos",        "1",                      ACCENT_RED),
        ]
        for label, val, clr in totais:
            c = tk.Frame(cards, bg=BG_CARD, padx=20, pady=12)
            c.pack(side="left", padx=(0, 12))
            tk.Label(c, text=val,   bg=BG_CARD, fg=clr,    font=("Segoe UI", 22, "bold")).pack()
            tk.Label(c, text=label, bg=BG_CARD, fg=TEXT_SEC, font=("Segoe UI", 9)).pack()


# ── Vendas ────────────────────────────────────────────────────────────

class VendasPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_DARK)
        hdr.pack(fill="x", padx=28, pady=(24, 0))
        tk.Label(hdr, text="Vendas & Compras", bg=BG_DARK,
                 fg=TEXT_PRI, font=("Segoe UI", 20, "bold")).pack(side="left")
        styled_btn(hdr, "+ Nova Venda").pack(side="right")

        # filtros data
        bar = tk.Frame(self, bg=BG_DARK)
        bar.pack(fill="x", padx=28, pady=12)

        for lbl, val in [("De:", "01/03/2026"), ("Até:", "31/03/2026")]:
            tk.Label(bar, text=lbl, bg=BG_DARK, fg=TEXT_SEC,
                     font=("Segoe UI", 10)).pack(side="left", padx=(0, 4))
            ef = tk.Frame(bar, bg=BG_INPUT)
            ef.pack(side="left", padx=(0, 12))
            e = tk.Entry(ef, bg=BG_INPUT, fg=TEXT_PRI, relief="flat",
                         font=("Segoe UI", 10), width=12, insertbackground=ACCENT, bd=0)
            e.pack(ipady=7, padx=6)
            e.insert(0, val)

        styled_btn(bar, "Filtrar", bg=ACCENT, w=8).pack(side="left", padx=4)

        for status in ("Todos", "Pago", "Pendente"):
            clr = ACCENT_GREEN if status == "Pago" else (ACCENT_YEL if status == "Pendente" else TEXT_SEC)
            styled_btn(bar, status, bg=BG_CARD, fg=clr, w=9).pack(side="right", padx=3)

        cols = ("Nº Venda", "Paciente", "Item", "Valor", "Status", "Funcionário", "Data")
        tv_frame, tv = build_treeview(self, cols)
        tv_frame.pack(fill="both", expand=True, padx=28, pady=(0, 8))

        for col, w, anch in zip(cols, (80, 150, 160, 90, 90, 120, 110),
                                 ("center", "w", "w", "e", "center", "center", "center")):
            tv.heading(col, text=col)
            tv.column(col, width=w, anchor=anch)

        for i, row in enumerate(demo_vendas):
            tag = "pago" if row[4] == "Pago" else "pendente"
            if i % 2:
                tag = tag  # prioridade status
            tv.insert("", "end", values=row, tags=(tag,))

        # totalizador
        total = tk.Frame(self, bg=BG_PANEL)
        total.pack(fill="x", padx=28, pady=(0, 20))

        tots = [("Faturamento Total", "R$ 475,00", ACCENT_GREEN),
                ("Pendente",          "R$  60,00", ACCENT_YEL),
                ("Recebido",          "R$ 415,00", ACCENT)]

        for lbl, val, clr in tots:
            box = tk.Frame(total, bg=BG_CARD, padx=20, pady=10)
            box.pack(side="left", padx=(0, 10), pady=8)
            tk.Label(box, text=val, bg=BG_CARD, fg=clr,    font=("Segoe UI", 16, "bold")).pack()
            tk.Label(box, text=lbl, bg=BG_CARD, fg=TEXT_SEC, font=("Segoe UI", 9)).pack()


# ── Dashboard ─────────────────────────────────────────────────────────

class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)
        self._build()

    def _build(self):
        # saudação
        hdr = tk.Frame(self, bg=BG_DARK)
        hdr.pack(fill="x", padx=28, pady=(28, 4))
        tk.Label(hdr, text="Painel Geral", bg=BG_DARK,
                 fg=TEXT_PRI, font=("Segoe UI", 20, "bold")).pack(side="left")
        tk.Label(hdr, text="Março 2026", bg=BG_DARK,
                 fg=TEXT_SEC, font=("Segoe UI", 11)).pack(side="right")

        # KPI cards
        kpis_row = tk.Frame(self, bg=BG_DARK)
        kpis_row.pack(fill="x", padx=28, pady=(16, 20))

        kpis = [
            ("👤", "Pacientes",   str(len(demo_pacientes)), "+2 este mês",  ACCENT),
            ("📦", "Produtos",    "5",                      "2 com estoque baixo", ACCENT_YEL),
            ("💰", "Faturamento", "R$ 475",                 "este mês",     ACCENT_GREEN),
            ("⏳", "Pendentes",   "1 venda",                "R$ 60,00",     ACCENT_RED),
        ]
        for icon, title, val, sub, clr in kpis:
            card = tk.Frame(kpis_row, bg=BG_CARD, pady=16, padx=20)
            card.pack(side="left", fill="x", expand=True, padx=(0, 12))
            top = tk.Frame(card, bg=BG_CARD)
            top.pack(fill="x")
            tk.Label(top, text=icon, bg=BG_CARD, fg=clr,
                     font=("Segoe UI", 18)).pack(side="left")
            tk.Label(top, text=title, bg=BG_CARD, fg=TEXT_SEC,
                     font=("Segoe UI", 9)).pack(side="left", padx=6, pady=4)
            tk.Label(card, text=val, bg=BG_CARD, fg=TEXT_PRI,
                     font=("Segoe UI", 22, "bold")).pack(anchor="w")
            tk.Label(card, text=sub, bg=BG_CARD, fg=TEXT_MUT,
                     font=("Segoe UI", 8)).pack(anchor="w")

        # Dois painéis lado a lado
        mid = tk.Frame(self, bg=BG_DARK)
        mid.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        # Últimas vendas
        left = tk.Frame(mid, bg=BG_CARD)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(left, text="Últimas Vendas", bg=BG_CARD, fg=TEXT_PRI,
                 font=("Segoe UI", 12, "bold"), pady=14).pack(anchor="w", padx=16)
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x")

        for row in demo_vendas[-4:]:
            r = tk.Frame(left, bg=BG_CARD)
            r.pack(fill="x", padx=16, pady=6)
            clr_status = ACCENT_GREEN if row[4] == "Pago" else ACCENT_YEL
            tk.Label(r, text=row[1], bg=BG_CARD, fg=TEXT_PRI,
                     font=("Segoe UI", 10)).pack(side="left")
            tk.Label(r, text=row[4], bg=BG_CARD, fg=clr_status,
                     font=("Segoe UI", 9, "bold")).pack(side="right")
            tk.Label(r, text=row[3], bg=BG_CARD, fg=ACCENT,
                     font=("Segoe UI", 10)).pack(side="right", padx=12)

        # Gráfico de barras simples (canvas)
        right = tk.Frame(mid, bg=BG_CARD, width=280)
        right.pack(side="right", fill="both")
        right.pack_propagate(False)
        tk.Label(right, text="Vendas por Dia (Março)", bg=BG_CARD, fg=TEXT_PRI,
                 font=("Segoe UI", 11, "bold"), pady=14).pack(anchor="w", padx=16)
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        canvas = tk.Canvas(right, bg=BG_CARD, bd=0, highlightthickness=0, height=180)
        canvas.pack(fill="both", expand=True, padx=16, pady=12)

        bar_data = [("15", 150), ("16", 80), ("18", 60), ("20", 150), ("22", 35)]
        max_val = 180
        bw = 28
        gap = 18
        x0  = 24
        base_y = 160

        for i, (label, v) in enumerate(bar_data):
            bh = int(v / max_val * 130)
            x1 = x0 + i * (bw + gap)
            x2 = x1 + bw
            canvas.create_rectangle(x1, base_y - bh, x2, base_y,
                                     fill=ACCENT, outline="", width=0)
            canvas.create_text(x1 + bw // 2, base_y + 10,
                                text=label, fill=TEXT_SEC, font=("Segoe UI", 8))
            canvas.create_text(x1 + bw // 2, base_y - bh - 10,
                                text=f"R${v}", fill=TEXT_PRI, font=("Segoe UI", 7, "bold"))


# ═══════════════════════════════════════════════════════════════════════
#  APLICAÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════

class SmartClinic:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SmartClinic — Sistema Integrado de Gestão Clínica")
        self.root.configure(bg=BG_DARK)
        self.root.geometry("1100x680")
        self.root.minsize(900, 600)

        self._setup_icon()
        self._build_layout()
        self.root.mainloop()

    def _setup_icon(self):
        try:
            img = tk.PhotoImage(width=32, height=32)
            self.root.iconphoto(True, img)
        except Exception:
            pass

    def _build_layout(self):
        # ── Sidebar
        self.sidebar = tk.Frame(self.root, bg=BG_PANEL, width=SIDEBAR_W)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=BG_PANEL, pady=22)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="⚕",  bg=BG_PANEL, fg=ACCENT,
                 font=("Segoe UI", 24)).pack()
        tk.Label(logo_frame, text="SmartClinic", bg=BG_PANEL, fg=TEXT_PRI,
                 font=("Segoe UI", 13, "bold")).pack()
        tk.Label(logo_frame, text="Gestão Clínica v1.0", bg=BG_PANEL, fg=TEXT_MUT,
                 font=("Segoe UI", 8)).pack()

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=4)

        # Menu items
        self.nav_items = {}
        self.active_page = None

        menu = [
            ("📊", "Dashboard",  DashboardPage),
            ("👥", "Pacientes",  PacientesPage),
            ("📦", "Produtos",   ProdutosPage),
            ("💳", "Vendas",     VendasPage),
        ]

        for icon, label, page_cls in menu:
            self._add_nav_item(icon, label, page_cls)

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=12)

        # Rodapé sidebar
        bottom = tk.Frame(self.sidebar, bg=BG_PANEL)
        bottom.pack(side="bottom", fill="x", pady=12)
        tk.Label(bottom, text="●  Sistema Online", bg=BG_PANEL,
                 fg=ACCENT_GREEN, font=("Segoe UI", 8)).pack()

        # ── Área principal
        self.main_area = tk.Frame(self.root, bg=BG_DARK)
        self.main_area.pack(side="left", fill="both", expand=True)

        # Topbar
        topbar = tk.Frame(self.main_area, bg=BG_PANEL, height=48)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.topbar_title = tk.Label(topbar, text="Dashboard", bg=BG_PANEL,
                                      fg=TEXT_PRI, font=("Segoe UI", 11, "bold"))
        self.topbar_title.pack(side="left", padx=20, pady=12)

        tk.Label(topbar, text="Dr. Admin  ▾", bg=BG_PANEL, fg=TEXT_SEC,
                 font=("Segoe UI", 10)).pack(side="right", padx=20)
        tk.Label(topbar, text="🔔", bg=BG_PANEL, fg=TEXT_SEC,
                 font=("Segoe UI", 12)).pack(side="right")

        # Conteúdo
        self.content = tk.Frame(self.main_area, bg=BG_DARK)
        self.content.pack(fill="both", expand=True)

        # Páginas instanciadas
        self.pages = {}
        for _, label, page_cls in menu:
            page = page_cls(self.content)
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pages[label] = page

        self._switch("Dashboard")

    def _add_nav_item(self, icon, label, page_cls):
        btn_frame = tk.Frame(self.sidebar, bg=BG_PANEL, cursor="hand2")
        btn_frame.pack(fill="x", padx=10, pady=2)

        accent_bar = tk.Frame(btn_frame, bg=BG_PANEL, width=3)
        accent_bar.pack(side="left", fill="y")

        inner = tk.Frame(btn_frame, bg=BG_PANEL, padx=10, pady=10)
        inner.pack(fill="x", side="left")

        icon_lbl = tk.Label(inner, text=icon, bg=BG_PANEL, fg=TEXT_SEC,
                            font=("Segoe UI", 13))
        icon_lbl.pack(side="left")
        lbl = tk.Label(inner, text=label, bg=BG_PANEL, fg=TEXT_SEC,
                       font=("Segoe UI", 10))
        lbl.pack(side="left", padx=10)

        widgets = (btn_frame, inner, icon_lbl, lbl, accent_bar)

        def on_click(l=label):
            self._switch(l)

        def on_enter(e, ww=widgets):
            if self.active_page != label:
                for w in ww:
                    w.config(bg="#1C2236")

        def on_leave(e, ww=widgets, l=label):
            if self.active_page != l:
                for w in ww:
                    w.config(bg=BG_PANEL)

        for w in widgets:
            w.bind("<Button-1>", lambda e, l=label: on_click(l))
            w.bind("<Enter>",  on_enter)
            w.bind("<Leave>",  on_leave)

        self.nav_items[label] = (widgets, accent_bar)

    def _switch(self, name):
        # Resetar anterior
        if self.active_page and self.active_page in self.nav_items:
            prev_widgets, prev_bar = self.nav_items[self.active_page]
            for w in prev_widgets:
                w.config(bg=BG_PANEL)
            prev_bar.config(bg=BG_PANEL)
            for w in prev_widgets[2:4]:  # icon e label
                w.config(fg=TEXT_SEC)

        self.active_page = name
        widgets, bar = self.nav_items[name]
        for w in widgets:
            w.config(bg="#1C2A45")
        bar.config(bg=ACCENT, width=3)
        widgets[2].config(fg=ACCENT)   # icon
        widgets[3].config(fg=TEXT_PRI)  # label

        self.pages[name].lift()
        self.topbar_title.config(text=name)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    SmartClinic()