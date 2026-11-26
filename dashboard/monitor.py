#!/usr/bin/env python3
"""
Hardware & SMART Monitor for fanControl
Reads hwmon temperatures, fan speeds, PWM controls and SMART disk metrics.
"""

import os
import glob
import json
import shutil
import subprocess
from typing import Dict, List, Any, Optional

class HwmonMonitor:
    def __init__(self, hwmon_root: str = "/sys/class/hwmon"):
        self.hwmon_root = hwmon_root

    def get_sensors(self) -> List[Dict[str, Any]]:
        sensors = []
        if not os.path.exists(self.hwmon_root):
            return sensors

        for hwmon_dir in sorted(glob.glob(os.path.join(self.hwmon_root, "hwmon*"))):
            name_file = os.path.join(hwmon_dir, "name")
            name = "unknown"
            if os.path.exists(name_file):
                try:
                    with open(name_file, "r") as f:
                        name = f.read().strip()
                except Exception:
                    pass

            hw_info: Dict[str, Any] = {
                "id": os.path.basename(hwmon_dir),
                "name": name,
                "temps": [],
                "fans": [],
                "pwms": []
            }

            # Scan temperature inputs
            for temp_input in sorted(glob.glob(os.path.join(hwmon_dir, "temp*_input"))):
                base = temp_input[:-6]  # strip '_input'
                label_file = f"{base}_label"
                label = os.path.basename(base)
                if os.path.exists(label_file):
                    try:
                        with open(label_file, "r") as f:
                            label = f.read().strip()
                    except Exception:
                        pass

            crit_file = f"{base}_crit"
            crit = None
            if os.path.exists(crit_file):
                try:
                    with open(crit_file, "r") as f:
                        crit = float(f.read().strip()) / 1000.0
                except Exception:
                    pass

                try:
                    with open(temp_input, "r") as f:
                        temp_c = float(f.read().strip()) / 1000.0
                        hw_info["temps"].append({
                            "label": label,
                            "temp": temp_c,
                            "crit": crit,
                            "path": temp_input
                        })
                except Exception:
                    pass

            # Scan fans (RPM)
            for fan_input in sorted(glob.glob(os.path.join(hwmon_dir, "fan*_input"))):
                base = fan_input[:-6]
                label_file = f"{base}_label"
                label = os.path.basename(base)
                if os.path.exists(label_file):
                    try:
                        with open(label_file, "r") as f:
                            label = f.read().strip()
                    except Exception:
                        pass

                try:
                    with open(fan_input, "r") as f:
                        rpm = int(f.read().strip())
                        hw_info["fans"].append({
                            "label": label,
                            "rpm": rpm,
                            "path": fan_input
                        })
                except Exception:
                    pass

            # Scan PWM (0-255)
            for pwm_file in sorted(glob.glob(os.path.join(hwmon_dir, "pwm[0-9]*"))):
                if pwm_file.endswith("_enable") or pwm_file.endswith("_mode"):
                    continue
                try:
                    with open(pwm_file, "r") as f:
                        pwm_val = int(f.read().strip())
                        duty = round((pwm_val / 255.0) * 100, 1)
                        hw_info["pwms"].append({
                            "name": os.path.basename(pwm_file),
                            "value": pwm_val,
                            "duty_percent": duty,
                            "path": pwm_file
                        })
                except Exception:
                    pass

            if hw_info["temps"] or hw_info["fans"] or hw_info["pwms"]:
                sensors.append(hw_info)

        return sensors


