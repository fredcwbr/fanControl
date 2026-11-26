#!/usr/bin/env python3
"""
Opção 3: Dashboard Gráfico (GUI) em Python/Tkinter
Monitor de Sensores hwmon, Ventoinhas, SMART, RAID (md) e LVM (VGs & LVs).
"""

import os
import sys
import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from monitor import HwmonMonitor, SmartMonitor, RaidMonitor, LvmMonitor

class FanControlGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("⚡ FanControl - Hardware, SMART, RAID & LVM")
        self.geometry("1100x720")
        self.minsize(900, 580)

        # Dark theme styling
        self.bg_color = "#181825"
        self.card_bg = "#1e1e2e"
        self.accent_color = "#89b4fa"
        self.text_color = "#cdd6f4"
        self.text_dim = "#a6adc8"
        self.green = "#a6e3a1"
        self.yellow = "#f9e2af"
        self.red = "#f38ba8"

        self.configure(bg=self.bg_color)

        self.hw_mon = HwmonMonitor()
        self.smart_mon = SmartMonitor()
        self.raid_mon = RaidMonitor()
        self.lvm_mon = LvmMonitor()

        self.demo_mode = tk.BooleanVar(value=False)
        self.auto_refresh = tk.BooleanVar(value=True)
        self.refresh_interval_ms = 1500

        self.disks = self.smart_mon.list_disks()

        self.setup_styles()
        self.build_ui()

        # Start periodic update
        self.after(200, self.update_data_loop)

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".", background=self.bg_color, foreground=self.text_color)
        style.configure("TFrame", background=self.bg_color)
        style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Sans", 10))
        style.configure("Card.TLabel", background=self.card_bg, foreground=self.text_color, font=("Sans", 10))
        style.configure("Header.TLabel", background=self.bg_color, foreground=self.accent_color, font=("Sans", 14, "bold"))
        style.configure("SubHeader.TLabel", background=self.card_bg, foreground=self.accent_color, font=("Sans", 11, "bold"))

        style.configure("Treeview",
                        background=self.card_bg,
                        foreground=self.text_color,
                        fieldbackground=self.card_bg,
                        rowheight=28,
                        font=("Sans", 10))
        style.configure("Treeview.Heading",
                        background="#313244",
                        foreground=self.accent_color,
                        font=("Sans", 10, "bold"),
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", "#45475a")],
                  foreground=[("selected", "#ffffff")])

        # Progressbar
        style.configure("Green.Horizontal.TProgressbar", foreground=self.green, background=self.green, troughcolor="#313244")
        style.configure("Yellow.Horizontal.TProgressbar", foreground=self.yellow, background=self.yellow, troughcolor="#313244")
        style.configure("Red.Horizontal.TProgressbar", foreground=self.red, background=self.red, troughcolor="#313244")

        # Buttons
        style.configure("TButton", background="#313244", foreground=self.text_color, borderwidth=0, font=("Sans", 9, "bold"))
        style.map("TButton", background=[("active", "#45475a")])
        style.configure("TCheckbutton", background=self.bg_color, foreground=self.text_color, font=("Sans", 9))

    def build_ui(self):
        # 1. Top Bar
        top_bar = ttk.Frame(self, padding=12)
        top_bar.pack(fill=tk.X, side=tk.TOP)

        title_lbl = ttk.Label(top_bar, text="⚡ FanControl Dashboard", style="Header.TLabel")
        title_lbl.pack(side=tk.LEFT)

        is_root = (os.geteuid() == 0)
        perm_text = "● Modo Root Ativo" if is_root else "▲ Não-Root (SMART: use sudo)"
        perm_color = self.green if is_root else self.yellow
        perm_lbl = tk.Label(top_bar, text=perm_text, bg=self.bg_color, fg=perm_color, font=("Sans", 9, "bold"))
        perm_lbl.pack(side=tk.LEFT, padx=16)

        # Controls on Right
        btn_refresh = ttk.Button(top_bar, text="🔄 Atualizar Agora", command=self.refresh_once)
        btn_refresh.pack(side=tk.RIGHT, padx=4)

        chk_demo = ttk.Checkbutton(top_bar, text="Modo Demonstração (SMART)", variable=self.demo_mode, command=self.refresh_once)
        chk_demo.pack(side=tk.RIGHT, padx=10)

        chk_auto = ttk.Checkbutton(top_bar, text="Auto-Refresh", variable=self.auto_refresh)
        chk_auto.pack(side=tk.RIGHT, padx=6)

        # 2. Main Content Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        # Tab 1: SMART Disks
        self.tab_smart = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.tab_smart, text=" 💾 Discos & SMART ")

        # Tab 2: RAID (md)
        self.tab_raid = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.tab_raid, text=" 🛡️ RAID (mdstat) ")

        # Tab 3: LVM (VGs & LVs)
        self.tab_lvm = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.tab_lvm, text=" 📦 LVM (VGs & LVs) ")

        # Tab 4: HWMON & Fans
        self.tab_hwmon = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.tab_hwmon, text=" 🌡️ Sensores Térmicos & Fans ")

        self.build_smart_tab()
        self.build_raid_tab()
        self.build_lvm_tab()
        self.build_hwmon_tab()

        # 3. Status Bar
        status_bar = ttk.Frame(self, padding=(12, 6))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_lbl = ttk.Label(status_bar, text="Pronto.", font=("Sans", 9))
        self.status_lbl.pack(side=tk.LEFT)
        self.clock_lbl = ttk.Label(status_bar, text="", font=("Sans", 9))
        self.clock_lbl.pack(side=tk.RIGHT)

    def build_smart_tab(self):
        columns = ("dev", "model", "type", "size", "temp", "status", "health", "realloc", "pending", "uncorr", "crc", "ata_err")
        self.smart_tree = ttk.Treeview(self.tab_smart, columns=columns, show="headings", height=8)

        self.smart_tree.heading("dev", text="Disco")
        self.smart_tree.heading("model", text="Modelo")
        self.smart_tree.heading("type", text="Tipo")
        self.smart_tree.heading("size", text="Tamanho")
        self.smart_tree.heading("temp", text="Temp (°C)")
        self.smart_tree.heading("status", text="Status SMART")
        self.smart_tree.heading("health", text="Saúde")
        self.smart_tree.heading("realloc", text="Setores Realocados (ID 5)")
        self.smart_tree.heading("pending", text="Pendentes (ID 197)")
        self.smart_tree.heading("uncorr", text="Não Corrigíveis (ID 198)")
        self.smart_tree.heading("crc", text="Erros CRC (ID 199)")
        self.smart_tree.heading("ata_err", text="Erros ATA Log")

        self.smart_tree.column("dev", width=70, anchor="center")
        self.smart_tree.column("model", width=160, anchor="w")
        self.smart_tree.column("type", width=60, anchor="center")
        self.smart_tree.column("size", width=70, anchor="center")
        self.smart_tree.column("temp", width=80, anchor="center")
        self.smart_tree.column("status", width=100, anchor="center")
        self.smart_tree.column("health", width=75, anchor="center")
        self.smart_tree.column("realloc", width=140, anchor="center")
        self.smart_tree.column("pending", width=120, anchor="center")
        self.smart_tree.column("uncorr", width=135, anchor="center")
        self.smart_tree.column("crc", width=110, anchor="center")
        self.smart_tree.column("ata_err", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(self.tab_smart, orient=tk.VERTICAL, command=self.smart_tree.yview)
        self.smart_tree.configure(yscroll=scrollbar.set)

        self.smart_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        info_frame = ttk.Frame(self.tab_smart, style="Card.TFrame", padding=10)
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        legend_text = (
            "📌 Guia de Erros SMART:\n"
            "• Setores Realocados (ID 5): Setores com defeito físico movidos para área reserva. Valor > 0 indica degradação da mídia.\n"
            "• Setores Pendentes (ID 197): Setores instáveis aguardando remapeamento.\n"
            "• Não Corrigíveis (ID 198): Falhas irrecuperáveis durante leitura/escrita.\n"
            "• Erros CRC (ID 199): Problemas de integridade na interface SATA (cabo defeituoso ou mal encaixado)."
        )
        lbl_legend = ttk.Label(info_frame, text=legend_text, style="Card.TLabel", justify="left")
        lbl_legend.pack(anchor="w")

    def build_raid_tab(self):
        columns = ("array", "level", "size", "health", "state", "disks", "sync", "members")
        self.raid_tree = ttk.Treeview(self.tab_raid, columns=columns, show="headings", height=8)

        self.raid_tree.heading("array", text="Array RAID")
        self.raid_tree.heading("level", text="Nível")
        self.raid_tree.heading("size", text="Tamanho")
        self.raid_tree.heading("health", text="Saúde / Máscara")
        self.raid_tree.heading("state", text="Estado")
        self.raid_tree.heading("disks", text="Discos (Ativos/Total)")
        self.raid_tree.heading("sync", text="Sincronização")
        self.raid_tree.heading("members", text="Componentes & Erros")

        self.raid_tree.column("array", width=90, anchor="center")
        self.raid_tree.column("level", width=80, anchor="center")
        self.raid_tree.column("size", width=80, anchor="center")
        self.raid_tree.column("health", width=140, anchor="center")
        self.raid_tree.column("state", width=90, anchor="center")
        self.raid_tree.column("disks", width=130, anchor="center")
        self.raid_tree.column("sync", width=100, anchor="center")
        self.raid_tree.column("members", width=360, anchor="w")

        scrollbar = ttk.Scrollbar(self.tab_raid, orient=tk.VERTICAL, command=self.raid_tree.yview)
        self.raid_tree.configure(yscroll=scrollbar.set)

        self.raid_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        card = ttk.Frame(self.tab_raid, style="Card.TFrame", padding=10)
        card.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        r_text = (
            "📌 Status do RAID (mdstat):\n"
            "• [UU]: Todos os discos ativos e sincronizados (Saudável).\n"
            "• [_UU] ou [U_]: Array DEGRADADO! Um ou mais discos falharam ou foram removidos.\n"
            "• Sincronização: Indica se o array está executando reconstrução (rebuild/recovery), verificação ou idle."
        )
        ttk.Label(card, text=r_text, style="Card.TLabel").pack(anchor="w")

    def build_lvm_tab(self):
        columns = ("vg", "lv", "dm", "size", "path")
        self.lvm_tree = ttk.Treeview(self.tab_lvm, columns=columns, show="headings", height=10)

        self.lvm_tree.heading("vg", text="Volume Group (VG)")
        self.lvm_tree.heading("lv", text="Logical Volume (LV)")
        self.lvm_tree.heading("dm", text="Dispositivo DM")
        self.lvm_tree.heading("size", text="Tamanho")
        self.lvm_tree.heading("path", text="Caminho /dev/mapper")

        self.lvm_tree.column("vg", width=130, anchor="center")
        self.lvm_tree.column("lv", width=160, anchor="w")
        self.lvm_tree.column("dm", width=90, anchor="center")
        self.lvm_tree.column("size", width=90, anchor="center")
        self.lvm_tree.column("path", width=300, anchor="w")

        scrollbar = ttk.Scrollbar(self.tab_lvm, orient=tk.VERTICAL, command=self.lvm_tree.yview)
        self.lvm_tree.configure(yscroll=scrollbar.set)

        self.lvm_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        card = ttk.Frame(self.tab_lvm, style="Card.TFrame", padding=10)
        card.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        self.lvm_summary_lbl = ttk.Label(card, text="Carregando VGs...", style="Card.TLabel")
        self.lvm_summary_lbl.pack(anchor="w")

    def build_hwmon_tab(self):
        self.hwmon_canvas = tk.Canvas(self.tab_hwmon, bg=self.bg_color, highlightthickness=0)
        hwmon_scroll = ttk.Scrollbar(self.tab_hwmon, orient=tk.VERTICAL, command=self.hwmon_canvas.yview)
        self.hwmon_container = ttk.Frame(self.hwmon_canvas)

        self.hwmon_container.bind("<Configure>", lambda e: self.hwmon_canvas.configure(scrollregion=self.hwmon_canvas.bbox("all")))
        self.hwmon_canvas.create_window((0, 0), window=self.hwmon_container, anchor="nw")
        self.hwmon_canvas.configure(yscrollcommand=hwmon_scroll.set)

        self.hwmon_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        hwmon_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_once(self):
        threading.Thread(target=self._fetch_and_render, daemon=True).start()

    def update_data_loop(self):
        if self.auto_refresh.get():
            self.refresh_once()
        self.after(self.refresh_interval_ms, self.update_data_loop)

    def _fetch_and_render(self):
        hw_sensors = self.hw_mon.get_sensors()
        demo = self.demo_mode.get()
        smart_data = [self.smart_mon.get_disk_smart(d, demo_mode=demo) for d in self.disks]
        raids = self.raid_mon.get_arrays()
        lvm = self.lvm_mon.get_lvm_info()

        self.after(0, lambda: self._apply_data(hw_sensors, smart_data, raids, lvm))

    def _apply_data(self, hw_sensors, smart_data, raids, lvm):
        # 1. Update SMART Tree
        for item in self.smart_tree.get_children():
            self.smart_tree.delete(item)

        for d in smart_data:
            if not d:
                continue

            if d.get("error_msg"):
                status_str = "🔒 Sem Acesso"
                temp_str = "-"
                health_str = "--"
                realloc = "-"
                pending = "-"
                uncorr = "-"
                crc = "-"
                ata_err = "-"
            else:
                temp_str = f"{d['temp']} °C" if d.get("temp") is not None else "--"
                status_str = d.get("status", "UNKNOWN")
                health_str = f"{d['health_percent']}%" if d.get("health_percent") is not None else "--"
                realloc = str(d.get("reallocated_sectors", 0))
                pending = str(d.get("pending_sectors", 0))
                uncorr = str(d.get("uncorrectable_sectors", 0))
                crc = str(d.get("crc_errors", 0))
                ata_err = str(d.get("ata_errors", 0))

            self.smart_tree.insert("", tk.END, values=(
                d.get("name", "--"),
                d.get("model", "--"),
                d.get("type", "--"),
                f"{d.get('size_gb', 0)} GB",
                temp_str,
                status_str,
                health_str,
                realloc,
                pending,
                uncorr,
                crc,
                ata_err
            ))

        # 2. Update RAID Tree
        for item in self.raid_tree.get_children():
            self.raid_tree.delete(item)

        for r in raids:
            health_str = f"▲ DEGRADADO {r['health_mask']}" if r["degraded"] else f"● OK {r['health_mask']}"
            disks_str = f"{r['active_disks']}/{r['total_disks']}"

            members_summary = ", ".join([f"{m['name']}({m['state']}{',err:'+str(m['errors']) if m['errors']>0 else ''})" for m in r["members"]])

            self.raid_tree.insert("", tk.END, values=(
                r["name"],
                r["level"],
                f"{r['size_gb']} GB",
                health_str,
                r["state"].upper(),
                disks_str,
                r["sync_action"],
                members_summary
            ))

        # 3. Update LVM Tree
        for item in self.lvm_tree.get_children():
            self.lvm_tree.delete(item)

        for lv in lvm.get("lvs", []):
            self.lvm_tree.insert("", tk.END, values=(
                lv["vg"],
                lv["lv"],
                lv["dm"],
                f"{lv['size_gb']} GB",
                lv["path"]
            ))

        vgs_summary = " | ".join([f"VG {v['name']}: {v['total_lvs']} LVs ({v['allocated_gb']} GB alocados)" for v in lvm.get("vgs", [])])
        self.lvm_summary_lbl.config(text=f"📦 Resumo dos Volume Groups: {vgs_summary if vgs_summary else 'Nenhum VG detectado'}")

        # 4. Update Hwmon Cards
        for widget in self.hwmon_container.winfo_children():
            widget.destroy()

        for dev in hw_sensors:
            card = ttk.Frame(self.hwmon_container, style="Card.TFrame", padding=10)
            card.pack(fill=tk.X, expand=True, padx=8, pady=6)

            title = f"{dev['id']}: {dev['name'].upper()}"
            ttk.Label(card, text=title, style="SubHeader.TLabel").pack(anchor="w", pady=(0, 6))

            for t in dev["temps"]:
                row = ttk.Frame(card, style="Card.TFrame")
                row.pack(fill=tk.X, pady=2)

                lbl = ttk.Label(row, text=f"{t['label']}:", style="Card.TLabel", width=22)
                lbl.pack(side=tk.LEFT)

                temp_val = t["temp"]
                p_style = "Green.Horizontal.TProgressbar"
                if temp_val >= 80: p_style = "Red.Horizontal.TProgressbar"
                elif temp_val >= 55: p_style = "Yellow.Horizontal.TProgressbar"

                pb = ttk.Progressbar(row, length=180, mode="determinate", value=min(temp_val, 100), style=p_style)
                pb.pack(side=tk.LEFT, padx=10)

                v_lbl = ttk.Label(row, text=f"{temp_val:5.1f} °C", style="Card.TLabel", width=10)
                v_lbl.pack(side=tk.LEFT)

            for fan in dev["fans"]:
                row = ttk.Frame(card, style="Card.TFrame")
                row.pack(fill=tk.X, pady=2)
                ttk.Label(row, text=f"Ventoinha ({fan['label']}):", style="Card.TLabel", width=22).pack(side=tk.LEFT)
                ttk.Label(row, text=f"{fan['rpm']} RPM", style="Card.TLabel", font=("Sans", 10, "bold")).pack(side=tk.LEFT, padx=10)

            for pwm in dev["pwms"]:
                row = ttk.Frame(card, style="Card.TFrame")
                row.pack(fill=tk.X, pady=2)
                ttk.Label(row, text=f"PWM ({pwm['name']}):", style="Card.TLabel", width=22).pack(side=tk.LEFT)
                ttk.Label(row, text=f"{pwm['value']} ({pwm['duty_percent']}%)", style="Card.TLabel").pack(side=tk.LEFT, padx=10)

        # 5. Disk Temperatures Card (Thermal Tab convenience)
        if smart_data:
            disk_card = ttk.Frame(self.hwmon_container, style="Card.TFrame", padding=10)
            disk_card.pack(fill=tk.X, expand=True, padx=8, pady=6)

            title = "💾 TEMPERATURAS DOS DISCOS (SMART)"
            ttk.Label(disk_card, text=title, style="SubHeader.TLabel").pack(anchor="w", pady=(0, 6))

            for d in smart_data:
                if not d:
                    continue
                row = ttk.Frame(disk_card, style="Card.TFrame")
                row.pack(fill=tk.X, pady=2)

                model_snip = d.get("model", "")[:12]
                label_str = f"{d.get('name', 'disk')} ({model_snip}) [{d.get('type', '')}]:"
                lbl = ttk.Label(row, text=label_str, style="Card.TLabel", width=26)
                lbl.pack(side=tk.LEFT)

                temp_val = d.get("temp")
                if temp_val is not None:
                    p_style = "Green.Horizontal.TProgressbar"
                    if temp_val >= 55:
                        p_style = "Red.Horizontal.TProgressbar"
                    elif temp_val >= 45:
                        p_style = "Yellow.Horizontal.TProgressbar"

                    pb = ttk.Progressbar(row, length=180, mode="determinate", value=min(temp_val, 100), style=p_style)
                    pb.pack(side=tk.LEFT, padx=10)

                    v_lbl = ttk.Label(row, text=f"{temp_val:5.1f} °C", style="Card.TLabel", width=10)
                    v_lbl.pack(side=tk.LEFT)
                else:
                    err = "🔒 Sem Acesso (use sudo)" if d.get("error_msg") else "-- (Sem sensor SMART)"
                    v_lbl = ttk.Label(row, text=err, style="Card.TLabel", width=25)
                    v_lbl.pack(side=tk.LEFT, padx=10)

        # Update Footer
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.status_lbl.config(text=f"Monitorando {len(hw_sensors)} hwmon, {len(smart_data)} discos, {len(raids)} arrays RAID, {len(lvm.get('vgs', []))} VGs LVM.")
        self.clock_lbl.config(text=f"Última atualização: {now}")

def main():
    if "DISPLAY" not in os.environ and "WAYLAND_DISPLAY" not in os.environ:
        print("Erro: Nenhuma sessão gráfica (DISPLAY ou WAYLAND_DISPLAY) detectada.")
        print("Para ambiente apenas de terminal, use a Opção 1 (Rich) ou Opção 2 (C / ncursesw):")
        print("  python3 dashboard/tui_rich.py")
        print("  ./dashboard/fancontrol-tui")
        sys.exit(1)

    app = FanControlGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
