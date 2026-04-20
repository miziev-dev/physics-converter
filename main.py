import tkinter as tk
from tkinter import ttk, messagebox

# ─── ЦВЕТОВАЯ СХЕМА ───────────────────────────────────────────────────────────
BG         = "#1e1e2e"   # фон приложения
SIDEBAR_BG = "#181825"   # боковая панель
CARD_BG    = "#313244"   # карточка
ACCENT     = "#cba6f7"   # фиолетовый акцент
ACCENT2    = "#89b4fa"   # синий акцент
TEXT       = "#cdd6f4"   # основной текст
TEXT_SUB   = "#a6adc8"   # вторичный текст
SUCCESS    = "#a6e3a1"   # зелёный
ENTRY_BG   = "#45475a"   # фон поля ввода
BTN_BG     = "#cba6f7"   # кнопка
BTN_FG     = "#1e1e2e"   # текст кнопки
HOVER      = "#b48ead"   # hover кнопки

# ─── ДАННЫЕ КОНВЕРТЕРА ─────────────────────────────────────────────────────────
CATEGORIES = {
    "📏  Длина": {
        "units": ["Метр (м)", "Километр (км)", "Сантиметр (см)", "Миллиметр (мм)",
                  "Микрометр (мкм)", "Нанометр (нм)", "Дюйм (in)", "Фут (ft)",
                  "Ярд (yd)", "Миля (mi)", "Морская миля (nmi)"],
        "to_base": {
            "Метр (м)": 1, "Километр (км)": 1e3, "Сантиметр (см)": 1e-2,
            "Миллиметр (мм)": 1e-3, "Микрометр (мкм)": 1e-6, "Нанометр (нм)": 1e-9,
            "Дюйм (in)": 0.0254, "Фут (ft)": 0.3048, "Ярд (yd)": 0.9144,
            "Миля (mi)": 1609.344, "Морская миля (nmi)": 1852
        },
        "temp": False
    },
    "⚖️  Масса": {
        "units": ["Килограмм (кг)", "Грамм (г)", "Миллиграмм (мг)", "Тонна (т)",
                  "Фунт (lb)", "Унция (oz)", "Карат (ct)"],
        "to_base": {
            "Килограмм (кг)": 1, "Грамм (г)": 1e-3, "Миллиграмм (мг)": 1e-6,
            "Тонна (т)": 1e3, "Фунт (lb)": 0.453592, "Унция (oz)": 0.0283495,
            "Карат (ct)": 2e-4
        },
        "temp": False
    },
    "🌡️  Температура": {
        "units": ["Цельсий (°C)", "Фаренгейт (°F)", "Кельвин (K)", "Ранкин (°R)"],
        "to_base": {},
        "temp": True
    },
    "⚡  Скорость": {
        "units": ["м/с", "км/ч", "Миля/ч (mph)", "Узел (kn)", "Фут/с (ft/s)",
                  "Скорость света (c)"],
        "to_base": {
            "м/с": 1, "км/ч": 1/3.6, "Миля/ч (mph)": 0.44704,
            "Узел (kn)": 0.514444, "Фут/с (ft/s)": 0.3048,
            "Скорость света (c)": 299792458
        },
        "temp": False
    },
    "⚡  Энергия": {
        "units": ["Джоуль (Дж)", "Килоджоуль (кДж)", "МегаДж (МДж)", "Калория (кал)",
                  "Килокалория (ккал)", "эВ (электронвольт)", "кВт·ч", "Эрг"],
        "to_base": {
            "Джоуль (Дж)": 1, "Килоджоуль (кДж)": 1e3, "МегаДж (МДж)": 1e6,
            "Калория (кал)": 4.184, "Килокалория (ккал)": 4184,
            "эВ (электронвольт)": 1.602176634e-19, "кВт·ч": 3.6e6, "Эрг": 1e-7
        },
        "temp": False
    },
    "🔵  Давление": {
        "units": ["Паскаль (Па)", "Килопаскаль (кПа)", "МегаПаскаль (МПа)",
                  "Атмосфера (атм)", "Бар (bar)", "мм рт.ст. (mmHg)",
                  "мм вод.ст. (mmH₂O)", "PSI (фунт/дюйм²)"],
        "to_base": {
            "Паскаль (Па)": 1, "Килопаскаль (кПа)": 1e3, "МегаПаскаль (МПа)": 1e6,
            "Атмосфера (атм)": 101325, "Бар (bar)": 1e5,
            "мм рт.ст. (mmHg)": 133.322, "мм вод.ст. (mmH₂O)": 9.80665,
            "PSI (фунт/дюйм²)": 6894.76
        },
        "temp": False
    },
}

