"""
TimeLimiter - программа для контроля времени работы на компьютере
Версия: 2.1 - с оверлей-таймером
"""

import os
import sys
import time
import json
import hashlib
import datetime
import logging
import threading
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from typing import Dict, Tuple, Optional

# Настройка логирования
LOG_FILE = Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / "TimeLimiter" / "timer.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Константы
GRACE_MINUTES = 5
CONFIG_DIR = Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / "TimeLimiter"
CONFIG_FILE = CONFIG_DIR / "timer_config.json"
DATA_FILE = CONFIG_DIR / "timer_data.txt"

# Создаем директорию если её нет
CONFIG_DIR.mkdir(parents=True, exist_ok=True)


class TimerOverlay:
    """Оверлей с таймером поверх всех окон"""

    def __init__(self):
        self.root = None
        self.label = None
        self.is_visible = False
        self.update_thread = None
        self.running = False

    def create_overlay(self):
        """Создание оверлей-окна"""
        self.root = tk.Tk()
        self.root.title("TimeLimiter - Таймер")

        # Настройки окна
        self.root.overrideredirect(True)  # Без рамок
        self.root.attributes("-topmost", True)  # Поверх всех окон
        self.root.attributes("-alpha", 0.9)  # Полупрозрачное
        self.root.geometry("280x80+{}+{}".format(
            self.root.winfo_screenwidth() // 2 - 140,  # Центр по горизонтали
            10  # Отступ сверху
        ))

        # Фоновый цвет
        self.root.configure(bg='#2c2c2c')

        # Заголовок
        title_label = tk.Label(
            self.root,
            text="⏱ ОСТАЛОСЬ ВРЕМЕНИ",
            font=('Segoe UI', 10, 'bold'),
            fg='#aaaaaa',
            bg='#2c2c2c'
        )
        title_label.pack(pady=(8, 0))

        # Время
        self.label = tk.Label(
            self.root,
            text="--:--",
            font=('Segoe UI', 32, 'bold'),
            fg='#00ff00',
            bg='#2c2c2c'
        )
        self.label.pack(pady=(0, 8))

        # Кнопка закрытия (маленькая, незаметная)
        close_btn = tk.Label(
            self.root,
            text="✕",
            font=('Segoe UI', 8),
            fg='#666666',
            bg='#2c2c2c',
            cursor='hand2'
        )
        close_btn.place(x=260, y=5)
        close_btn.bind('<Button-1>', self.hide)

        # Возможность перетаскивать окно
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)

        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        # Прячем окно при запуске
        self.root.withdraw()
        self.is_visible = False

    def start_move(self, event):
        """Начало перетаскивания"""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """Перетаскивание окна"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_time(self, minutes_left: int):
        """Обновление отображаемого времени"""
        if self.label and self.is_visible:
            if minutes_left < 0:
                minutes_left = 0

            hours = minutes_left // 60
            mins = minutes_left % 60

            if hours > 0:
                time_str = f"{hours:02d}:{mins:02d}"
            else:
                time_str = f"{mins:02d}:00"

            self.label.config(text=time_str)

            # Меняем цвет в зависимости от оставшегося времени
            if minutes_left <= 5:
                self.label.config(fg='#ff0000')  # Красный - критично
            elif minutes_left <= 15:
                self.label.config(fg='#ff8800')  # Оранжевый - скоро закончится
            else:
                self.label.config(fg='#00ff00')  # Зеленый - нормально

            # Если осталось 0, мигаем
            if minutes_left <= 0:
                self.start_blinking()
            else:
                self.stop_blinking()

    def start_blinking(self):
        """Запуск мигания при нулевом времени"""
        if not hasattr(self, 'blink_state'):
            self.blink_state = False
            self.blink_after_id = None

        if self.blink_after_id:
            self.root.after_cancel(self.blink_after_id)
            self.blink_after_id = None

        self.do_blink()

    def do_blink(self):
        """Мигание текста"""
        if self.is_visible and self.label:
            if self.blink_state:
                self.label.config(fg='#ff0000')
            else:
                self.label.config(fg='#2c2c2c')  # Цвет фона - скрываем текст

            self.blink_state = not self.blink_state
            self.blink_after_id = self.root.after(500, self.do_blink)

    def stop_blinking(self):
        """Остановка мигания"""
        if hasattr(self, 'blink_after_id') and self.blink_after_id:
            self.root.after_cancel(self.blink_after_id)
            self.blink_after_id = None

        if self.label and self.is_visible:
            self.label.config(fg='#00ff00')

    def show(self):
        """Показать таймер"""
        if not self.root:
            self.create_overlay()

        self.root.deiconify()
        self.is_visible = True
        logger.info("Таймер отображен")

        # Запускаем поток обновления, если его нет
        if not self.running:
            self.running = True
            # Обновление через отдельный поток
            threading.Thread(target=self._update_loop, daemon=True).start()

    def hide(self, event=None):
        """Скрыть таймер"""
        if self.root:
            self.root.withdraw()
            self.is_visible = False
            self.running = False
            self.stop_blinking()
            logger.info("Таймер скрыт")

    def _update_loop(self):
        """Цикл обновления времени в отдельном потоке"""
        from queue import Queue
        self.update_queue = Queue()

        # Получаем ссылку на основной объект TimeLimiter
        # Это будет установлено из main
        while self.running:
            if hasattr(self, 'limiter') and self.limiter:
                config = self.limiter.config
                effective_limit = config["limit_minutes"] + self.limiter.bonus_minutes
                minutes_left = effective_limit - self.limiter.used_minutes

                # Обновляем UI через main thread
                if self.root:
                    self.root.after(0, lambda: self.update_time(minutes_left))

            time.sleep(1)  # Обновление каждую секунду

    def set_limiter(self, limiter):
        """Установка ссылки на основной объект"""
        self.limiter = limiter

    def destroy(self):
        """Закрытие оверлея"""
        self.running = False
        if self.root:
            self.root.destroy()
            self.root = None


class TimeLimiter:
    """Основной класс программы TimeLimiter"""

    def __init__(self):
        self.config = self.load_config()
        self.today_str, self.used_minutes, self.bonus_minutes = self.read_data()
        self.lock = threading.Lock()
        self.running = True
        self.overlay = TimerOverlay()
        self.overlay.set_limiter(self)

    @staticmethod
    def hash_password(pwd: str) -> str:
        """Хеширование пароля с солью для дополнительной безопасности"""
        salt = "TimeLimiterSalt2024"
        return hashlib.sha256((salt + pwd).encode("utf-8")).hexdigest()

    @staticmethod
    def default_config() -> dict:
        """Конфигурация по умолчанию"""
        return {
            "limit_minutes": 5,
            "password_hash": TimeLimiter.hash_password("1234"),
            "limit_enabled": True,
            "auto_shutdown": True,
            "warning_minutes": 1,
            "show_timer": True,  # Новая опция - показывать таймер
        }

    def load_config(self) -> dict:
        """Загрузка конфигурации с обработкой ошибок"""
        try:
            if not CONFIG_FILE.exists():
                config = self.default_config()
                self.save_config(config)
                return config

            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)

            defaults = self.default_config()
            for key, value in defaults.items():
                config.setdefault(key, value)

            return config

        except Exception as e:
            logger.error(f"Ошибка загрузки конфигурации: {e}")
            config = self.default_config()
            self.save_config(config)
            return config

    def save_config(self, config: dict):
        """Сохранение конфигурации"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            logger.info("Конфигурация сохранена")
        except Exception as e:
            logger.error(f"Ошибка сохранения конфигурации: {e}")

    def read_data(self) -> Tuple[str, int, int]:
        """Чтение данных за сегодняшний день"""
        today_str = datetime.date.today().isoformat()

        if not DATA_FILE.exists():
            return today_str, 0, 0

        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                if len(lines) >= 3 and lines[0] == today_str:
                    return today_str, int(lines[1]), int(lines[2])
        except Exception as e:
            logger.error(f"Ошибка чтения данных: {e}")

        return today_str, 0, 0

    def save_data(self, date_str: str, used_minutes: int, bonus_minutes: int):
        """Сохранение данных"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                f.write(f"{date_str}\n{used_minutes}\n{bonus_minutes}")
        except Exception as e:
            logger.error(f"Ошибка сохранения данных: {e}")

    def force_shutdown(self):
        """Принудительное выключение компьютера или блокировка"""
        # Скрываем таймер перед выключением
        self.overlay.hide()

        if self.config.get("auto_shutdown", True):
            logger.warning("Выключение компьютера!")
            os.system("shutdown /s /f /t 0")
        else:
            logger.warning("Блокировка компьютера!")
            os.system("rundll32.exe user32.dll,LockWorkStation")
            sys.exit()

    def ask_password(self, title: str, message: str) -> bool:
        """Диалог ввода пароля с таймаутом"""
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        start_time = time.time()
        grace_seconds = GRACE_MINUTES * 60

        while time.time() - start_time < grace_seconds:
            remaining = int(grace_seconds - (time.time() - start_time))
            message_with_time = f"{message}\n\nОсталось времени: {remaining} секунд"

            pwd = simpledialog.askstring(
                title,
                message_with_time,
                show='*',
                parent=root
            )

            if pwd is not None:
                if self.hash_password(pwd) == self.config["password_hash"]:
                    root.destroy()
                    logger.info("Пароль введен верно")
                    return True
                else:
                    messagebox.showerror("Ошибка", "Неверный пароль!", parent=root)
            else:
                break

        root.destroy()
        logger.warning("Время ввода пароля истекло или отменено")
        return False

    def show_warning(self, minutes_left: int):
        """Показать предупреждение о скором окончании времени"""
        if minutes_left <= 0:
            return

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        messagebox.showwarning(
            "⚠ Внимание!",
            f"До окончания лимита времени осталось {minutes_left} минут!",
            parent=root
        )
        root.destroy()

    def check_limit(self):
        """Проверка лимита с возможностью продления"""
        with self.lock:
            self.config = self.load_config()

            if not self.config["limit_enabled"]:
                # Если лимит выключен, скрываем таймер
                if self.config.get("show_timer", True):
                    self.overlay.hide()
                return

            effective_limit = self.config["limit_minutes"] + self.bonus_minutes

            # Показываем или скрываем таймер
            if self.config.get("show_timer", True):
                self.overlay.show()
            else:
                self.overlay.hide()

            # Проверяем, нужно ли показать предупреждение
            if self.config.get("warning_minutes", 1) > 0:
                minutes_left = effective_limit - self.used_minutes
                if 0 < minutes_left <= self.config.get("warning_minutes", 1):
                    self.show_warning(minutes_left)

            if self.used_minutes >= effective_limit:
                if self.ask_password(
                    "Лимит времени исчерпан",
                    f"Дневной лимит ({effective_limit} мин) исчерпан.\n"
                    f"Введите пароль для продления еще на {self.config['limit_minutes']} минут:"
                ):
                    self.bonus_minutes += self.config["limit_minutes"]
                    self.save_data(self.today_str, self.used_minutes, self.bonus_minutes)
                    logger.info(f"Время продлено. Бонус: {self.bonus_minutes} мин")
                else:
                    self.force_shutdown()

    def run(self):
        """Основной цикл программы"""
        logger.info("TimeLimiter запущен")

        # Показываем таймер при старте если включен
        if self.config.get("show_timer", True) and self.config["limit_enabled"]:
            self.overlay.show()

        # Первичная проверка при старте
        self.check_limit()

        while self.running:
            time.sleep(60)  # Проверка каждую минуту

            current_date_str = datetime.date.today().isoformat()

            # Сброс в полночь
            if current_date_str != self.today_str:
                logger.info("Новый день - сброс счетчиков")
                self.today_str = current_date_str
                self.used_minutes = 0
                self.bonus_minutes = 0

            self.used_minutes += 1
            self.save_data(self.today_str, self.used_minutes, self.bonus_minutes)

            # Проверяем лимит каждые 5 минут
            if self.used_minutes % 5 == 0:
                self.check_limit()

    def stop(self):
        """Остановка программы"""
        self.running = False
        self.overlay.destroy()
        logger.info("TimeLimiter остановлен")


class SettingsWindow:
    """Окно настроек"""

    def __init__(self, config: dict):
        self.config = config.copy()
        self.root = None
        self.limit_var = None
        self.enabled_var = None
        self.auto_shutdown_var = None
        self.warning_var = None
        self.show_timer_var = None
        self.pwd_var = None

    def show(self):
        """Отображение окна настроек"""
        self.root = tk.Tk()
        self.root.title("Настройки TimeLimiter")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Лимит времени
        ttk.Label(main_frame, text="Дневной лимит (минут):").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.limit_var = tk.StringVar(value=str(self.config["limit_minutes"]))
        ttk.Entry(main_frame, textvariable=self.limit_var, width=10).grid(
            row=0, column=1, sticky=tk.W, pady=5
        )

        # Включение/выключение
        self.enabled_var = tk.BooleanVar(value=self.config["limit_enabled"])
        ttk.Checkbutton(
            main_frame,
            text="Лимит включён",
            variable=self.enabled_var
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Показывать таймер
        self.show_timer_var = tk.BooleanVar(value=self.config.get("show_timer", True))
        ttk.Checkbutton(
            main_frame,
            text="Показывать таймер поверх всех окон",
            variable=self.show_timer_var
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Автоматическое выключение
        self.auto_shutdown_var = tk.BooleanVar(value=self.config.get("auto_shutdown", True))
        ttk.Checkbutton(
            main_frame,
            text="Выключать компьютер при превышении (иначе блокировать)",
            variable=self.auto_shutdown_var
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Предупреждение
        ttk.Label(main_frame, text="Предупреждение за (минут до окончания):").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.warning_var = tk.StringVar(value=str(self.config.get("warning_minutes", 1)))
        ttk.Entry(main_frame, textvariable=self.warning_var, width=10).grid(
            row=4, column=1, sticky=tk.W, pady=5
        )

        # Смена пароля
        ttk.Label(
            main_frame,
            text="Новый пароль (оставьте пустым, чтобы не менять):"
        ).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(15, 5))

        self.pwd_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.pwd_var, show="*", width=20).grid(
            row=6, column=0, columnspan=2, pady=5
        )

        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)

        ttk.Button(
            btn_frame,
            text="Сохранить",
            command=self.on_save,
            width=12
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Отмена",
            command=self.root.destroy,
            width=12
        ).pack(side=tk.LEFT, padx=5)

        # Центрируем окно
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.root.mainloop()

    def on_save(self):
        """Сохранение настроек"""
        try:
            new_limit = int(self.limit_var.get())
            if new_limit <= 0:
                raise ValueError("Лимит должен быть положительным числом")

            warning_minutes = int(self.warning_var.get())
            if warning_minutes < 0:
                raise ValueError("Предупреждение не может быть отрицательным")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e), parent=self.root)
            return

        # Обновляем конфигурацию
        self.config["limit_minutes"] = new_limit
        self.config["limit_enabled"] = self.enabled_var.get()
        self.config["auto_shutdown"] = self.auto_shutdown_var.get()
        self.config["warning_minutes"] = warning_minutes
        self.config["show_timer"] = self.show_timer_var.get()

        # Меняем пароль если введен
        new_pwd = self.pwd_var.get().strip()
        if new_pwd:
            self.config["password_hash"] = TimeLimiter.hash_password(new_pwd)
            logger.info("Пароль изменен")

        # Сохраняем
        limiter = TimeLimiter()
        limiter.save_config(self.config)

        messagebox.showinfo("Готово", "Настройки сохранены", parent=self.root)
        self.root.destroy()


def run_settings():
    """Запуск режима настроек"""
    limiter = TimeLimiter()

    # Запрашиваем пароль для доступа к настройкам
    if not limiter.ask_password(
        "Настройки TimeLimiter",
        "Введите пароль для доступа к настройкам:"
    ):
        logger.warning("Доступ к настройкам запрещен")
        sys.exit()

    # Показываем окно настроек
    settings = SettingsWindow(limiter.config)
    settings.show()


def main():
    """Главная функция"""
    # Проверяем, не запущен ли уже экземпляр
    try:
        import psutil
        current_pid = os.getpid()
        process_name = os.path.basename(sys.argv[0])

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['pid'] != current_pid and proc.info['name'] == process_name:
                    logger.warning("Программа уже запущена")
                    sys.exit()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except ImportError:
        logger.warning("psutil не установлен, проверка запущенных экземпляров пропущена")

    # Запускаем основной режим
    limiter = TimeLimiter()

    try:
        limiter.run()
    except KeyboardInterrupt:
        logger.info("Программа остановлена пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        limiter.stop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--settings":
            run_settings()
        elif sys.argv[1] == "--version":
            print("TimeLimiter v2.1")
        elif sys.argv[1] == "--help":
            print("""
TimeLimiter - контроль времени работы на компьютере

Использование:
  python main.py                 - Запуск в режиме слежения
  python main.py --settings      - Открыть настройки
  python main.py --version       - Показать версию
  python main.py --help          - Показать эту справку
            """)
        else:
            print(f"Неизвестный аргумент: {sys.argv[1]}")
    else:
        main()
