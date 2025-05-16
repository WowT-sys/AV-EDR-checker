import win32com.client
import pythoncom
import time
import random
import os
import sys
import ctypes
from ctypes import wintypes
import threading
import uuid
import platform
import winreg
import socket
import locale
import datetime

class SystemInfoUtility:
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.start_time = datetime.datetime.now()
        self.system_info = self._collect_basic_system_info()
        self.execution_context = self._analyze_execution_context()
        self.operation_mode = self._determine_operation_mode()
        self._initialize_environment()
    
    def _initialize_environment(self):
        try:
            locale.setlocale(locale.LC_ALL, '')
        except:
            pass
        self.is_virtual = self._check_if_virtual_environment()
        self._perform_startup_sequence()
    
    def _perform_startup_sequence(self):
        self._check_single_instance()
        self._adaptive_delay(50, 150)
        self._check_common_registry_settings()
    
    def _check_single_instance(self):
        try:
            random_name = f"Global\\{uuid.uuid4().hex[:12]}"
            ctypes.windll.kernel32.GetLastError()
        except:
            pass
    
    def _check_common_registry_settings(self):
        try:
            reg_paths = [
                (winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced"),
                (winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"),
                (winreg.HKEY_CURRENT_USER, "Control Panel\\International")
            ]
            for root, path in reg_paths:
                try:
                    key = winreg.OpenKey(root, path, 0, winreg.KEY_READ)
                    winreg.CloseKey(key)
                    self._adaptive_delay(1, 5)
                except:
                    pass
        except:
            pass
    
    def _collect_basic_system_info(self):
        info = {}
        try:
            info['hostname'] = socket.gethostname()
            info['os_version'] = platform.platform()
            info['python_version'] = platform.python_version()
            info['processor'] = platform.processor()
            try:
                info['screen_width'] = ctypes.windll.user32.GetSystemMetrics(0)
                info['screen_height'] = ctypes.windll.user32.GetSystemMetrics(1)
            except:
                pass
        except:
            pass
        return info
    
    def _check_if_virtual_environment(self):
        try:
            vm_indicators = [
                "vmware",
                "virtualbox",
                "qemu",
                "xen",
                "parallels"
            ]
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    "SYSTEM\\CurrentControlSet\\Control\\SystemInformation")
                manufacturer = winreg.QueryValueEx(key, "SystemManufacturer")[0].lower()
                winreg.CloseKey(key)
                for indicator in vm_indicators:
                    if indicator in manufacturer:
                        return True
            except:
                pass
            return False
        except:
            return False
    
    def _analyze_execution_context(self):
        context = {}
        context['parent_process'] = self._get_parent_process()
        try:
            context['exe_path'] = os.path.abspath(sys.argv[0])
            context['exe_dir'] = os.path.dirname(context['exe_path'])
        except:
            context['exe_path'] = "unknown"
            context['exe_dir'] = "unknown"
        try:
            context['is_admin'] = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            context['is_admin'] = False
        try:
            context['user_profile'] = os.environ.get('USERPROFILE', '')
        except:
            context['user_profile'] = ""
        return context
    
    def _get_parent_process(self):
        try:
            class PROCESS_BASIC_INFORMATION(ctypes.Structure):
                _fields_ = [
                    ("Reserved1", ctypes.c_void_p),
                    ("PebBaseAddress", ctypes.c_void_p),
                    ("Reserved2", ctypes.c_void_p * 2),
                    ("UniqueProcessId", ctypes.c_void_p),
                    ("InheritedFromUniqueProcessId", ctypes.c_void_p)
                ]
            return os.getppid()
        except:
            return "unknown"
    
    def _determine_operation_mode(self):
        mode = {
            'stealth_level': 0,
            'can_use_wmi': True,
            'can_use_registry': True,
            'can_use_filesystem': True
        }
        parent = self.execution_context.get('parent_process', 'unknown')
        suspicious_parents = ["procmon", "wireshark", "processhacker", "ida", "x64dbg"]
        if any(p in str(parent).lower() for p in suspicious_parents):
            mode['stealth_level'] = 2
        if "\\temp\\" in self.execution_context.get('exe_dir', '').lower():
            mode['stealth_level'] = max(mode['stealth_level'], 1)
        if self.execution_context.get('is_admin', False):
            mode['stealth_level'] = max(0, mode['stealth_level'] - 1)
        return mode
    
    def _adaptive_delay(self, min_ms=10, max_ms=50):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0")
            mhz = winreg.QueryValueEx(key, "~MHz")[0]
            winreg.CloseKey(key)
            performance_factor = min(1.0, max(0.5, 2000 / max(1, mhz)))
        except:
            performance_factor = 1.0
        base_delay = random.uniform(min_ms/1000, max_ms/1000)
        actual_delay = base_delay * performance_factor
        event = threading.Event()
        event.wait(timeout=actual_delay)
    
    def check_security_products(self):
        results = []
        if self.operation_mode['stealth_level'] >= 2:
            return results
        self._simulate_user_interaction()
        try:
            if self._is_ui_context():
                pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
            else:
                pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
            self._adaptive_delay(5, 20)
            properties = ["displayName", "productState"]
            query = f"SELECT {', '.join(properties)} FROM AntivirusProduct"
            try:
                locator = win32com.client.Dispatch("WbemScripting.SWbemLocator")
                service = locator.ConnectServer(".", "ROOT\\SecurityCenter2")
                self._adaptive_delay(5, 20)
                items = service.ExecQuery(query, "WQL", 48)
                for item in items:
                    try:
                        self._adaptive_delay(1, 5)
                        av_info = {}
                        name = getattr(item, 'displayName', 'Unknown')
                        state = getattr(item, 'productState', 0)
                        state_hex = f'{state:06x}'.upper()
                        enabled_hex = state_hex[2:4]
                        update_hex = state_hex[4:6]
                        enabled_status = 'Enabled' if enabled_hex == '10' else 'Disabled'
                        update_status = 'Up to Date' if update_hex == '00' else 'Not Up to Date'
                        av_info['name'] = name
                        av_info['state_hex'] = state_hex
                        av_info['enabled'] = enabled_status
                        av_info['updates'] = update_status
                        results.append(av_info)
                    except Exception:
                        continue
            except Exception:
                pass
        except Exception:
            pass
        finally:
            try:
                pythoncom.CoUninitialize()
            except:
                pass
        return results
    
    def detect_multiple_security_products(self, security_products):
        product_names = [product['name'].lower() for product in security_products]
        unique_products = set(product_names)
        return len(unique_products) > 1, unique_products
    
    def _is_ui_context(self):
        parent = str(self.execution_context.get('parent_process', '')).lower()
        ui_parents = ["explorer", "cmd", "powershell", "pythonw"]
        return any(p in parent for p in ui_parents)
    
    def _simulate_user_interaction(self):
        try:
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            pt = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            foreground_window = ctypes.windll.user32.GetForegroundWindow()
            text_len = ctypes.windll.user32.GetWindowTextLengthW(foreground_window)
            return (pt.x, pt.y, foreground_window, text_len)
        except:
            pass
    
    def generate_report(self, security_products, verbose=False, silent=False):
        if silent:
            return
        execution_time = (datetime.datetime.now() - self.start_time).total_seconds()
        if verbose:
            print(f"\nSystem Information Utility [{self.session_id}]")
            print(f"System: {self.system_info.get('os_version', 'Unknown')}")
            print(f"Execution Time: {execution_time:.2f} seconds")
            print(f"{'=' * 50}")
        if not security_products:
            print("No security products detected or information unavailable.")
            return
        print(f"\nDetected {len(security_products)} security product(s):")
        for i, product in enumerate(security_products, 1):
            print(f"\n{i}. {product['name']}")
            print(f"   Status: {product['enabled']}")
            print(f"   Definitions: {product['updates']}")
            if verbose:
                print(f"   State Code: {product['state_hex']}")
        if verbose:
            print(f"\nInformation collected at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    args = parse_arguments()
    utility = SystemInfoUtility()
    utility._adaptive_delay(20, 80)
    security_products = utility.check_security_products()
    has_multiple, unique_products = utility.detect_multiple_security_products(security_products)
    if has_multiple:
        print("\nMultiple security products detected:")
        for product in unique_products:
            print(f" - {product}")
    else:
        print("\nOnly one security product detected.")
    utility.generate_report(
        security_products, 
        verbose=args.get('verbose', False),
        silent=args.get('silent', False)
    )
    return security_products

def parse_arguments():
    args = {}
    for arg in sys.argv[1:]:
        if arg in ['--silent', '-s']:
            args['silent'] = True
        elif arg in ['--verbose', '-v']:
            args['verbose'] = True
        elif arg in ['--help', '-h', '/?']:
            print_help()
            sys.exit(0)
    return args

def print_help():
    print("System Information Utility")
    print("Usage: python script.py [options]")
    print("\nOptions:")
    print("  -s, --silent     Run silently without output")
    print("  -v, --verbose    Show detailed information")
    print("  -h, --help       Show this help message")

if __name__ == "__main__":
    try:
        time.sleep(random.uniform(0.05, 0.2))
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        if '--debug' in sys.argv:
            print(f"Error: {str(e)}")
        sys.exit(1)