def convert_temperature(value, from_unit, to_unit):
    # Привести к Цельсию
    if from_unit == "Цельсий (°C)":
        c = value
    elif from_unit == "Фаренгейт (°F)":
        c = (value - 32) * 5/9
    elif from_unit == "Кельвин (K)":
        c = value - 273.15
    elif from_unit == "Ранкин (°R)":
        c = (value - 491.67) * 5/9
    # Из Цельсия в нужную
    if to_unit == "Цельсий (°C)":
        return c
    elif to_unit == "Фаренгейт (°F)":
        return c * 9/5 + 32
    elif to_unit == "Кельвин (K)":
        return c + 273.15
    elif to_unit == "Ранкин (°R)":
        return (c + 273.15) * 9/5

def format_result(value):
    if abs(value) == 0:
        return "0"
    if abs(value) >= 1e9 or (abs(value) < 1e-4 and abs(value) > 0):
        return f"{value:.6e}"
    if abs(value) >= 1000:
        return f"{value:,.6f}".rstrip('0').rstrip('.')
    return f"{value:.8f}".rstrip('0').rstrip('.')

class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Конвертер физических величин")
        self.geometry("820x560")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.current_category = list(CATEGORIES.keys())[0]
        self._build_ui()

    def _build_ui(self):
        # ── SIDEBAR ──
        sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="⚗️", font=("Segoe UI Emoji", 28),
                 bg=SIDEBAR_BG, fg=ACCENT).pack(pady=(24, 0))
        tk.Label(sidebar, text="Конвертер\nвеличин", font=("Segoe UI", 11, "bold"),
                 bg=SIDEBAR_BG, fg=TEXT, justify="center").pack(pady=(4, 20))

        tk.Frame(sidebar, bg=CARD_BG, height=1).pack(fill="x", padx=16, pady=4)

        self.btn_refs = {}
        for cat in CATEGORIES:
            btn = tk.Button(
                sidebar, text=cat, font=("Segoe UI", 10),
                bg=SIDEBAR_BG, fg=TEXT_SUB,
                activebackground=CARD_BG, activeforeground=TEXT,
                relief="flat", anchor="w", padx=16, pady=8, cursor="hand2",
                command=lambda c=cat: self._switch_category(c)
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.btn_refs[cat] = btn

        tk.Frame(sidebar, bg=CARD_BG, height=1).pack(fill="x", padx=16, pady=12)
        tk.Label(sidebar, text="by miziev-dev", font=("Segoe UI", 8),
                 bg=SIDEBAR_BG, fg=TEXT_SUB).pack(side="bottom", pady=12)

        # ── MAIN AREA ──
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self._build_converter_panel()
        self._switch_category(self.current_category)

    def _build_converter_panel(self):
        # Заголовок
        header = tk.Frame(self.main, bg=BG)
        header.pack(fill="x", padx=32, pady=(28, 0))

        self.title_label = tk.Label(
            header, text="", font=("Segoe UI", 18, "bold"),
            bg=BG, fg=TEXT
        )
        self.title_label.pack(anchor="w")
        self.sub_label = tk.Label(
            header, text="", font=("Segoe UI", 10),
            bg=BG, fg=TEXT_SUB
        )
        self.sub_label.pack(anchor="w", pady=(2, 0))

        tk.Frame(self.main, bg=CARD_BG, height=1).pack(fill="x", padx=32, pady=16)

        # Карточка FROM
        card_from = tk.Frame(self.main, bg=CARD_BG, bd=0)
        card_from.pack(fill="x", padx=32, pady=(0, 12))
        tk.Label(card_from, text="  ИЗ", font=("Segoe UI", 9, "bold"),
                 bg=CARD_BG, fg=ACCENT).pack(anchor="w", padx=12, pady=(12, 4))

        row_from = tk.Frame(card_from, bg=CARD_BG)
        row_from.pack(fill="x", padx=12, pady=(0, 14))

        self.entry_var = tk.StringVar(value="1")
        self.entry = tk.Entry(
            row_from, textvariable=self.entry_var,
            font=("Consolas", 20, "bold"),
            bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", bd=0, width=14
        )
        self.entry.pack(side="left", ipady=10, ipadx=12)
        self.entry.bind("<KeyRelease>", lambda e: self._convert())

        self.from_var = tk.StringVar()
        self.from_cb = ttk.Combobox(
            row_from, textvariable=self.from_var,
            font=("Segoe UI", 11), state="readonly", width=26
        )
        self.from_cb.pack(side="left", padx=(12, 0), ipady=8)
        self.from_cb.bind("<<ComboboxSelected>>", lambda e: self._convert())

        # Стрелка
        arrow_frame = tk.Frame(self.main, bg=BG)
        arrow_frame.pack()
        tk.Label(arrow_frame, text="↕", font=("Segoe UI", 20),
                 bg=BG, fg=ACCENT).pack()

        # Карточка TO
        card_to = tk.Frame(self.main, bg=CARD_BG, bd=0)
        card_to.pack(fill="x", padx=32, pady=(0, 20))
        tk.Label(card_to, text="  В", font=("Segoe UI", 9, "bold"),
                 bg=CARD_BG, fg=ACCENT2).pack(anchor="w", padx=12, pady=(12, 4))

        row_to = tk.Frame(card_to, bg=CARD_BG)
        row_to.pack(fill="x", padx=12, pady=(0, 14))

        self.result_var = tk.StringVar(value="—")
        self.result_label = tk.Label(
            row_to, textvariable=self.result_var,
            font=("Consolas", 20, "bold"),
            bg=ENTRY_BG, fg=SUCCESS,
            width=14, anchor="w", padx=12, pady=10
        )
        self.result_label.pack(side="left")

        self.to_var = tk.StringVar()
        self.to_cb = ttk.Combobox(
            row_to, textvariable=self.to_var,
            font=("Segoe UI", 11), state="readonly", width=26
        )
        self.to_cb.pack(side="left", padx=(12, 0), ipady=8)
        self.to_cb.bind("<<ComboboxSelected>>", lambda e: self._convert())

        # Кнопки
        btn_frame = tk.Frame(self.main, bg=BG)
        btn_frame.pack(pady=4)

        def make_btn(parent, text, cmd, color=BTN_BG):
            b = tk.Button(parent, text=text, font=("Segoe UI", 10, "bold"),
                          bg=color, fg=BTN_FG, activebackground=HOVER,
                          relief="flat", padx=24, pady=8, cursor="hand2",
                          command=cmd)
            b.pack(side="left", padx=6)
            return b

        make_btn(btn_frame, "⇄  Поменять местами", self._swap)
        make_btn(btn_frame, "✕  Очистить", self._clear, ENTRY_BG)

        # Стили для Combobox
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=ENTRY_BG, background=CARD_BG,
                        foreground=TEXT, selectbackground=ACCENT,
                        selectforeground=BTN_FG, arrowcolor=ACCENT)
        style.map("TCombobox", fieldbackground=[("readonly", ENTRY_BG)],
                  foreground=[("readonly", TEXT)])

    def _switch_category(self, cat):
        self.current_category = cat
        data = CATEGORIES[cat]
        units = data["units"]

        # Обновить заголовок
        self.title_label.config(text=cat)
        self.sub_label.config(text=f"{len(units)} единиц измерения")

        # Обновить комбобоксы
        self.from_cb["values"] = units
        self.to_cb["values"] = units
        self.from_var.set(units[0])
        self.to_var.set(units[1] if len(units) > 1 else units[0])
        self.entry_var.set("1")

        # Обновить стиль кнопок в сайдбаре
        for c, btn in self.btn_refs.items():
            if c == cat:
                btn.config(bg=CARD_BG, fg=ACCENT, font=("Segoe UI", 10, "bold"))
            else:
                btn.config(bg=SIDEBAR_BG, fg=TEXT_SUB, font=("Segoe UI", 10))

        self._convert()

    def _convert(self):
        try:
            raw = self.entry_var.get().replace(",", ".").strip()
            if not raw:
                self.result_var.set("—")
                return
            value = float(raw)
        except ValueError:
            self.result_var.set("Ошибка")
            self.result_label.config(fg="#f38ba8")
            return

        self.result_label.config(fg=SUCCESS)
        data = CATEGORIES[self.current_category]
        from_u = self.from_var.get()
        to_u   = self.to_var.get()

        if data["temp"]:
            result = convert_temperature(value, from_u, to_u)
        else:
            base = value * data["to_base"][from_u]
            result = base / data["to_base"][to_u]

        self.result_var.set(format_result(result))

    def _swap(self):
        f = self.from_var.get()
        t = self.to_var.get()
        self.from_var.set(t)
        self.to_var.set(f)
        self._convert()

    def _clear(self):
        self.entry_var.set("")
        self.result_var.set("—")
        self.result_label.config(fg=SUCCESS)

if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()