import psutil
import GPUtil
import winreg
import os
import time
import comtypes
from pycaw.pycaw import AudioUtilities

# Global variables for network speed calculation
last_net_io = psutil.net_io_counters()
last_net_time = time.time()

def get_network_speed():
    global last_net_io, last_net_time
    try:
        io = psutil.net_io_counters()
        now = time.time()
        
        # Prevent division by zero
        delta_time = now - last_net_time
        if delta_time == 0: delta_time = 1
            
        upload = (io.bytes_sent - last_net_io.bytes_sent) / delta_time
        download = (io.bytes_recv - last_net_io.bytes_recv) / delta_time
        
        last_net_io = io
        last_net_time = now
        
        # Return in MB/s
        return {
            "up": round(upload / 1024 / 1024, 2),
            "down": round(download / 1024 / 1024, 2)
        }
    except:
        return {"up": 0, "down": 0}

def get_top_processes():
    try:
        processes = []
        for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Filter out system idles
        processes = [p for p in processes if p['name'] and p['name'].lower() != 'system idle process']
        
        top_cpu = sorted(processes, key=lambda p: p['cpu_percent'] or 0, reverse=True)[:5]
        top_mem = sorted(processes, key=lambda p: p['memory_percent'] or 0, reverse=True)[:5]
        
        return {
            "cpu_apps": [{"name": p['name'], "val": round(p['cpu_percent'] or 0, 1)} for p in top_cpu],
            "mem_apps": [{"name": p['name'], "val": round(p['memory_percent'] or 0, 1)} for p in top_mem]
        }
    except Exception as e:
        return {"cpu_apps": [], "mem_apps": []}

def get_basic_stats():
    # CPU, Mem, Battery
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    batt = psutil.sensors_battery()
    battery_pct = batt.percent if batt else 100
    
    # GPU
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            gpu_load = gpu.load * 100
            gpu_temp = gpu.temperature
        else:
            gpu_load = 0
            gpu_temp = 0
    except:
        gpu_load = 0
        gpu_temp = 0
        
    return {
        "cpu": cpu,
        "ram": mem.percent,
        "battery": battery_pct,
        "gpu_load": gpu_load,
        "gpu_temp": gpu_temp,
        "fan_speed": 2250, # Simulated due to Windows WMI lock
        "fan_temp": 42     # Simulated
    }

def get_audio_apps():
    try:
        comtypes.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        active_apps = []
        for session in sessions:
            if session.Process:
                app_name = session.Process.name()
                if app_name not in ["System Sounds", "audiodg.exe"] and app_name not in active_apps:
                    active_apps.append(app_name)
        comtypes.CoUninitialize()
        return active_apps
    except:
        return []

def get_camera_mic_usage(device_type="webcam"):
    try:
        base_key = f"Software\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\{device_type}"
        active_apps = []
        
        # Check Packaged Apps
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_key) as key:
            num_subkeys = winreg.QueryInfoKey(key)[0]
            for i in range(num_subkeys):
                app_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, app_name) as app_key:
                    try:
                        start_time = winreg.QueryValueEx(app_key, "LastUsedTimeStart")[0]
                        stop_time = winreg.QueryValueEx(app_key, "LastUsedTimeStop")[0]
                        if start_time > stop_time:
                            active_apps.append(app_name.split("_")[0])
                    except: pass
                    
        # Check non-packaged apps (Desktop apps)
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"{base_key}\\NonPackaged") as key:
                num_subkeys = winreg.QueryInfoKey(key)[0]
                for i in range(num_subkeys):
                    app_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, app_name) as app_key:
                        try:
                            start_time = winreg.QueryValueEx(app_key, "LastUsedTimeStart")[0]
                            stop_time = winreg.QueryValueEx(app_key, "LastUsedTimeStop")[0]
                            if start_time > stop_time:
                                active_apps.append(app_name.split("#")[-1])
                        except: pass
        except: pass
        
        return active_apps
    except Exception as e:
        return []

def get_all_stats():
    stats = get_basic_stats()
    stats["audio_apps"] = get_audio_apps()
    stats["camera_apps"] = get_camera_mic_usage("webcam")
    stats["mic_apps"] = get_camera_mic_usage("microphone")
    stats["network"] = get_network_speed()
    stats["top_procs"] = get_top_processes()
    return stats
