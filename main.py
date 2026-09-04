import logging
import subprocess
import sys
import tkinter as tk
import threading
import time

from pathlib import Path
from datetime import date

from pynput import keyboard, mouse


APP_NAME = "TimeLimiter"


# --------------------------------------------------
# Application directory
# --------------------------------------------------

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent


SETTINGS_FILE = BASE_DIR / "settings.txt"
USAGE_FILE = BASE_DIR / "usage.txt"
LOG_FILE = BASE_DIR / "timelimiter.log"


# Как часто сохранять usage.txt
USAGE_SAVE_INTERVAL = 10

# Через сколько секунд без активности
# останавливаем таймер
INACTIVITY_TIMEOUT = 10


# --------------------------------------------------
# Create application directory
# --------------------------------------------------

BASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(APP_NAME)


# --------------------------------------------------
# Settings
# --------------------------------------------------

def create_default_settings():
    try:
        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            file.write("limit_minutes=5\n")
            file.write("password=1234\n")
            file.write("timer_enabled=true\n")

        logger.info(
            "Default settings file created."
        )

    except Exception:
        logger.exception(
            "Failed to create default settings file."
        )


def load_settings():

    settings = {
        "limit_minutes": 5,
        "password": "1234",
        "timer_enabled": True,
    }

    if not SETTINGS_FILE.exists():

        logger.warning(
            "Settings file not found. "
            "Creating default settings."
        )

        create_default_settings()

        return settings

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line or "=" not in line:
                    continue

                key, value = line.split(
                    "=",
                    1,
                )

                key = key.strip()
                value = value.strip()

                if key == "limit_minutes":

                    try:
                        settings["limit_minutes"] = int(
                            value
                        )

                    except ValueError:

                        logger.warning(
                            "Invalid limit_minutes value: %s. "
                            "Using default.",
                            value,
                        )

                elif key == "password":

                    settings["password"] = value

                elif key == "timer_enabled":

                    settings["timer_enabled"] = (
                        value.lower() == "true"
                    )

    except Exception:

        logger.exception(
            "Failed to read settings file."
        )

    return settings


# --------------------------------------------------
# Usage
# --------------------------------------------------

