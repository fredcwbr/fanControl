#!/usr/bin/env python3
"""
Opção 1: Dashboard TUI Moderno em Python com Rich
Monitor de Sensores hwmon, Ventoinhas, SMART, RAID (md) e LVM (VG/LV).
"""

import sys
import time
import os
import argparse
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from monitor import HwmonMonitor, SmartMonitor, RaidMonitor, LvmMonitor

console = Console()

def get_temp_bar(temp: float, max_temp: float = 100.0, width: int = 15) -> Text:
    if temp is None:
        return Text("N/A", style="dim")
    pct = min(max(temp / max_temp, 0.0), 1.0)
    filled = int(round(pct * width))
    bar_chars = "━" * filled + "─" * (width - filled)

    if temp < 50.0:
        color = "green"
    elif temp < 70.0:
        color = "yellow"
    elif temp < 85.0:
        color = "dark_orange"
    else:
        color = "bold red"

    txt = Text()
    txt.append(f"{temp:5.1f}°C ", style=f"bold {color}")
    txt.append(bar_chars, style=color)
    return txt

def get_health_badge(status: str, health_pct: int) -> Text:
    txt = Text()
    if status == "PASSED":
        txt.append("● OK ", style="bold green")
    elif status == "WARNING":
        txt.append("▲ ATENÇÃO ", style="bold yellow")
    elif status == "FAILED":
        txt.append("✖ FALHA ", style="bold red")
    else:
        txt.append("? INDISP ", style="dim")

    if health_pct is not None:
        if health_pct >= 90:
            h_color = "green"
        elif health_pct >= 60:
            h_color = "yellow"
        else:
            h_color = "bold red"
        txt.append(f"({health_pct}%)", style=h_color)
    return txt

def make_header(demo_mode: bool, current_view: str) -> Panel:
    title_text = Text()
    title_text.append("⚡ FanControl ", style="bold cyan")
    title_text.append("• Dashboard de Hardware, SMART, RAID & LVM", style="white")
    if demo_mode:
        title_text.append(" [MODO DEMO]", style="bold magenta")
    else:
        is_root = (os.geteuid() == 0)
        if not is_root:
            title_text.append(" [NÃO-ROOT]", style="yellow")
        else:
            title_text.append(" [ROOT ATIVO]", style="green")

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    right_text = Text(f"Visão: [{current_view}] | [Tab/v] Mudar Visão | [d] Demo | [q] Sair | {now}", style="dim")

    table = Table.grid(expand=True)
    table.add_column(justify="left", ratio=2)
    table.add_column(justify="right", ratio=1)
    table.add_row(title_text, right_text)

    return Panel(table, style="cyan", box=box.ROUNDED)

def make_hwmon_panel(hw_sensors: list) -> Panel:
    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("Sensor / Dispositivo", style="bold white", width=20)
    table.add_column("Canal / Rótulo", style="cyan", width=18)
    table.add_column("Temperatura / Valor", justify="left")
    table.add_column("RPM / PWM", justify="right", style="magenta")

    has_data = False
    for dev in hw_sensors:
        name = dev["name"].upper()
        for t in dev["temps"]:
            has_data = True
            bar = get_temp_bar(t["temp"])
            table.add_row(f"{dev['id']} ({name})", t["label"], bar, "-")

        for fan in dev["fans"]:
            has_data = True
            table.add_row(f"{dev['id']} ({name})", fan["label"], "-", f"{fan['rpm']} RPM")

        for pwm in dev["pwms"]:
            has_data = True
            table.add_row(f"{dev['id']} ({name})", pwm["name"], "-", f"PWM {pwm['value']} ({pwm['duty_percent']}%)")

    if not has_data:
        table.add_row("Nenhum sensor hwmon encontrado", "-", "-", "-")

    return Panel(table, title="[bold green]🌡️ Sensores Térmicos & Ventoinhas (hwmon)[/]", box=box.ROUNDED)

