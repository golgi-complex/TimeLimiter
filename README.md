<<<<<<< HEAD
# TimeLimiter (`main.py`)
=======
# TimeLimiter
>>>>>>> b953006 (feat: Add timer overlay and improve security. README update)

**Родительский контроль экранного времени для Windows 10/11**

TimeLimiter — приложение для ограничения ежедневного времени работы за компьютером. При достижении установленного лимита программа запрашивает родительский пароль для продления сеанса или автоматически выключает/блокирует компьютер.

Программа работает в фоновом режиме и автоматически запускается вместе с Windows.

---

## Возможности

* **Суточный лимит** — по умолчанию 60 минут. Время считается суммарно за текущий день и автоматически сбрасывается в полночь.
* **Оверлей-таймер** — полупрозрачное окно поверх других окон показывает оставшееся время с цветовой индикацией:

  * 🟢 зелёный — более 15 минут;
  * 🟠 оранжевый — от 5 до 15 минут;
  * 🔴 красный — менее 5 минут;
  * мигание — время вышло.
* **Защита от обхода** — после окончания доступного времени появляется окно ввода родительского пароля с 5-минутным таймером.
* **Автоматическое действие** — если пароль не введён в течение 5 минут, компьютер выключается или блокируется в зависимости от настроек.
* **Продление сеанса** — правильный пароль добавляет к дневному лимиту ещё `limit_minutes` минут. Продление можно выполнять многократно.
* **Настройки** — отдельное окно с возможностью:

  * изменить дневной лимит;
  * включить или отключить ограничение;
  * включить или отключить отображение таймера;
  * выбрать действие после превышения лимита;
  * установить время предупреждения;
  * изменить родительский пароль.
* **Хеширование пароля** — пароль не хранится в открытом виде.
* **Логирование** — события и ошибки записываются в `C:\ProgramData\TimeLimiter\timer.log`.
* **Защита от двойного запуска** — предотвращает запуск нескольких экземпляров программы одновременно.
* **Скрытый режим** — приложение может работать без консольного окна после сборки в `.exe`.

---

## Установка и запуск из исходного кода

### Требования

* Windows 10 или Windows 11
* Python 3.12+
* Git — опционально, только для клонирования репозитория

Python можно скачать с официального сайта:

https://python.org

### Клонирование репозитория

Клонируйте репозиторий и перейдите в его директорию:

```bash
git clone https://github.com/golgi-complex/TimeLimiter.git
cd TimeLimiter
```

<<<<<<< HEAD
Убедитесь, что в рабочей директории проекта созданы файлы `main.py` и `requirements.txt`. Выполните в терминале команду установки:
=======
Также можно скачать репозиторий в виде ZIP-архива и распаковать его вручную.

### Создание виртуального окружения

Рекомендуется использовать отдельное виртуальное окружение:

```bash
python -m venv myenv
```

Активируйте его:
>>>>>>> b953006 (feat: Add timer overlay and improve security. README update)

```powershell
myenv\Scripts\activate
```

### Установка зависимостей

Установите необходимые Python-пакеты:

```bash
pip install -r requirements.txt
```

### Запуск программы

Запуск основного режима:

```bash
python main.py
```

Запуск окна настроек:

```bash
python main.py --settings
```

Для доступа к настройкам потребуется родительский пароль.

Пароль по умолчанию:

