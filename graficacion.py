import sys, os, csv
import pandas as pd
from datetime import date
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QMessageBox, QCalendarWidget, QDialog,
    QLineEdit, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

base = Path(__file__).resolve().parent
archivo = str(base / "ventasdiarias.txt")


class canvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(7, 4), tight_layout=True)
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)

    def plot(self, x, y, kind="line", title="", xlabel="", ylabel=""):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        if kind == "line":
            self.ax.plot(x, y, marker="o")
        elif kind == "bar":
            self.ax.bar(x, y)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.grid(True, alpha=0.3)
        self.draw()


class registrowindow(QDialog):
    def __init__(self, parent=None, on_saved=None):
        super().__init__(parent)
        self.setWindowTitle("gestión de ventas")
        self.setMinimumSize(600, 400)
        self.on_saved = on_saved
        self.setStyleSheet("""
        QMainWindow { background:#0f172a; }
        QLabel { color:#e5e7eb; font-size:14px; }

        QPushButton {
            background:#22c55e; color:white; border:none; padding:10px 16px;
            border-radius:8px; font-size:14px;
        }
        QPushButton:hover { background:#16a34a; }

        #panel { background:#111827; border:1px solid #374151; border-radius:12px; }

        /* ComboBox */
        QComboBox {
            background:#111827;
            color:#e5e7eb;
            padding:6px;
            border:1px solid #374151;
            border-radius:6px;
        }
        QComboBox QAbstractItemView {
            background:#1f2937;
            color:#e5e7eb;
            selection-background-color:#2563eb;
            selection-color:white;
            border:1px solid #374151;
        }

        /* Calendar */
        QCalendarWidget {
            background:#111827;
            border:1px solid #374151;
            border-radius:10px;
        }
        QCalendarWidget QWidget { background:#111827; color:#e5e7eb; selection-background-color:#2563eb; }
        QCalendarWidget QToolButton { color:#e5e7eb; background:#1f2937; border:0; padding:6px; border-radius:6px; }
        QCalendarWidget QMenu { background:#111827; color:#e5e7eb; }
        QCalendarWidget QSpinBox { background:#111827; color:#e5e7eb; }
        QCalendarWidget QAbstractItemView:enabled { selection-background-color:#2563eb; selection-color:white; }
        """)

        layout = QVBoxLayout(self)

        self.tab = QTableWidget(0, 3)
        self.tab.setHorizontalHeaderLabels(["fecha", "hora", "ventas"])
        layout.addWidget(self.tab)

        form = QHBoxLayout()
        self.ed_fecha = QLineEdit()
        self.ed_fecha.setPlaceholderText("yyyy-mm-dd")
        self.ed_hora = QLineEdit()
        self.ed_hora.setPlaceholderText("hh:mm")
        self.ed_ventas = QLineEdit()
        self.ed_ventas.setValidator(QIntValidator(0, 100000))
        self.ed_ventas.setPlaceholderText("cantidad")
        form.addWidget(QLabel("fecha"))
        form.addWidget(self.ed_fecha)
        form.addWidget(QLabel("hora"))
        form.addWidget(self.ed_hora)
        form.addWidget(QLabel("ventas"))
        form.addWidget(self.ed_ventas)
        layout.addLayout(form)

        row_btns = QHBoxLayout()
        self.btn_add = QPushButton("añadir")
        self.btn_upd = QPushButton("actualizar")
        self.btn_del = QPushButton("borrar")
        self.btn_save = QPushButton("guardar")
        self.btn_close = QPushButton("cerrar")
        row_btns.addWidget(self.btn_add)
        row_btns.addWidget(self.btn_upd)
        row_btns.addWidget(self.btn_del)
        row_btns.addWidget(self.btn_save)
        row_btns.addWidget(self.btn_close)
        layout.addLayout(row_btns)

        self.btn_add.clicked.connect(self.add_row_from_form)
        self.btn_upd.clicked.connect(self.update_selected_from_form)
        self.btn_del.clicked.connect(self.delete_selected)
        self.btn_save.clicked.connect(self.save)
        self.btn_close.clicked.connect(self.accept)
        self.tab.itemSelectionChanged.connect(self.sync_form_from_selection)

        self.load_data()

    def load_data(self):
        self.tab.setRowCount(0)
        if not os.path.exists(archivo):
            return
        with open(archivo, encoding="utf-8") as fh:
            next(fh, None)
            for line in fh:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    r = self.tab.rowCount()
                    self.tab.insertRow(r)
                    for c, val in enumerate(parts):
                        self.tab.setItem(r, c, QTableWidgetItem(val))

    def add_row_from_form(self):
        f = self.ed_fecha.text().strip()
        h = self.ed_hora.text().strip()
        v = self.ed_ventas.text().strip()
        if not f or not h or not v:
            QMessageBox.warning(self, "error", "completa todos los campos")
            return
        r = self.tab.rowCount()
        self.tab.insertRow(r)
        self.tab.setItem(r, 0, QTableWidgetItem(f))
        self.tab.setItem(r, 1, QTableWidgetItem(h))
        self.tab.setItem(r, 2, QTableWidgetItem(v))
        self.clear_form()

    def update_selected_from_form(self):
        r = self.tab.currentRow()
        if r < 0:
            return
        self.tab.setItem(r, 0, QTableWidgetItem(self.ed_fecha.text().strip()))
        self.tab.setItem(r, 1, QTableWidgetItem(self.ed_hora.text().strip()))
        self.tab.setItem(r, 2, QTableWidgetItem(self.ed_ventas.text().strip()))

    def delete_selected(self):
        r = self.tab.currentRow()
        if r >= 0:
            self.tab.removeRow(r)

    def sync_form_from_selection(self):
        r = self.tab.currentRow()
        if r < 0:
            return
        self.ed_fecha.setText(self.tab.item(r, 0).text())
        self.ed_hora.setText(self.tab.item(r, 1).text())
        self.ed_ventas.setText(self.tab.item(r, 2).text())

    def clear_form(self):
        self.ed_fecha.clear()
        self.ed_hora.clear()
        self.ed_ventas.clear()

    def save(self):
        filas = []
        for r in range(self.tab.rowCount()):
            f = (self.tab.item(r, 0).text() if self.tab.item(r, 0) else "").strip()
            h = (self.tab.item(r, 1).text() if self.tab.item(r, 1) else "").strip()
            v = (self.tab.item(r, 2).text() if self.tab.item(r, 2) else "").strip()
            try:
                v = int(v)
            except ValueError:
                v = 0
            if f and h:
                filas.append(f"{f},{h},{v}")
        with open(archivo, "w", encoding="utf-8") as fh:
            fh.write("fecha,hora,ventas\n")
            fh.write("\n".join(filas))
        if self.on_saved:
            self.on_saved()
        QMessageBox.information(self, "ok", "registros guardados")
        self.accept()