def make_smart_panel(disks_smart: list) -> Panel:
    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("Disco", style="bold white", width=9)
    table.add_column("Modelo / Tipo", style="white", width=20)
    table.add_column("Saúde / Status", justify="center", width=16)
    table.add_column("Temp", justify="center", width=8)
    table.add_column("Realocados (ID5)", justify="right", width=16)
    table.add_column("Pendentes", justify="right", width=11)
    table.add_column("Não Corrigíveis", justify="right", width=15)
    table.add_column("Erros CRC", justify="right", width=11)
    table.add_column("Erros ATA", justify="right", width=11)

    has_perm_error = False

    for d in disks_smart:
        if not d:
            continue
        dev_label = f"{d['name']} ({d['size_gb']}G)"
        model_type = f"{d['model'][:14]} [{d['type']}]"

        if d.get("error_msg"):
            has_perm_error = True
            badge = Text("🔒 Sem Acesso", style="yellow")
            temp_str = "-"
            realloc = "-"
            pending = "-"
            uncorr = "-"
            crc = "-"
            ata_err = "-"
        else:
            badge = get_health_badge(d["status"], d["health_percent"])
            temp = d["temp"]
            if temp is not None:
                t_color = "green" if temp < 45 else ("yellow" if temp < 55 else "bold red")
                temp_str = Text(f"{temp}°C", style=t_color)
            else:
                temp_str = Text("N/A", style="dim")

            def fmt_err(val: int) -> Text:
                if val is None or val == 0:
                    return Text("0", style="green")
                return Text(str(val), style="bold red")

            realloc = fmt_err(d["reallocated_sectors"])
            pending = fmt_err(d["pending_sectors"])
            uncorr = fmt_err(d["uncorrectable_sectors"])
            crc = fmt_err(d["crc_errors"])
            ata_err = fmt_err(d["ata_errors"])

        table.add_row(
            dev_label,
            model_type,
            badge,
            temp_str,
            realloc,
            pending,
            uncorr,
            crc,
            ata_err
        )

    subtitle = "[dim]Valores > 0 em vermelho indicam potenciais falhas no disco[/]"
    if has_perm_error:
        subtitle += " | [yellow]Execute com 'sudo' para ioctl SMART[/]"

    return Panel(table, title="[bold cyan]💾 Métricas SMART de Armazenamento[/]", subtitle=subtitle, box=box.ROUNDED)

def make_raid_panel(raids: list) -> Panel:
    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("Array", style="bold white", width=12)
    table.add_column("Nível", style="cyan", width=8)
    table.add_column("Tamanho", justify="center", width=10)
    table.add_column("Saúde / Máscara", justify="center", width=18)
    table.add_column("Estado Array", justify="center", width=14)
    table.add_column("Discos Ativos", justify="center", width=14)
    table.add_column("Componentes / Membros & Erros", justify="left")

    if not raids:
        table.add_row("Nenhum array RAID (md) detectado", "-", "-", "-", "-", "-", "-")
    else:
        for r in raids:
            # Badge
            badge = Text()
            if r["degraded"]:
                badge.append(f"▲ DEGRADADO {r['health_mask']}", style="bold red")
            else:
                badge.append(f"● OK {r['health_mask']}", style="bold green")

            state_style = "bold red" if r["degraded"] else "green"
            state_text = Text(r["state"].upper(), style=state_style)

            disks_str = f"{r['active_disks']}/{r['total_disks']}"

            # Members formatting
            members_txt = Text()
            for idx, m in enumerate(r["members"]):
                if idx > 0:
                    members_txt.append(" | ")
                m_color = "green" if "in_sync" in m["state"] else "bold red"
                err_str = f" [err:{m['errors']}]" if m['errors'] > 0 else ""
                members_txt.append(f"{m['name']}", style=f"bold {m_color}")
                members_txt.append(f"({m['state']}{err_str})", style=m_color)

            if r["sync_progress"]:
                members_txt.append(f"\n⚡ {r['sync_progress']}", style="yellow")

            table.add_row(
                r["name"],
                r["level"],
                f"{r['size_gb']} GB",
                badge,
                state_text,
                disks_str,
                members_txt
            )

    return Panel(table, title="[bold magenta]🛡️ Linux Software RAID (md / mdstat)[/]", box=box.ROUNDED)