<<<<<<< HEAD
```powershell
copy-item "dist\main.exe" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\main.exe" -Force
=======
```text
1234
```

Просмотр справки:

```bash
python main.py --help
>>>>>>> b953006 (feat: Add timer overlay and improve security. README update)
```

---

<<<<<<< HEAD
## 6. Настройки в коде (`main.py`)
=======
## Сборка исполняемого `.exe`
>>>>>>> b953006 (feat: Add timer overlay and improve security. README update)

Для запуска программы на компьютере без установленного Python можно собрать самостоятельный `.exe`-файл с помощью **PyInstaller**.

Установите PyInstaller:

```bash
pip install pyinstaller
```

Выполните сборку:

```bash
pyinstaller --noconsole --onefile --name TimeLimiter main.py
```

После завершения сборки готовый файл будет находиться здесь:

```text
dist\TimeLimiter.exe
```

Параметр `--noconsole` отключает отображение консольного окна при запуске приложения.

---

## Автозапуск вместе с Windows

Чтобы TimeLimiter автоматически запускался для всех пользователей при старте Windows, скопируйте собранный `.exe` в системную папку автозапуска.

Из PowerShell:

```powershell
Copy-Item "dist\TimeLimiter.exe" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\TimeLimiter.exe" -Force
```

После этого программа будет запускаться автоматически при входе пользователя в Windows.

---

## Конфигурационные файлы

Все настройки, данные и логи хранятся в:

```text
C:\ProgramData\TimeLimiter\
```

Основные файлы:

| Файл                | Назначение                                      |
| ------------------- | ----------------------------------------------- |
| `timer_config.json` | Настройки программы и хеш пароля                |
| `timer_data.txt`    | Счётчик использованного времени за текущий день |
| `timer.log`         | Журнал событий и ошибок                         |

Все необходимые файлы и директории создаются автоматически при первом запуске.

---

## Настройки по умолчанию

| Параметр          |      Значение | Описание                                                |
| ----------------- | ------------: | ------------------------------------------------------- |
| `limit_minutes`   |          `60` | Дневной лимит в минутах                                 |
| `password_hash`   | хеш от `1234` | Родительский пароль по умолчанию                        |
| `limit_enabled`   |        `true` | Включено ли ограничение времени                         |
| `auto_shutdown`   |        `true` | `true` — выключение, `false` — блокировка               |
| `warning_minutes` |           `1` | За сколько минут до окончания показывать предупреждение |
| `show_timer`      |        `true` | Показывать ли оверлей-таймер                            |

> **Важно:** после первого запуска рекомендуется изменить пароль по умолчанию.

---

## Использование

### Таймер

При запуске программы в верхней части экрана появляется таймер, если отображение таймера включено в настройках.

Таймер:

* показывает оставшееся время;
* меняет цвет в зависимости от оставшегося времени;
* можно перемещать мышью;
* можно временно скрыть нажатием на кнопку закрытия.

После скрытия таймер автоматически появится снова через минуту.

### Предупреждение

Когда до окончания доступного времени остаётся установленное в настройках количество минут, программа показывает предупреждение.

По умолчанию предупреждение появляется за 1 минуту до окончания.

### Окончание времени

После полного использования дневного лимита появляется окно ввода родительского пароля.

Если введён правильный пароль:

1. проверяется пароль;
2. к доступному времени добавляется ещё `limit_minutes` минут;
3. пользователь продолжает работу;
4. при необходимости пароль можно вводить повторно для дальнейшего продления.

Если пароль не введён в течение 5 минут, выполняется выбранное действие:

* выключение компьютера;
* или блокировка компьютера.

---

## Настройки

Для открытия окна настроек используйте:

```bash
python main.py --settings
```

В собранной версии приложения настройки запускаются с параметром:

```text
TimeLimiter.exe --settings
```

Доступ к настройкам защищён родительским паролем.

В окне настроек доступны:

* изменение дневного лимита;
* включение/отключение ограничения;
* включение/отключение таймера;
* выбор действия после окончания времени;
* настройка времени предупреждения;
* изменение родительского пароля.

---

## Безопасность

TimeLimiter использует следующие механизмы защиты:

* пароль не хранится в открытом виде;
* пароль преобразуется в SHA-256 хеш с использованием соли;
* конфигурация и данные хранятся в системной директории `ProgramData`;
* предусмотрена защита от запуска нескольких экземпляров приложения;
* родительские настройки защищены паролем.

> TimeLimiter предназначен прежде всего для бытового родительского контроля. Это не является полноценной системой информационной безопасности и не гарантирует защиту от пользователя с административными правами Windows.

---

## Структура проекта

Основная логика приложения разделена на несколько компонентов:

| Компонент        | Назначение                                     |
| ---------------- | ---------------------------------------------- |
| `TimeLimiter`    | Основная логика подсчёта и ограничения времени |
| `TimerOverlay`   | Оверлей с отображением оставшегося времени     |
| `SettingsWindow` | Окно настроек программы                        |
| `main.py`        | Точка входа приложения                         |

Основные настройки и поведение программы можно изменить непосредственно в `main.py`.

---

## Логирование

Для диагностики работы приложения используется журнал:

```text
C:\ProgramData\TimeLimiter\timer.log
```

В лог записываются основные события программы, включая:

* запуск и завершение;
* изменение настроек;
* запуск таймера;
* достижение лимита;
* попытки ввода пароля;
* продление времени;
* ошибки.

Лог рекомендуется использовать при диагностике проблем с запуском или работой приложения.

---

## Лицензия

Лицензия проекта не указана.


# TimeLimiter

**Parental Screen Time Control for Windows 10/11**

TimeLimiter is a parental control application that limits the amount of time a user can spend on a Windows computer each day.

When the daily limit is reached, the application requests a parent password to extend the session. If the correct password is not entered within the configured timeout, the computer is automatically shut down or locked.

TimeLimiter runs in the background and can be configured to start automatically with Windows.

---

## Features

* **Daily time limit** — 60 minutes by default. Usage time is accumulated throughout the day and automatically resets at midnight.
* **Timer overlay** — a semi-transparent always-on-top window displays the remaining time with color indicators:

  * 🟢 Green — more than 15 minutes remaining;
  * 🟠 Orange — 5–15 minutes remaining;
  * 🔴 Red — less than 5 minutes remaining;
  * Blinking — time has expired.
* **Bypass protection** — when the time limit is reached, a password window appears with a 5-minute countdown.
* **Automatic action** — if the correct password is not entered within 5 minutes, the computer is shut down or locked, depending on the selected setting.
* **Session extension** — entering the correct parent password adds another `limit_minutes` to the available time. The session can be extended multiple times.
* **Settings window** — provides options to:

  * change the daily time limit;
  * enable or disable the time limit;
  * enable or disable the timer overlay;
  * choose the action after the limit is reached;
  * configure the warning time;
  * change the parent password.
* **Password hashing** — passwords are not stored in plain text.
* **Logging** — application events and errors are written to `C:\ProgramData\TimeLimiter\timer.log`.
* **Single-instance protection** — prevents multiple copies of the application from running simultaneously.
* **Silent mode** — the application can run without a console window when built as an `.exe`.

---

## Installation and Running from Source

### Requirements

* Windows 10 or Windows 11
* Python 3.12+
* Git — optional, only required for cloning the repository

Python can be downloaded from:

https://python.org

### Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/golgi-complex/TimeLimiter.git
cd TimeLimiter
```