def load_usage():

    today = date.today().isoformat()

    usage = {
        "date": today,
        "used_seconds": 0,
    }

    if not USAGE_FILE.exists():

        logger.info(
            "Usage file not found. "
            "Starting from 0 seconds."
        )

        save_usage(usage)

        return usage

    try:

        with open(
            USAGE_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line or "=" not in line:
                    continue

                key, value = line.split(
                    "=",
                    1,
                )

                key = key.strip()
                value = value.strip()

                if key == "date":

                    usage["date"] = value

                elif key == "used_seconds":

                    try:
                        usage["used_seconds"] = int(
                            value
                        )

                    except ValueError:

                        logger.warning(
                            "Invalid used_seconds value: %s. "
                            "Resetting to 0.",
                            value,
                        )

                        usage["used_seconds"] = 0

    except Exception:

        logger.exception(
            "Failed to read usage file."
        )

        return usage

    # Новый день
    if usage["date"] != today:

        logger.info(
            "New day detected. "
            "Resetting usage from %s seconds.",
            usage["used_seconds"],
        )

        usage["date"] = today
        usage["used_seconds"] = 0

        save_usage(usage)

    return usage


def save_usage(usage):

    try:

        with open(
            USAGE_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                f"date={usage['date']}\n"
            )

            file.write(
                f"used_seconds={usage['used_seconds']}\n"
            )

    except Exception:

        logger.exception(
            "Failed to save usage data."
        )


# --------------------------------------------------
# Main application
# --------------------------------------------------

def main():

    logger.info(
        "=" * 60
    )

    logger.info(
        "TimeLimiter started"
    )

    logger.info(
        "Application directory: %s",
        BASE_DIR,
    )

    settings = load_settings()

    logger.info(
        "Settings loaded: limit=%s minutes, "
        "timer_enabled=%s",
        settings["limit_minutes"],
        settings["timer_enabled"],
    )

    usage = load_usage()

    logger.info(
        "Usage loaded: date=%s, "
        "used_seconds=%s",
        usage["date"],
        usage["used_seconds"],
    )

    # --------------------------------------------------
    # Time calculation
    # --------------------------------------------------

    limit_seconds = (
        settings["limit_minutes"] * 60
    )

    remaining_seconds = max(
        0,
        limit_seconds - usage["used_seconds"],
    )

    logger.info(
        "Remaining time: %s seconds",
        remaining_seconds,
    )

    # --------------------------------------------------
    # Activity tracking
    # --------------------------------------------------

    last_activity_time = time.monotonic()

    activity_lock = threading.Lock()

    def register_activity():

        nonlocal last_activity_time

        with activity_lock:

            last_activity_time = time.monotonic()

    def keyboard_activity(key):

        register_activity()

    def mouse_activity(*args):

        register_activity()

    keyboard_listener = keyboard.Listener(
        on_press=keyboard_activity,
    )

    mouse_listener = mouse.Listener(
        on_move=mouse_activity,
        on_click=mouse_activity,
        on_scroll=mouse_activity,
    )

    keyboard_listener.start()
    mouse_listener.start()

    logger.info(
        "Keyboard and mouse activity monitoring started."
    )

    # --------------------------------------------------
    # Tkinter
    # --------------------------------------------------

    root = tk.Tk()

    root.overrideredirect(True)

    root.attributes(
        "-topmost",
        True,
    )

    transparent_color = "#000001"

    root.configure(
        bg=transparent_color
    )

    root.attributes(
        "-transparentcolor",
        transparent_color,
    )

    window_width = 180
    window_height = 60

    screen_width = (
        root.winfo_screenwidth()
    )

    x = (
        screen_width - window_width
    ) // 2

    y = 0

    root.geometry(
        f"{window_width}x{window_height}+{x}+{y}"
    )

    if not settings["timer_enabled"]:

        root.withdraw()

        logger.info(
            "Timer display is disabled."
        )

    timer_label = tk.Label(
        root,
        text="00:00",
        font=(
            "Segoe UI",
            31,
            "bold",
        ),
        fg="#7CFC00",
        bg=transparent_color,
    )

    timer_label.pack(
        expand=True
    )

    # --------------------------------------------------
    # State
    # --------------------------------------------------

    blink_visible = True

    password_window = None

    password_timeout_seconds = 60

    password_timeout_job = None

    seconds_since_save = 0

    was_inactive = False

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    def shutdown_computer():

        logger.warning(
            "Password timeout reached. "
            "Shutting down Windows."
        )

        try:

            subprocess.run(
                [
                    "shutdown",
                    "/s",
                    "/t",
                    "0",
                ],
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

        except Exception:

            logger.exception(
                "Failed to execute "
                "Windows shutdown command."
            )

    # --------------------------------------------------
    # Timer color
    # --------------------------------------------------

    def update_timer_color():

        # Если пользователь бездействует,
        # таймер становится голубым.
        if was_inactive:

            color = "#00BFFF"

        elif remaining_seconds > 15 * 60:

            color = "#7CFC00"

        elif remaining_seconds >= 5 * 60:

            color = "#FFA500"

        else:

            color = "#FF3333"

        timer_label.config(
            fg=color
        )

    # --------------------------------------------------
    # Blink timer
    # --------------------------------------------------

    def blink_timer():

        nonlocal blink_visible

        if remaining_seconds <= 0:

            blink_visible = (
                not blink_visible
            )

            if blink_visible:

                timer_label.config(
                    fg="#FF3333"
                )

            else:

                timer_label.config(
                    fg=transparent_color
                )

            root.after(
                500,
                blink_timer,
            )

    # --------------------------------------------------
    # Password window
    # --------------------------------------------------

    def show_password_window():

        nonlocal password_window
        nonlocal password_timeout_seconds
        nonlocal password_timeout_job

        if password_window is not None:
            return

        logger.info(
            "Daily time limit reached. "
            "Showing password window."
        )

        password_window = tk.Toplevel(
            root
        )

        password_window.title(
            "TimeLimiter"
        )

        password_window.resizable(
            False,
            False,
        )

        password_window.attributes(
            "-topmost",
            True,
        )

        password_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: None,
        )

        window_width = 360
        window_height = 230

        screen_width = (
            password_window.winfo_screenwidth()
        )

        screen_height = (
            password_window.winfo_screenheight()
        )

        x = (
            screen_width - window_width
        ) // 2

        y = (
            screen_height - window_height
        ) // 2

        password_window.geometry(
            f"{window_width}x{window_height}+{x}+{y}"
        )

        title_label = tk.Label(
            password_window,
            text="Time limit reached",
            font=(
                "Segoe UI",
                16,
                "bold",
            ),
        )

        title_label.pack(
            pady=(20, 5)
        )

        message_label = tk.Label(
            password_window,
            text=(
                "Enter the parent password "
                "to continue."
            ),
            font=(
                "Segoe UI",
                10,
            ),
        )

        message_label.pack(
            pady=(0, 10)
        )

        timeout_label = tk.Label(
            password_window,
            text="Time remaining: 01:00",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
        )

        timeout_label.pack(
            pady=(0, 10)
        )

        password_entry = tk.Entry(
            password_window,
            font=(
                "Segoe UI",
                12,
            ),
            show="*",
            justify="center",
            width=25,
        )

        password_entry.pack()

        error_label = tk.Label(
            password_window,
            text="",
            font=(
                "Segoe UI",
                9,
            ),
        )

        error_label.pack(
            pady=(5, 5)
        )

        def update_password_timeout():

            nonlocal password_timeout_seconds
            nonlocal password_timeout_job

            if password_window is None:
                return

            if password_timeout_seconds <= 0:

                timeout_label.config(
                    text="Time remaining: 00:00"
                )

                logger.info(
                    "Password entry timeout reached."
                )

                password_timeout_job = None

                shutdown_computer()

                return

            minutes = (
                password_timeout_seconds // 60
            )

            seconds = (
                password_timeout_seconds % 60
            )

            timeout_label.config(
                text=(
                    f"Time remaining: "
                    f"{minutes:02d}:{seconds:02d}"
                )
            )

            password_timeout_seconds -= 1

            password_timeout_job = (
                password_window.after(
                    1000,
                    update_password_timeout,
                )
            )

        def check_password():

            nonlocal remaining_seconds
            nonlocal password_window
            nonlocal password_timeout_job
            nonlocal seconds_since_save

            entered_password = (
                password_entry.get()
            )

            if (
                entered_password
                == settings["password"]
            ):

                logger.info(
                    "Correct parent password entered."
                )

                if password_timeout_job is not None:

                    try:

                        password_window.after_cancel(
                            password_timeout_job
                        )

                    except tk.TclError:
                        pass

                    password_timeout_job = None

                remaining_seconds = (
                    limit_seconds
                )

                usage["used_seconds"] = (
                    limit_seconds
                )

                save_usage(
                    usage
                )

                seconds_since_save = 0

                password_window.destroy()

                password_window = None

                register_activity()

                was_inactive = False

                update_timer_color()

                logger.info(
                    "Session extended by %s minutes.",
                    settings["limit_minutes"],
                )

                root.after(
                    1000,
                    update_timer,
                )

            else:

                logger.warning(
                    "Incorrect parent password entered."
                )

                error_label.config(
                    text="Incorrect password."
                )

                password_entry.delete(
                    0,
                    tk.END,
                )

                password_entry.focus_set()

        ok_button = tk.Button(
            password_window,
            text="OK",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            width=10,
            command=check_password,
        )

        ok_button.pack(
            pady=(0, 15)
        )

        password_entry.bind(
            "<Return>",
            lambda event: check_password(),
        )

        password_entry.focus_set()

        password_timeout_seconds = 60

        password_timeout_job = (
            password_window.after(
                1000,
                update_password_timeout,
            )
        )

    # --------------------------------------------------
    # Main timer
    # --------------------------------------------------

    def update_timer():

        nonlocal remaining_seconds
        nonlocal seconds_since_save
        nonlocal was_inactive

        # Проверяем новый день
        today = date.today().isoformat()

        if usage["date"] != today:

            logger.info(
                "Midnight reached. "
                "Resetting daily usage "
                "from %s seconds.",
                usage["used_seconds"],
            )

            usage["date"] = today

            usage["used_seconds"] = 0

            remaining_seconds = (
                limit_seconds
            )

            seconds_since_save = 0

            save_usage(
                usage
            )

            logger.info(
                "Daily limit reset. "
                "New remaining time: %s seconds.",
                remaining_seconds,
            )

        # --------------------------------------------------
        # Check inactivity
        # --------------------------------------------------

        with activity_lock:

            inactive_seconds = (
                time.monotonic()
                - last_activity_time
            )

        is_inactive = (
            inactive_seconds
            >= INACTIVITY_TIMEOUT
        )

        if is_inactive:

            if not was_inactive:

                logger.info(
                    "User inactive for %s seconds. "
                    "Timer paused.",
                    INACTIVITY_TIMEOUT,
                )

                was_inactive = True

            # Показываем голубой цвет
            # во время паузы.
            timer_label.config(
                fg="#00BFFF"
            )

            # Время НЕ списываем.
            root.after(
                1000,
                update_timer,
            )

            return

        # --------------------------------------------------
        # User active again
        # --------------------------------------------------

        if was_inactive:

            logger.info(
                "User activity detected. "
                "Timer resumed."
            )

            was_inactive = False

        # --------------------------------------------------
        # Time limit reached
        # --------------------------------------------------

        if remaining_seconds <= 0:

            timer_label.config(
                text="00:00"
            )

            save_usage(
                usage
            )

            seconds_since_save = 0

            blink_timer()

            show_password_window()

            return

        # --------------------------------------------------
        # Update timer
        # --------------------------------------------------

        update_timer_color()

        minutes = (
            remaining_seconds // 60
        )

        seconds = (
            remaining_seconds % 60
        )

        timer_label.config(
            text=(
                f"{minutes:02d}:{seconds:02d}"
            )
        )

        # Списываем одну секунду
        remaining_seconds -= 1

        usage["used_seconds"] += 1

        seconds_since_save += 1

        # Сохраняем каждые 10 секунд
        if (
            seconds_since_save
            >= USAGE_SAVE_INTERVAL
        ):

            save_usage(
                usage
            )

            seconds_since_save = 0

        root.after(
            1000,
            update_timer,
        )

    # --------------------------------------------------
    # Start timer
    # --------------------------------------------------

    if settings["timer_enabled"]:

        update_timer()

    # --------------------------------------------------
    # Main loop
    # --------------------------------------------------

    try:

        root.mainloop()

    finally:

        logger.info(
            "Stopping keyboard and mouse listeners."
        )

        keyboard_listener.stop()
        mouse_listener.stop()


# --------------------------------------------------
# Application entry point
# --------------------------------------------------

if __name__ == "__main__":

    try:

        main()

    except Exception:

        logger.exception(
            "Fatal application error."
        )

        raise
