#!/usr/bin/env bash
# Script de inicialização dos Dashboards do FanControl

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

show_menu() {
    echo "=========================================================="
    echo "           ⚡ FanControl Dashboard Selector               "
    echo "=========================================================="
    echo " Escolha qual versão do Dashboard deseja executar:        "
    echo ""
    echo " 1) TUI Python (Rich)        [Visual Moderno no Terminal] "
    echo " 2) TUI Nativo em C (ncurses) [Binário Leve Compilado]    "
    echo " 3) GUI Gráfica (Tkinter)    [Janela Desktop Completa]    "
    echo " q) Sair                                                  "
    echo "=========================================================="
    read -rp " Digite sua opção [1-3]: " opt
    case "$opt" in
        1) run_tui_rich ;;
        2) run_tui_c ;;
        3) run_gui ;;
        q|Q) exit 0 ;;
        *) echo "Opção inválida!"; exit 1 ;;
    esac
}

run_tui_rich() {
    echo "Iniciando TUI Python com Rich..."
    python3 "$DIR/tui_rich.py" "$@"
}

run_tui_c() {
    if [ ! -f "$DIR/fancontrol-tui" ]; then
        echo "Compilando TUI C..."
        make -C "$DIR/tui_c"
    fi
    echo "Iniciando TUI C ncursesw..."
    "$DIR/fancontrol-tui" "$@"
}

run_gui() {
    echo "Iniciando Dashboard Gráfico..."
    python3 "$DIR/gui_app.py" "$@"
}

case "$1" in
    1|--rich|--tui-rich)
        shift
        run_tui_rich "$@"
        ;;
    2|--c|--tui-c)
        shift
        run_tui_c "$@"
        ;;
    3|--gui)
        shift
        run_gui "$@"
        ;;
    -h|--help)
        echo "Uso: ./run.sh [1|2|3|--rich|--c|--gui] [--demo]"
        echo "  1, --rich : TUI Python Moderno (Rich)"
        echo "  2, --c    : TUI C Nativo (ncursesw)"
        echo "  3, --gui  : GUI Gráfica Desktop"
        echo "  --demo    : Modo simulação para testes sem root/smartctl"
        exit 0
        ;;
    *)
        show_menu
        ;;
esac