class SmartMonitor:
    def __init__(self):
        for candidate in [shutil.which("smartctl"), "/usr/sbin/smartctl", "/sbin/smartctl", "/usr/local/sbin/smartctl"]:
            if candidate and os.path.exists(candidate):
                self.smartctl_bin = candidate
                break
        else:
            self.smartctl_bin = shutil.which("smartctl") or "/usr/sbin/smartctl"

    def list_disks(self) -> List[Dict[str, Any]]:
        disks = []
        pattern = "/sys/block/*"
        for block_path in sorted(glob.glob(pattern)):
            devname = os.path.basename(block_path)
            # Filter standard physical drives: sd*, nvme*n*, vd*
            if not (devname.startswith("sd") or devname.startswith("nvme") or devname.startswith("vd")):
                continue

            size_file = os.path.join(block_path, "size")
            if not os.path.exists(size_file):
                continue

            try:
                with open(size_file, "r") as f:
                    size_blocks = int(f.read().strip())
                if size_blocks <= 0:
                    continue
                size_gb = round(size_blocks * 512 / (1024 ** 3), 1)
            except Exception:
                continue

            model = "Desconhecido"
            model_file = os.path.join(block_path, "device/model")
            if os.path.exists(model_file):
                try:
                    with open(model_file, "r") as f:
                        model = f.read().strip()
                except Exception:
                    pass
            elif devname.startswith("nvme"):
                nvme_model = os.path.join(block_path, "device/device/model")
                if os.path.exists(nvme_model):
                    try:
                        with open(nvme_model, "r") as f:
                            model = f.read().strip()
                    except Exception:
                        pass

            rotational = True
            rot_file = os.path.join(block_path, "queue/rotational")
            if os.path.exists(rot_file):
                try:
                    with open(rot_file, "r") as f:
                        rotational = (f.read().strip() == "1")
                except Exception:
                    pass

            disk_type = "HDD" if rotational else "SSD"
            if devname.startswith("nvme"):
                disk_type = "NVMe"

            disks.append({
                "dev": f"/dev/{devname}",
                "name": devname,
                "model": model,
                "size_gb": size_gb,
                "type": disk_type
            })

        return disks

    def _run_smartctl_json(self, dev: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(self.smartctl_bin):
            return None

        # Attempts with and without sudo / sat / nvme flags
        commands_to_try = [
            [self.smartctl_bin, "-j", "-a", dev],
            [self.smartctl_bin, "-j", "-a", "-d", "sat", dev],
            ["sudo", "-n", self.smartctl_bin, "-j", "-a", dev],
            ["sudo", "-n", self.smartctl_bin, "-j", "-a", "-d", "sat", dev]
        ]

        for cmd in commands_to_try:
            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                if proc.stdout and proc.stdout.strip().startswith("{"):
                    data = json.loads(proc.stdout)
                    # Verify if it returned actual disk info (not just exit error)
                    if "smart_status" in data or "ata_smart_attributes" in data or "nvme_smart_health_information_log" in data:
                        return data
            except Exception:
                pass
        return None

    def get_disk_smart(self, disk_info: Dict[str, Any], demo_mode: bool = False) -> Dict[str, Any]:
        dev = disk_info["dev"]
        result: Dict[str, Any] = {
            "dev": dev,
            "name": disk_info["name"],
            "model": disk_info["model"],
            "size_gb": disk_info["size_gb"],
            "type": disk_info["type"],
            "temp": None,
            "status": "UNKNOWN",
            "health_percent": None,
            "reallocated_sectors": 0,
            "pending_sectors": 0,
            "uncorrectable_sectors": 0,
            "crc_errors": 0,
            "read_errors": 0,
            "ata_errors": 0,
            "power_on_hours": None,
            "error_msg": None
        }

        if demo_mode:
            # Deterministic simulation based on disk name
            seed = sum(ord(c) for c in disk_info["name"])
            result["temp"] = 32 + (seed % 14)
            result["status"] = "PASSED"
            result["health_percent"] = 100 - (seed % 7)
            result["power_on_hours"] = 1200 + (seed * 15)
            result["reallocated_sectors"] = 0 if (seed % 3 != 0) else (seed % 4)
            result["pending_sectors"] = 0
            result["uncorrectable_sectors"] = 0
            result["crc_errors"] = 0
            result["ata_errors"] = 0
            return result

        data = self._run_smartctl_json(dev)
        if not data:
            result["error_msg"] = "Sem permissão (requer sudo/root)"
            return result

        # Overall Status
        smart_status = data.get("smart_status", {})
        if smart_status:
            passed = smart_status.get("passed")
            result["status"] = "PASSED" if passed else "FAILED"

        # Direct Temperature
        temp_data = data.get("temperature", {})
        if temp_data and "current" in temp_data:
            result["temp"] = temp_data["current"]

        # Power on time
        pot = data.get("power_on_time", {})
        if pot and "hours" in pot:
            result["power_on_hours"] = pot["hours"]

        # NVMe Health & Errors
        nvme_log = data.get("nvme_smart_health_information_log", {})
        if nvme_log:
            if result["temp"] is None and "temperature" in nvme_log:
                result["temp"] = nvme_log["temperature"]
            if "percentage_used" in nvme_log:
                used = nvme_log["percentage_used"]
                result["health_percent"] = max(0, 100 - used)
            if "media_errors" in nvme_log:
                result["uncorrectable_sectors"] = nvme_log["media_errors"]
            if "num_err_log_entries" in nvme_log:
                result["ata_errors"] = nvme_log["num_err_log_entries"]
            if "critical_warning" in nvme_log and nvme_log["critical_warning"] > 0:
                result["status"] = "WARNING"

        # ATA Attributes (SATA HDD / SSD)
        ata_table = data.get("ata_smart_attributes", {}).get("table", [])
        for attr in ata_table:
            attr_id = attr.get("id")
            name = attr.get("name", "")
            raw_val = attr.get("raw", {}).get("value", 0)
            norm_val = attr.get("value")

            # Temperature
            if attr_id in (194, 190) and result["temp"] is None:
                result["temp"] = raw_val

            # Reallocated Sectors (ID 5)
            elif attr_id == 5:
                result["reallocated_sectors"] = raw_val

            # Current Pending Sector (ID 197)
            elif attr_id == 197:
                result["pending_sectors"] = raw_val

            # Offline Uncorrectable (ID 198)
            elif attr_id == 198:
                result["uncorrectable_sectors"] = raw_val

            # UltraDMA CRC Error Count (ID 199)
            elif attr_id == 199:
                result["crc_errors"] = raw_val

            # Raw Read Error Rate (ID 1)
            elif attr_id == 1:
                result["read_errors"] = raw_val

            # SSD Wear / Health (ID 231 SSD_Life_Left or 177 / 202)
            elif attr_id in (231, 177, 202, 169) and result["health_percent"] is None:
                if norm_val is not None and 0 <= norm_val <= 100:
                    result["health_percent"] = norm_val

        # ATA Error Log count
        error_log = data.get("ata_smart_error_log", {}).get("summary", {})
        if error_log and "count" in error_log:
            result["ata_errors"] = error_log["count"]

        # If health percentage is still unset and no reallocated sectors, default to 100% or based on reallocated
        if result["health_percent"] is None:
            if result["reallocated_sectors"] > 0:
                result["health_percent"] = max(10, 100 - (result["reallocated_sectors"] * 5))
            elif result["status"] == "PASSED":
                result["health_percent"] = 100

        return result


class RaidMonitor:
    def __init__(self, mdstat_path: str = "/proc/mdstat", sys_block: str = "/sys/block"):
        self.mdstat_path = mdstat_path
        self.sys_block = sys_block

    def get_arrays(self) -> List[Dict[str, Any]]:
        arrays = []
        if not os.path.exists(self.sys_block):
            return arrays

        # Scan /sys/block/md*
        for md_path in sorted(glob.glob(os.path.join(self.sys_block, "md*"))):
            md_name = os.path.basename(md_path)
            md_dir = os.path.join(md_path, "md")
            if not os.path.exists(md_dir):
                continue

            def read_file_or(p: str, default: str = "") -> str:
                try:
                    if os.path.exists(p):
                        with open(p, "r") as f:
                            return f.read().strip()
                except Exception:
                    pass
                return default

            level = read_file_or(os.path.join(md_dir, "level"), "unknown").upper()
            state = read_file_or(os.path.join(md_dir, "array_state"), "unknown")
            degraded_str = read_file_or(os.path.join(md_dir, "degraded"), "0")
            is_degraded = (degraded_str == "1")

            raid_disks_str = read_file_or(os.path.join(md_dir, "raid_disks"), "0")
            try:
                raid_disks = int(raid_disks_str)
            except ValueError:
                raid_disks = 0

            sync_action = read_file_or(os.path.join(md_dir, "sync_action"), "idle")

            # Size from /sys/block/mdX/size (512-byte blocks)
            size_blocks_str = read_file_or(os.path.join(md_path, "size"), "0")
            try:
                size_gb = round(int(size_blocks_str) * 512 / (1024 ** 3), 1)
            except ValueError:
                size_gb = 0.0

            # Scan member disks in /sys/block/mdX/md/dev-*
            members = []
            for dev_path in sorted(glob.glob(os.path.join(md_dir, "dev-*"))):
                dev_base = os.path.basename(dev_path)
                member_name = dev_base[4:] if dev_base.startswith("dev-") else dev_base
                m_state = read_file_or(os.path.join(dev_path, "state"), "unknown")
                m_slot = read_file_or(os.path.join(dev_path, "slot"), "-1")
                m_errors = read_file_or(os.path.join(dev_path, "errors"), "0")

                members.append({
                    "name": member_name,
                    "state": m_state,
                    "slot": m_slot,
                    "errors": int(m_errors) if m_errors.isdigit() else 0
                })

            # Check /proc/mdstat for [UU] mask and resync progress
            health_mask = ""
            sync_progress = ""
            if os.path.exists(self.mdstat_path):
                try:
                    with open(self.mdstat_path, "r") as f:
                        lines = f.readlines()
                    for idx, line in enumerate(lines):
                        if line.startswith(md_name + " ") or line.startswith(md_name + ":"):
                            # Look at subsequent lines
                            for sub_line in lines[idx:idx + 4]:
                                if "[" in sub_line and "]" in sub_line:
                                    parts = sub_line.split()
                                    for p in parts:
                                        if p.startswith("[") and p.endswith("]") and ("U" in p or "_" in p):
                                            health_mask = p
                                if "resync" in sub_line or "recovery" in sub_line or "check" in sub_line:
                                    sync_progress = sub_line.strip()
                except Exception:
                    pass

            arrays.append({
                "name": md_name,
                "dev": f"/dev/{md_name}",
                "level": level,
                "state": state,
                "degraded": is_degraded,
                "total_disks": raid_disks,
                "active_disks": len([m for m in members if "in_sync" in m["state"]]),
                "size_gb": size_gb,
                "sync_action": sync_action,
                "sync_progress": sync_progress,
                "health_mask": health_mask,
                "members": members
            })

        return arrays


class LvmMonitor:
    def __init__(self, sys_block: str = "/sys/block"):
        self.sys_block = sys_block

    def get_lvm_info(self) -> Dict[str, Any]:
        """
        Parses device-mapper sysfs nodes to extract VGs and LVs reliably
        even without root access to /dev/mapper/control.
        """
        vgs: Dict[str, Dict[str, Any]] = {}
        lvs: List[Dict[str, Any]] = []

        for dm_path in sorted(glob.glob(os.path.join(self.sys_block, "dm-*"))):
            dm_name = os.path.basename(dm_path)
            dm_dir = os.path.join(dm_path, "dm")
            if not os.path.exists(dm_dir):
                continue

            def read_f(p: str) -> str:
                try:
                    if os.path.exists(p):
                        with open(p, "r") as f:
                            return f.read().strip()
                except Exception:
                    pass
                return ""

            uuid = read_f(os.path.join(dm_dir, "uuid"))
            raw_name = read_f(os.path.join(dm_dir, "name"))
            size_str = read_f(os.path.join(dm_path, "size"))

            try:
                size_gb = round(int(size_str) * 512 / (1024 ** 3), 1)
            except ValueError:
                size_gb = 0.0

            # Only process LVM targets
            if not (uuid.startswith("LVM-") or ("-" in raw_name and not raw_name.startswith("mpath"))):
                continue

            # Devmapper escapes '-' as '--'. Split by single '-'
            # e.g. "vgSDD-W8" -> vg="vgSDD", lv="W8"
            # e.g. "VGSDA3-Win8SWP" -> vg="VGSDA3", lv="Win8SWP"
            parts = raw_name.replace("--", "\x00").split("-")
            if len(parts) >= 2:
                vg_name = parts[0].replace("\x00", "-")
                lv_name = "-".join(parts[1:]).replace("\x00", "-")
            else:
                vg_name = "Desconhecido"
                lv_name = raw_name

            lv_entry = {
                "vg": vg_name,
                "lv": lv_name,
                "dm": dm_name,
                "path": f"/dev/mapper/{raw_name}",
                "size_gb": size_gb,
                "uuid": uuid
            }
            lvs.append(lv_entry)

            if vg_name not in vgs:
                vgs[vg_name] = {
                    "name": vg_name,
                    "total_lvs": 0,
                    "allocated_gb": 0.0,
                    "lvs": []
                }
            vgs[vg_name]["total_lvs"] += 1
            vgs[vg_name]["allocated_gb"] = round(vgs[vg_name]["allocated_gb"] + size_gb, 1)
            vgs[vg_name]["lvs"].append(lv_entry)

        return {
            "vgs": list(vgs.values()),
            "lvs": lvs
        }