def make_lvm_panel(lvm_info: dict) -> Panel:
    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("Volume Group (VG)", style="bold cyan", width=18)
    table.add_column("Espaço Alocado", justify="center", width=16)
    table.add_column("Qtd LVs", justify="center", width=10)
    table.add_column("Volumes Lógicos (LV) Mapeados", justify="left")

    vgs = lvm_info.get("vgs", [])
    if not vgs:
        table.add_row("Nenhum Volume Group LVM detectado", "-", "-", "-")
    else:
        for vg in vgs:
            lvs_summary = Text()
            for idx, lv in enumerate(vg["lvs"][:6]):
                if idx > 0:
                    lvs_summary.append(", ")
                lvs_summary.append(f"{lv['lv']} ({lv['size_gb']}G)", style="white")
            if len(vg["lvs"]) > 6:
                lvs_summary.append(f" + {len(vg['lvs']) - 6} outros...", style="dim")

            table.add_row(
                vg["name"],
                f"{vg['allocated_gb']} GB",
                str(vg["total_lvs"]),
                lvs_summary
            )

    return Panel(table, title="[bold yellow]📦 LVM (Logical Volume Manager - VGs & LVs)[/]", box=box.ROUNDED)

def main():
    parser = argparse.ArgumentParser(description="FanControl TUI Dashboard (Hardware, SMART, RAID, LVM)")
    parser.add_argument("--interval", "-i", type=float, default=1.5, help="Intervalo de atualização em segundos (padrão: 1.5)")
    parser.add_argument("--demo", "-d", action="store_true", help="Modo demonstração/simulação para SMART")
    args = parser.parse_args()

    hw_mon = HwmonMonitor()
    smart_mon = SmartMonitor()
    raid_mon = RaidMonitor()
    lvm_mon = LvmMonitor()
    disks = smart_mon.list_disks()

    demo_mode = args.demo

    # Views: "TUDO", "STORAGE" (SMART + RAID + LVM), "SENSORES" (hwmon + SMART)
    views = ["COMPLETO", "STORAGE (RAID & LVM)", "SENSORES (Hwmon)"]
    view_idx = 0

    import select

    console.clear()

    try:
        with Live(console=console, screen=True, auto_refresh=False) as live:
            while True:
                # 1. Fetch data
                hw_sensors = hw_mon.get_sensors()
                disks_data = [smart_mon.get_disk_smart(d, demo_mode=demo_mode) for d in disks]
                raids_data = raid_mon.get_arrays()
                lvm_data = lvm_mon.get_lvm_info()

                cur_view = views[view_idx]

                # 2. Build layout based on current view
                layout = Layout()
                layout.split_column(
                    Layout(name="header", size=3),
                    Layout(name="body", ratio=1)
                )
                layout["header"].update(make_header(demo_mode, cur_view))

                if cur_view == "COMPLETO":
                    layout["body"].split_column(
                        Layout(name="top", ratio=1),
                        Layout(name="bottom", ratio=1)
                    )
                    layout["body"]["top"].split_row(
                        Layout(make_hwmon_panel(hw_sensors), ratio=1),
                        Layout(make_smart_panel(disks_data), ratio=2)
                    )
                    layout["body"]["bottom"].split_row(
                        Layout(make_raid_panel(raids_data), ratio=1),
                        Layout(make_lvm_panel(lvm_data), ratio=1)
                    )
                elif cur_view == "STORAGE (RAID & LVM)":
                    layout["body"].split_column(
                        Layout(make_smart_panel(disks_data), ratio=2),
                        Layout(make_raid_panel(raids_data), ratio=1),
                        Layout(make_lvm_panel(lvm_data), ratio=1)
                    )
                else: # SENSORES (Hwmon)
                    layout["body"].split_column(
                        Layout(make_hwmon_panel(hw_sensors), ratio=1),
                        Layout(make_smart_panel(disks_data), ratio=1)
                    )

                live.update(layout, refresh=True)

                # Check keyboard
                if select.select([sys.stdin], [], [], args.interval)[0]:
                    char = sys.stdin.read(1)
                    if char.lower() == 'q':
                        break
                    elif char.lower() == 'd':
                        demo_mode = not demo_mode
                    elif char.lower() in ('v', '\t', ' '):
                        view_idx = (view_idx + 1) % len(views)

    except KeyboardInterrupt:
        pass
    finally:
        console.clear()
        console.print("[cyan]FanControl Dashboard finalizado.[/cyan]")

if __name__ == "__main__":
    main()
