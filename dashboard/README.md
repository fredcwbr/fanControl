# FanControl - Dashboards de Monitoramento

Este diretório contém 3 implementações completas de monitoramento de hardware, ventoinhas, saúde SMART dos discos, **Linux Software RAID (`md`)** e **LVM (Volume Groups e Logical Volumes)** para o ecossistema **fanControl**.

---

## 🚀 As 3 Opções Disponíveis

### 1. TUI Moderno em Python (`Rich`)
- **Arquivo**: `tui_rich.py`
- **Características**:
  - Interface moderna no terminal inspirada em `btop`/`htop`.
  - Painéis com cores dinâmicas, barras visuais de temperatura e tabelas autoajustáveis.
  - Alternância de visões com as teclas **`v`**, **`Tab`** ou **`Espaço`**:
    - **COMPLETO**: Visão 4x4 (Sensores + SMART + RAID + LVM)
    - **STORAGE**: Foco em Armazenamento (SMART dos discos, Arrays RAID e LVM VGs/LVs)
    - **SENSORES**: Foco em temperaturas e ventoinhas
  - Atualização em tempo real não-bloqueante.
- **Execução**:
  ```bash
  python3 dashboard/tui_rich.py
  # ou com permissão root para SMART via ioctl:
  sudo python3 dashboard/tui_rich.py
  # ou em modo demonstração:
  python3 dashboard/tui_rich.py --demo
  ```

---

### 2. TUI Nativo em C (`ncursesw`)
- **Diretório**: `tui_c/` (Gera o binário compilado `fancontrol-tui`)
- **Características**:
  - Binário ultraleve em C puro sem dependências pesadas externas (usa apenas `libc` e `ncursesw`).
  - Totalmente integrado ao fluxo de compilação do projeto (`Makefile`).
  - Gráficos de barras em ASCII e cores temáticas.
  - Alerta visual em vermelho destacado para arrays RAID degradados (ex: `md101 [_UU]`).
  - Atalhos: `1` (Completo), `2` (Storage RAID/LVM), `3` (Sensores), `v/Tab` (Alternar visão), `d` (Demo), `q` (Sair).
- **Compilação e Execução**:
  ```bash
  make dashboard-c
  ./dashboard/fancontrol-tui
  # ou com permissão root:
  sudo ./dashboard/fancontrol-tui
  # ou em modo demonstração:
  ./dashboard/fancontrol-tui -d
  ```

---

### 3. GUI Gráfica Desktop (`Tkinter`)
- **Arquivo**: `gui_app.py`
- **Características**:
  - Janela gráfica independente em Dark Mode para ambientes com Desktop/X11/Wayland.
  - Abas dedicadas:
    - **💾 Discos & SMART**: Tabela interativa com cores de alerta e guia explicativo de defeitos.
    - **🛡️ RAID (mdstat)**: Status de saúde de cada array, máscara (`[UU]`, `[_UU]`), contagem de erros de I/O em cada partição membro (`dev-sda1`, `dev-sdf1`, etc.) e status de resync.
    - **📦 LVM (VGs & LVs)**: Relação de Volume Groups, contagem de LVs, capacidade alocada e mapeamento dos dispositivos `/dev/mapper/`.
    - **🌡️ Sensores Térmicos & Fans**: Medidores visuais com barras de progresso para CPU, GPU e ventoinhas (RPM e PWM).
  - Controle de atualização automática e botão de refresh manual.
- **Execução**:
  ```bash
  python3 dashboard/gui_app.py
  ```

---

## 🛠️ Launcher Unificado (`run.sh`)

```bash
# Menu interativo
./dashboard/run.sh

# Atalhos diretos
./dashboard/run.sh 1       # Abre o TUI Rich
./dashboard/run.sh 2       # Abre o TUI C
./dashboard/run.sh 3       # Abre a GUI Desktop
```

---

## 📊 Métricas Monitoradas

### 1. Linux Software RAID (`/proc/mdstat` e `/sys/block/md*`)
- **Arrays Ativos**: Nome do array (`md127`, `md101`, etc.) e nível (`RAID1`, `RAID5`, `RAID6`, `RAID10`).
- **Estado de Degradação**:
  - **`● OK [UU]`**: Todos os componentes ativos e sincronizados.
  - **`▲ DEGRADADO [_UU]`**: Um ou mais discos falharam ou estão ausentes.
- **Componentes Membros**: Lista de membros (`sda1`, `sde1`, `sdf1`), estado (`in_sync`, `faulty`, `spare`), slot do RAID e contagem de erros de bloco do membro (`errors`).
- **Sincronização & Rebuild**: Status da ação de sync (`idle`, `resync`, `recovery`, `check`) e progresso/velocidade/tempo estimado se estiver reconstruindo.

### 2. LVM - Volume Groups (VG) & Logical Volumes (LV)
- **Volume Groups**: Identificação dos grupos (ex: `vgSDD`, `VGSDA3`, `VGSDF3`).
- **Logical Volumes**: Listagem dos volumes lógicos mapeados (`dm-*` e `/dev/mapper/*`).
- **Capacidade**: Espaço total alocado por Volume Group e tamanho de cada LV.

### 3. SMART dos Discos (via `smartctl`)
- **Temperatura**: Medição térmica direta dos HDDs, SSDs e NVMe.
- **Status Geral & Saúde**: `PASSED`, `WARNING` ou `FAILED`, percentual de vida restante.
- **Contagem de Erros**:
  - **Setores Realocados (ID 5)**
  - **Setores Pendentes (ID 197)**
  - **Setores Não Corrigíveis (ID 198)**
  - **Erros CRC (ID 199)**
  - **Log de Erros ATA**

### 4. Sensores Térmicos e Ventoinhas (via `hwmon` e `sysfs`)
- **CPU**: Monitoramento por núcleo (`Core 0..N`) e encapsulamento (`Package id 0`).
- **GPU**: Temperatura do chip gráfico e frequências de clock.
- **ACPI / Placa-mãe**: Zonas térmicas do sistema.
- **Ventoinhas & PWM**: Rotação em RPM e ciclo de trabalho PWM.
