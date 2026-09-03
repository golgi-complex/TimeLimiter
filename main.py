import os
import sys
import time
import json
import hashlib
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

# --- НАСТРОЙКИ (не меняются без пересборки) ---
GRACE_MINUTES = 5           # Время на ввод пароля при исчерпанном лимите (в минутах)
CONFIG_FILE = "C:\\ProgramData\\timer_config.json"  # Лимит, пароль (хеш), вкл/выкл
DATA_FILE = "C:\\ProgramData\\timer_data.txt"        # Отработанное сегодня время


# --- РАБОТА С ПАРОЛЕМ ---

def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()


# --- РАБОТА С КОНФИГОМ (лимит / пароль / вкл-выкл) ---

def default_config() -> dict:
    return {
        "limit_minutes": 60,
        "password_hash": hash_password("1234"),  # смените через --settings сразу после установки
        "limit_enabled": True,
    }


def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        config = default_config()
        save_config(config)
        return config
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        defaults = default_config()
        for key, value in defaults.items():
            config.setdefault(key, value)
        return config
    except Exception:
        config = default_config()
        save_config(config)
        return config


def save_config(config: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f)
    except Exception:
        pass


# --- РАБОТА С ДАННЫМИ ЗА ДЕНЬ ---

def read_data():
    # Возвращает (дата, использовано_минут, бонусных_минут_за_сегодня)
    today_str = datetime.date.today().isoformat()
    if not os.path.exists(DATA_FILE):
        return today_str, 0, 0
    try:
        with open(DATA_FILE, "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 3 and lines[0] == today_str:
                return today_str, int(lines[1]), int(lines[2])
    except Exception:
        pass
    return today_str, 0, 0


def save_data(date_str, used_minutes, bonus_minutes):
    try:
        with open(DATA_FILE, "w") as f:
            f.write(f"{date_str}\n{used_minutes}\n{bonus_minutes}")
    except Exception:
        pass


def force_shutdown():
    os.system("shutdown /s /f /t 0")


# --- ОКНО ВВОДА ПАРОЛЯ (используется и для продления, и для доступа к настройкам) ---

def ask_password_window(config: dict, title: str, message: str) -> bool:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    start_time = time.time()
    while time.time() - start_time < GRACE_MINUTES * 60:
        pwd = simpledialog.askstring(title, message, show="*", parent=root)
        if pwd is not None and hash_password(pwd) == config["password_hash"]:
            root.destroy()
            return True
        elif pwd is None:
            break
        else:
            messagebox.showerror("Ошибка", "Неверный пароль!", parent=root)
    root.destroy()
    return False


# --- ОКНО НАСТРОЕК (лимит, пароль, вкл/выкл) ---

def show_settings_window(config: dict):
    root = tk.Tk()
    root.title("Настройки Screen Time Guard")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    tk.Label(root, text="Дневной лимит (минут):").grid(row=0, column=0, sticky="w", padx=10, pady=8)
    limit_var = tk.StringVar(value=str(config["limit_minutes"]))
    tk.Entry(root, textvariable=limit_var, width=10).grid(row=0, column=1, padx=10, pady=8)

    enabled_var = tk.BooleanVar(value=config["limit_enabled"])
    tk.Checkbutton(root, text="Лимит включён", variable=enabled_var).grid(
        row=1, column=0, columnspan=2, sticky="w", padx=10, pady=4
    )

    tk.Label(root, text="Новый пароль (оставьте пустым, чтобы не менять):").grid(
        row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(12, 2)
    )
    pwd_var = tk.StringVar()
    tk.Entry(root, textvariable=pwd_var, show="*", width=20).grid(
        row=3, column=0, columnspan=2, padx=10, pady=2
    )

    def on_save():
        try:
            new_limit = int(limit_var.get())
            if new_limit <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Лимит должен быть положительным целым числом", parent=root)
            return

        config["limit_minutes"] = new_limit
        config["limit_enabled"] = enabled_var.get()

        new_pwd = pwd_var.get().strip()
        if new_pwd:
            config["password_hash"] = hash_password(new_pwd)

        save_config(config)
        messagebox.showinfo("Готово", "Настройки сохранены", parent=root)
        root.destroy()

    tk.Button(root, text="Сохранить", command=on_save, width=12).grid(row=4, column=0, padx=10, pady=15)
    tk.Button(root, text="Отмена", command=root.destroy, width=12).grid(row=4, column=1, padx=10, pady=15)

    root.mainloop()


def run_settings():
    # Запуск: timer.exe --settings. Доступ только после ввода правильного пароля
    config = load_config()
    if not ask_password_window(config, "Настройки Screen Time Guard", "Введите пароль для доступа к настройкам:"):
        sys.exit()
    show_settings_window(config)


# --- ОСНОВНОЙ РЕЖИМ СЛЕЖЕНИЯ ---

def main():
    config = load_config()
    today_str, used_minutes, bonus_minutes = read_data()

    def check_limit():
        # Проверяет лимит; при верном пароле продлевает его ещё на limit_minutes
        nonlocal used_minutes, bonus_minutes, config
        config = load_config()  # подхватываем изменения, сделанные через --settings

        if not config["limit_enabled"]:
            return

        effective_limit = config["limit_minutes"] + bonus_minutes
        if used_minutes >= effective_limit:
            if ask_password_window(
                config,
                "Лимит времени исчерпан",
                f"Дневной лимит исчерпан.\nВведите пароль, чтобы продлить ещё на {config['limit_minutes']} минут:",
            ):
                bonus_minutes += config["limit_minutes"]
                save_data(today_str, used_minutes, bonus_minutes)
            else:
                force_shutdown()
                sys.exit()

    # Проверка сразу при старте (например, если лимит уже был исчерпан до перезагрузки)
    check_limit()

    while True:
        time.sleep(60)  # проверка каждую минуту
        current_date_str = datetime.date.today().isoformat()
        if current_date_str != today_str:
            today_str = current_date_str
            used_minutes = 0
            bonus_minutes = 0
        used_minutes += 1
        save_data(today_str, used_minutes, bonus_minutes)
        check_limit()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--settings":
        run_settings()
    else:
        main()
