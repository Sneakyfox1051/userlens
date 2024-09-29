import subprocess
import platform

def get_wifi_ssid():
    ssid = "Unknown"
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            for line in result.decode('utf-8').split('\n'):
                if "SSID" in line:
                    ssid = line.split(":")[1].strip()
                    break
        elif platform.system() == "Linux":
            result = subprocess.check_output(["iwgetid", "-r"])
            ssid = result.decode('utf-8').strip()
        elif platform.system() == "Darwin":  # MacOS
            result = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"])
            for line in result.decode('utf-8').split('\n'):
                if "SSID" in line:
                    ssid = line.split(":")[1].strip()
                    break
    except Exception as e:
        print(f"Error retrieving Wi-Fi SSID: {e}")
    return ssid

def get_network_latency():
    # Ping Google DNS to check latency
    host = "8.8.8.8"  # Google's public DNS server
    param = "-n" if platform.system().lower() == "windows" else "-c"

    try:
        command = ["ping", param, "1", host]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Extract latency from the result
        output = result.stdout.decode()
        if platform.system().lower() == "windows":
            # On Windows, look for "Average = Xms"
            latency = output.split("Average = ")[-1].replace("ms", "").strip()
        else:
            # On Linux/Mac, look for the "time=X ms" value
            latency = output.split("time=")[-1].split(" ")[0]
        return float(latency)
    except Exception as e:
        print(f"Error retrieving network latency: {e}")
        return None