class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graficación De Ventas por Hora")
        self.asegurar_archivo()
        self.df = self.cargar_df()
        self.resize(980, 560)
        QApplication.setStyle("Fusion")

        left = QWidget(objectName="panel")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(18, 18, 18, 18)

        t = QLabel("selecciona periodo")
        t.setFont(QFont("segoe ui", 16, QFont.Bold))
        left_layout.addWidget(t)

        self.cal = QCalendarWidget()
        self.cal.setGridVisible(True)
        left_layout.addWidget(QLabel("día"))
        left_layout.addWidget(self.cal)

        row_mes = QHBoxLayout()
        self.cmb_mes = QComboBox()
        self.cmb_mes.addItems([
            "01 enero","02 febrero","03 marzo","04 abril","05 mayo","06 junio",
            "07 julio","08 agosto","09 septiembre","10 octubre","11 noviembre","12 diciembre"
        ])
        self.cmb_anio_m = QComboBox()
        self.cmb_anio_m.addItems([str(a) for a in range(2025, 2036)])
        row_mes.addWidget(QLabel("mes"))
        row_mes.addWidget(self.cmb_mes)
        row_mes.addWidget(QLabel("año"))
        row_mes.addWidget(self.cmb_anio_m)
        left_layout.addLayout(row_mes)

        self.btn_registro = QPushButton("abrir registro")
        self.btn_dia = QPushButton("graficar día")
        self.btn_mes = QPushButton("graficar mes")
        self.btn_anio = QPushButton("graficar año")
        left_layout.addWidget(self.btn_registro)
        left_layout.addWidget(self.btn_dia)
        left_layout.addWidget(self.btn_mes)
        left_layout.addWidget(self.btn_anio)
        left_layout.addStretch(1)

        self.canvas = canvas()

        root = QWidget()
        main = QHBoxLayout(root)
        main.addWidget(left, 0)
        main.addWidget(self.canvas, 1)
        self.setCentralWidget(root)

        self.btn_registro.clicked.connect(self.abrir_registro)
        self.btn_dia.clicked.connect(self.graficar_dia)
        self.btn_mes.clicked.connect(self.graficar_mes)
        self.btn_anio.clicked.connect(self.graficar_anio)

    def asegurar_archivo(self):
        p = Path(archivo)
        if not p.exists() or p.stat().st_size == 0:
            p.write_text("fecha,hora,ventas\n", encoding="utf-8-sig")

    def cargar_df(self):
        cols = ["fecha","hora","ventas"]
        if not os.path.exists(archivo):
            return pd.DataFrame(columns=cols)
        df = pd.read_csv(archivo)
        if {"fecha","hora","ventas"} - set(df.columns):
            return pd.DataFrame(columns=cols)
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df = df.dropna(subset=["fecha"])
        df["hora"] = df["hora"].astype(str).str.strip()
        df["ventas"] = pd.to_numeric(df["ventas"], errors="coerce").fillna(0).astype(int)
        return df

    def refrescar(self):
        self.df = self.cargar_df()

    def abrir_registro(self):
        dlg = registrowindow(parent=self, on_saved=self.refrescar)
        dlg.exec_()

    def graficar_dia(self):
        d = self.cal.selectedDate()
        f = date(d.year(), d.month(), d.day())
        sub = self.df[self.df["fecha"].dt.date == f]
        if sub.empty:
            QMessageBox.information(self, "sin datos", f"no hay registros para {f.isoformat()}")
            return
        g = sub.groupby("hora")["ventas"].sum().reset_index()
        self.canvas.plot(g["hora"], g["ventas"], kind="line",
                         title=f"ventas del {f.isoformat()}", xlabel="hora", ylabel="ventas")

    def graficar_mes(self):
        mes_idx = int(self.cmb_mes.currentText().split()[0])
        anio = int(self.cmb_anio_m.currentText())
        sub = self.df[(self.df["fecha"].dt.year == anio) & (self.df["fecha"].dt.month == mes_idx)]
        if sub.empty:
            QMessageBox.information(self, "sin datos", f"no hay registros para {self.cmb_mes.currentText()} {anio}")
            return
        g = sub.groupby(sub["fecha"].dt.day)["ventas"].sum().reset_index()
        self.canvas.plot(g["fecha"], g["ventas"], kind="line",
                         title=f"ventas de {self.cmb_mes.currentText()} {anio}", xlabel="día", ylabel="ventas")

    def graficar_anio(self):
        anio = int(self.cmb_anio_m.currentText())
        sub = self.df[self.df["fecha"].dt.year == anio]
        if sub.empty:
            QMessageBox.information(self, "sin datos", f"no hay registros para {anio}")
            return
        g = sub.groupby(sub["fecha"].dt.month)["ventas"].sum().reset_index()
        meses = ["e","f","m","a","m","j","j","a","s","o","n","d"]
        x = [meses[i-1] for i in g["fecha"].tolist()]
        self.canvas.plot(x, g["ventas"], kind="bar",
                         title=f"ventas del año {anio}", xlabel="mes", ylabel="ventas")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = mainwindow()
    w.show()
    sys.exit(app.exec_())