Alternatively, you can download the repository as a ZIP archive and extract it manually.

### Create a Virtual Environment

Using a dedicated virtual environment is recommended:

```bash
python -m venv myenv
```

Activate the virtual environment:

```powershell
myenv\Scripts\activate
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Run the Application

Start the main time-tracking mode:

```bash
python main.py
```

Open the settings window:

```bash
python main.py --settings
```

The settings window requires the parent password.

Default password:

```text
1234
```

Display the command-line help:

```bash
python main.py --help
```

---

## Building the `.exe`

To run TimeLimiter on a computer without Python installed, you can build a standalone executable using **PyInstaller**.

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the application:

```bash
pyinstaller --noconsole --onefile --name TimeLimiter main.py
```

After the build is complete, the executable will be available at:

```text
dist\TimeLimiter.exe
```

The `--noconsole` option prevents a console window from appearing when the application starts.

---

## Windows Startup

To start TimeLimiter automatically when Windows starts, copy the executable to the system Startup folder.

Run the following command in PowerShell:

```powershell
Copy-Item "dist\TimeLimiter.exe" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\TimeLimiter.exe" -Force
```

After that, TimeLimiter will automatically start when a user logs into Windows.

---

## Configuration Files

All configuration, application data, and logs are stored in:

```text
C:\ProgramData\TimeLimiter\
```

Main files:

| File                | Description                            |
| ------------------- | -------------------------------------- |
| `timer_config.json` | Application settings and password hash |
| `timer_data.txt`    | Time usage counter for the current day |
| `timer.log`         | Application event and error log        |

All required files and directories are created automatically on the first launch.

---

## Default Settings

| Parameter         |  Default Value | Description                                                 |
| ----------------- | -------------: | ----------------------------------------------------------- |
| `limit_minutes`   |           `60` | Daily time limit in minutes                                 |
| `password_hash`   | Hash of `1234` | Default parent password                                     |
| `limit_enabled`   |         `true` | Enables or disables the time limit                          |
| `auto_shutdown`   |         `true` | `true` — shut down, `false` — lock                          |
| `warning_minutes` |            `1` | Number of minutes before the limit when the warning appears |
| `show_timer`      |         `true` | Enables or disables the timer overlay                       |

> **Important:** It is strongly recommended to change the default password after the first launch.

---

## Usage

### Timer Overlay

When TimeLimiter starts, a timer appears at the top of the screen if the timer overlay is enabled.

The timer:

* displays the remaining time;
* changes color depending on the remaining time;
* can be moved with the mouse;
* can be temporarily hidden using the close button.

After being hidden, the timer automatically appears again after one minute.

### Warning

When the remaining time reaches the configured warning threshold, TimeLimiter displays a notification.

The default warning time is **1 minute** before the daily limit is reached.

### Time Limit Reached

When the daily time limit is fully used, a parent password window appears.

If the correct password is entered:

1. the password is verified;
2. another `limit_minutes` is added to the available time;
3. the user can continue using the computer;
4. the password can be entered again later to extend the session further.

If the correct password is not entered within 5 minutes, the selected action is performed:

* shut down the computer;
* or lock the computer.

---

## Settings

To open the settings window from source code:

```bash
python main.py --settings
```

For the compiled version:

```text
TimeLimiter.exe --settings
```

Access to the settings is protected by the parent password.

Available settings include:

* daily time limit;
* enable/disable time restriction;
* enable/disable timer overlay;
* shutdown or lock after the limit is reached;
* warning time;
* parent password.

---

## Security

TimeLimiter uses several mechanisms to protect the application configuration:

* passwords are not stored in plain text;
* passwords are stored as SHA-256 hashes with a salt;
* configuration and application data are stored in the `ProgramData` directory;
* multiple application instances are prevented;
* access to parental settings is password protected.

> **Note:** TimeLimiter is primarily intended for everyday parental control. It is not a full security solution and cannot guarantee protection against a user with Windows administrator privileges.

---

## Project Structure

The application is organized into several main components:

| Component        | Description                                    |
| ---------------- | ---------------------------------------------- |
| `TimeLimiter`    | Core time tracking and limit enforcement logic |
| `TimerOverlay`   | Timer overlay and remaining-time display       |
| `SettingsWindow` | Application settings window                    |
| `main.py`        | Application entry point                        |

The main application logic and behavior can be modified in `main.py`.

---

## Logging

TimeLimiter maintains an application log at:

```text
C:\ProgramData\TimeLimiter\timer.log
```

The log contains important application events, including:

* application startup and shutdown;
* settings changes;
* timer activity;
* time limit reached;
* password attempts;
* session extensions;
* errors and exceptions.

The log can be useful when troubleshooting application issues.

---

## License

No license has been specified for this project.
