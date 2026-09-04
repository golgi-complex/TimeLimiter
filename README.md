# TimeLimiter

**Простой родительский контроль для ограничения ежедневного времени работы за компьютером в Windows 10/11.**

TimeLimiter отслеживает активное использование компьютера и ограничивает количество времени, которое пользователь может проводить за компьютером каждый день. После достижения дневного лимита TimeLimiter запрашивает родительский пароль для продолжения работы. Если правильный пароль не введён в течение 60 секунд, Windows автоматически выключается.

Приложение работает в фоновом режиме и может быть настроено на автоматический запуск вместе с Windows.

---

## Возможности

* ⏱️ Ограничение ежедневного времени работы за компьютером
* 🖱️⌨️ Автоматическая пауза после 10 секунд отсутствия активности клавиатуры или мыши
* 🔐 Защита родительским паролем
* ⏳ Таймер для ввода пароля
* 🛑 Автоматическое выключение Windows после истечения времени ожидания
* 🌙 Автоматический сброс дневного лимита в полночь
* 📊 Сохранение информации об использованном времени
* 💾 Сохранение данных об использовании каждые 10 секунд
* 🎨 Цветовая индикация оставшегося времени
* 📌 Таймер поверх всех окон
* ⚙️ Простая текстовая конфигурация
* 📝 Ведение журнала работы приложения
* 🚀 Поддержка автоматического запуска Windows
* 📦 Возможность создания портативного `.exe`
* 🪟 Поддержка Windows 10 и Windows 11

---

## Как работает TimeLimiter

TimeLimiter поддерживает обратный отсчёт, показывающий количество доступного времени работы за компьютером в текущем дне.

Например, если установлен дневной лимит:

```text
5 минут
```

таймер начинается со значения:

```text
05:00
```

При активном использовании компьютера таймер постепенно уменьшается.

Если в течение 10 секунд не происходит никакой активности клавиатуры или мыши, таймер автоматически приостанавливается.

После возобновления активности отсчёт продолжается.

### Пример

```text
05:00
04:59
04:58
...
04:52

[10 секунд без активности клавиатуры/мыши]

04:52  ← таймер приостановлен

[движение мыши]

04:52
04:51
04:50
...
```

Время бездействия **не вычитается** из доступного дневного времени.

---

## Цвета таймера

Цвет таймера зависит от оставшегося времени.

| Оставшееся время                  | Цвет                | Значение                |
| --------------------------------- | ------------------- | ----------------------- |
| Более 15 минут                    | 🟢 Зелёный          | Достаточно времени      |
| 5–15 минут                        | 🟠 Оранжевый        | Времени становится мало |
| Менее 5 минут                     | 🔴 Красный          | Критический уровень     |
| Пауза из-за отсутствия активности | 🔵 Синий            | Таймер приостановлен    |
| `00:00`                           | 🔴 Мигающий красный | Дневной лимит достигнут |

Синий цвет при отсутствии активности имеет приоритет над обычной цветовой индикацией времени.

Например, если осталось 3 минуты и пользователь перестал пользоваться компьютером, таймер изменит цвет с красного на синий.

---

## Дневной лимит

Дневной лимит настраивается через файл:

```text
settings.txt
```

Значение по умолчанию:

```text
limit_minutes=5
```

Значение указывается в минутах.

Например:

```text
limit_minutes=60
```

устанавливает дневной лимит в один час.

---

## Родительский пароль

Родительский пароль также задаётся в файле `settings.txt`.

Значение по умолчанию:

```text
password=1234
```

Когда дневной лимит достигает `00:00`, TimeLimiter отображает окно ввода пароля.

На ввод правильного пароля даётся 60 секунд.

### Правильный пароль

Если пароль введён правильно:

1. Окно ввода пароля закрывается.
2. Сессия продлевается ещё на полный период дневного лимита.
3. Данные об использовании обновляются.
4. Таймер продолжает отсчёт.

Например, если установлено:

```text
limit_minutes=30
```

после правильного ввода пароля пользователь получает ещё:

```text
30 минут
```

доступного времени.

### Неправильный пароль

Неправильный пароль не продлевает сессию.

Пользователь может продолжать попытки ввода, пока не истечёт 60-секундный таймер.

### Истечение времени ввода пароля

Если правильный пароль не введён в течение 60 секунд:

```text
shutdown /s /t 0
```

выполняется автоматически, после чего Windows немедленно выключается.

> **Примечание по безопасности:** в текущей версии родительский пароль хранится в открытом виде в `settings.txt`. Это сделано намеренно для упрощения текущей версии приложения. Такой способ хранения не обеспечивает защиту от технически подготовленного пользователя.

---

## Автоматический сброс в полночь

Информация об использованном времени автоматически сбрасывается в начале нового дня.

Например:

```text
date=2026-09-04
used_seconds=270
```

После наступления нового дня TimeLimiter обнаружит изменение даты и установит:

```text
date=2026-09-05
used_seconds=0
```

После этого снова становится доступен полный дневной лимит.

---

## Конфигурация

TimeLimiter использует простой текстовый файл:

```text
settings.txt
```

Пример содержимого:

```text
limit_minutes=5
password=1234
timer_enabled=true
```

### `limit_minutes`

Определяет ежедневный лимит времени.

Например:

```text
limit_minutes=60
```

означает один час доступного времени в день.

### `password`

Родительский пароль, необходимый для продления сессии.

Например:

```text
password=123456
```

### `timer_enabled`

Определяет, отображается ли таймер на экране.

Включить:

```text
timer_enabled=true
```

Выключить:

```text
timer_enabled=false
```

При отключённом отображении таймера отслеживание и подсчёт времени продолжает работать.

---

## Файлы приложения

TimeLimiter хранит свои файлы **в той же директории, где находится запущенное приложение**.

При запуске через Python:

```text
TimeLimiter/
├── main.py
├── settings.txt
├── usage.txt
├── timelimiter.log
└── requirements.txt
```

При запуске скомпилированного `.exe`:

```text
TimeLimiter/
├── TimeLimiter.exe
├── settings.txt
├── usage.txt
└── timelimiter.log
```

Такой подход делает приложение портативным.

Если `TimeLimiter.exe` переместить в другую директорию, файлы конфигурации, статистики и журнала будут созданы рядом с новым расположением `.exe`.

---

## Данные об использовании

Информация об использованном времени хранится в:

```text
usage.txt
```

Пример:

```text
date=2026-09-04
used_seconds=127
```

### `date`

Дата, к которой относится информация об использовании.

### `used_seconds`

Количество секунд, которые были засчитаны в текущем дне.

TimeLimiter сохраняет эту информацию каждые 10 секунд.

Это позволяет минимизировать потерю данных при неожиданном закрытии приложения или Windows.

---

## Журнал работы

Информация о работе приложения записывается в:

```text
timelimiter.log
```

Журнал содержит информацию, например, о:

* запуске приложения;
* загрузке конфигурации;
* загрузке данных об использовании;
* оставшемся времени;
* запуске мониторинга клавиатуры и мыши;
* обнаружении бездействия;
* постановке таймера на паузу;
* возобновлении таймера;
* попытках ввода пароля;
* истечении времени ввода пароля;
* сбросе дневного лимита;
* выключении Windows;
* ошибках приложения.

Пример:

```text
2026-09-04 12:00:00 | INFO | TimeLimiter started
2026-09-04 12:00:00 | INFO | Usage loaded: date=2026-09-04, used_seconds=0
2026-09-04 12:00:00 | INFO | Keyboard and mouse activity monitoring started.
2026-09-04 12:00:10 | INFO | User inactive for 10 seconds. Timer paused.
2026-09-04 12:00:15 | INFO | User activity detected. Timer resumed.
```

---

## Отслеживание активности

Для мониторинга активности клавиатуры и мыши TimeLimiter использует библиотеку `pynput`.

### Клавиатура

Отслеживаются:

* нажатия клавиш.

### Мышь

Отслеживаются:

* движение мыши;
* нажатия кнопок;
* прокрутка колёсика.

Если активность отсутствует в течение:

```text
10 секунд
```

таймер использования компьютера приостанавливается.

Порог бездействия задаётся в `main.py`:

```python
INACTIVITY_TIMEOUT = 10
```

Когда таймер приостановлен из-за отсутствия активности:

* обратный отсчёт останавливается;
* время использования не расходуется;
* таймер становится синим;
* приложение продолжает отслеживать активность.

Как только обнаруживается движение мыши или нажатие клавиши, таймер возобновляет работу и возвращается к обычной цветовой индикации.

---

## Таймер на экране

Таймер отображается в виде прозрачного оверлея в верхней центральной части экрана.

Пример:

```text
          04:37
```

Окно таймера:

* не имеет стандартной рамки Windows;
* находится поверх остальных окон;
* располагается по центру экрана;
* имеет прозрачный фон;
* отображает оставшееся время в формате `MM:SS`.

Отображение таймера можно отключить через:

```text
timer_enabled=false
```

---

## Структура проекта

Проект имеет простую структуру:

```text
TimeLimiter/
│
├── main.py
├── requirements.txt
├── README.md
│
├── settings.txt
├── usage.txt
└── timelimiter.log
```

Следующие файлы создаются автоматически при первом запуске приложения:

* `settings.txt`
* `usage.txt`
* `timelimiter.log`

---

## Требования

### Операционная система

* Windows 10
* Windows 11

### Python

Для разработки используется Python 3.12.

### Python-зависимости

Проект использует:

```text
pynput==1.8.2
pyinstaller==6.22.2
```

`pynput` используется приложением для глобального мониторинга клавиатуры и мыши.

`pyinstaller` используется для создания автономного исполняемого файла Windows.

---

## Установка для разработки

Клонировать репозиторий:

```powershell
git clone https://github.com/golgi-complex/TimeLimiter.git
```

Перейти в директорию проекта:

```powershell
cd TimeLimiter
```

Создать виртуальное окружение:

```powershell
python -m venv myenv
```

Активировать виртуальное окружение:

```powershell
.\myenv\Scripts\Activate.ps1
```

Установить зависимости:

```powershell
pip install -r requirements.txt
```

---

## Запуск через Python

Запустить приложение:

```powershell
python main.py
```

При первом запуске TimeLimiter автоматически создаст:

```text
settings.txt
usage.txt
timelimiter.log
```

в той же директории, где находится `main.py`.

---

## Создание Windows `.exe`

TimeLimiter можно собрать в автономный `.exe` с помощью PyInstaller.

Команда сборки:

```powershell
pyinstaller --onefile --noconsole --name TimeLimiter main.py
```

После успешной сборки исполняемый файл будет находиться здесь:

```text
dist\TimeLimiter.exe
```

Для запуска готового `.exe` установка Python на целевом компьютере не требуется.

---

## Установка исполняемого файла

Рекомендуемая директория установки:

```text
C:\ProgramData\TimeLimiter
```

Финальная структура может выглядеть следующим образом:

```text
C:\ProgramData\TimeLimiter\
│
├── TimeLimiter.exe
├── settings.txt
├── usage.txt
└── timelimiter.log
```

Поскольку TimeLimiter хранит свои файлы относительно расположения исполняемого файла, хранение `.exe` и файлов конфигурации в одной директории упрощает управление приложением и его перенос.

---

## Автоматический запуск Windows

TimeLimiter можно настроить на автоматический запуск вместе с Windows.

Рекомендуемый способ:

1. Оставить исполняемый файл здесь:

```text
C:\ProgramData\TimeLimiter\TimeLimiter.exe
```

2. Создать ярлык Windows, указывающий на:

```text
C:\ProgramData\TimeLimiter\TimeLimiter.exe
```

3. Поместить этот ярлык в папку автозагрузки Windows.

Для системной автозагрузки используется:

```text
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

### Важно

**Не рекомендуется помещать сам `TimeLimiter.exe` непосредственно в папку Startup**, если необходимо, чтобы файлы приложения оставались в:

```text
C:\ProgramData\TimeLimiter
```

TimeLimiter специально хранит:

```text
settings.txt
usage.txt
timelimiter.log
```

рядом с исполняемым файлом.

Поэтому `.exe` должен оставаться здесь:

```text
C:\ProgramData\TimeLimiter
```

а в папке Startup должен находиться **ярлык**, указывающий на этот `.exe`.

---

## Тестирование

Для разработки и тестирования стандартный лимит намеренно установлен небольшим:

```text
limit_minutes=5
```

Это позволяет быстро проверить работу приложения.

### Тестирование паузы при бездействии

1. Запустите TimeLimiter.
2. Не двигайте мышью и не нажимайте клавиши.
3. Подождите 10 секунд.
4. Таймер должен стать синим.
5. Обратный отсчёт должен остановиться.
6. Переместите мышь или нажмите клавишу.
7. Таймер должен вернуться к обычному цвету.
8. Обратный отсчёт должен продолжиться.

### Тестирование дневного лимита

Для ускорения тестирования временно измените:

```text
limit_minutes=5
```

на:

```text
limit_minutes=1
```

Таймер начнёт отсчёт с:

```text
01:00
```

После достижения:

```text
00:00
```

должно появиться окно ввода пароля.

### Тестирование пароля

Пароль по умолчанию:

```text
1234
```

Введите правильный пароль.

Таймер должен получить ещё один полный период работы.

Например, при лимите 5 минут:

```text
05:00
```

### Тестирование таймера ввода пароля

После появления окна пароля не вводите пароль.

Через 60 секунд TimeLimiter выполнит:

```text
shutdown /s /t 0
```

и Windows выключится.

> Будьте осторожны при тестировании этой функции на реальном компьютере. Перед тестом сохраните всю важную работу.

---

## Принятые архитектурные решения

### Подсчёт только активного времени

TimeLimiter учитывает только периоды, когда пользователь активно взаимодействует с компьютером.

Если клавиатура и мышь не используются в течение 10 секунд, таймер приостанавливается.

Это предотвращает расход дневного лимита во время простоя компьютера.

### Локальная конфигурация

Конфигурация хранится в обычном текстовом файле вместо реестра Windows.

Преимущества:

* простота редактирования;
* простота резервного копирования;
* лёгкий просмотр;
* портативность;
* отсутствие необходимости в установщике.

### Хранение файлов рядом с приложением

Файлы приложения хранятся рядом с исполняемым файлом.

Это позволяет избежать жёстко заданных путей и делает приложение портативным.

### Простая архитектура

Приложение намеренно использует небольшое количество зависимостей и по возможности использует стандартную библиотеку Python.

---

## Безопасность

TimeLimiter предназначен как **простая утилита родительского контроля**, а не как защищённая система безопасности.

Текущая версия не пытается защищать приложение от технически подготовленного пользователя.

Например, приложение не предотвращает:

* завершение процесса через Диспетчер задач;
* редактирование `settings.txt`;
* удаление `usage.txt`;
* изменение исполняемого файла;
* загрузку другой операционной системы;
* использование административных инструментов Windows.

Приложение намеренно оставлено простым, поскольку его основная задача — обеспечить базовое ограничение времени для обычного использования компьютера.

---

## Известные ограничения

* Родительский пароль хранится в открытом виде.
* Файлы приложения не защищены от ручного изменения.
* Процесс приложения можно завершить через Диспетчер задач.
* Нет графического интерфейса настроек.
* Данные об использовании не синхронизируются между несколькими компьютерами.
* Нет удалённого управления для родителей.
* Для определения активности используются только клавиатура и мышь.
* Интервал бездействия в текущей версии задаётся непосредственно в исходном коде.
* Приложение работает только в Windows.

---

## Технологии

TimeLimiter использует:

* **Python 3.12** — основной язык и среда выполнения
* **Tkinter** — графический интерфейс
* **pynput** — мониторинг клавиатуры и мыши
* **PyInstaller** — создание Windows `.exe`
* **Windows shutdown command** — автоматическое выключение системы
* **Python logging** — ведение журнала приложения

---

## Отказ от ответственности

TimeLimiter предоставляется «как есть».

При истечении времени ввода пароля приложение напрямую использует команду выключения Windows. Перед использованием приложения на рабочем компьютере рекомендуется тщательно протестировать его в контролируемой среде.

# TimeLimiter

**Simple parental control for limiting daily computer usage on Windows 10/11.**

TimeLimiter tracks active computer usage and limits the amount of time a user can spend at the computer each day. When the daily limit is reached, TimeLimiter requests a parent password to extend the session. If the correct password is not entered within 60 seconds, Windows is automatically shut down.

The application runs quietly in the background and can be configured to start automatically with Windows.

---

## Features

* ⏱️ Daily computer usage limit
* 🖱️⌨️ Automatic pause after 10 seconds without keyboard or mouse activity
* 🔐 Parent password protection
* ⏳ Password entry timeout
* 🛑 Automatic Windows shutdown when the timeout expires
* 🌙 Automatic daily reset at midnight
* 📊 Persistent usage tracking
* 💾 Usage data saved every 10 seconds
* 🎨 Color-coded remaining-time indicator
* 📌 Always-on-top timer overlay
* ⚙️ Simple text-based configuration
* 📝 Application logging
* 🚀 Windows startup support
* 📦 Portable `.exe` build
* 🪟 Supports Windows 10 and Windows 11

---

## How TimeLimiter Works

TimeLimiter maintains a countdown representing the amount of computer usage available for the current day.

For example, if the daily limit is:

```text
5 minutes
```

the timer starts at:

```text
05:00
```

While the computer is actively being used, the timer counts down.

If there is no keyboard or mouse activity for 10 seconds, the timer pauses automatically.

When activity resumes, the timer continues counting down.

### Example

```text
05:00
04:59
04:58
...
04:52

[10 seconds without keyboard/mouse activity]

04:52  ← timer paused

[mouse movement]

04:52
04:51
04:50
...
```

Inactive time does not reduce the available daily usage time.

---

## Timer Colors

The timer changes color depending on the remaining time.

| Remaining time       | Color           | Meaning                  |
| -------------------- | --------------- | ------------------------ |
| More than 15 minutes | 🟢 Green        | Plenty of time remaining |
| 5–15 minutes         | 🟠 Orange       | Time is running low      |
| Less than 5 minutes  | 🔴 Red          | Critical                 |
| Inactivity pause     | 🔵 Blue         | Timer is paused          |
| `00:00`              | 🔴 Blinking red | Daily limit reached      |

The inactivity color has priority over the normal time-based colors.

For example, if 3 minutes remain and the user becomes inactive, the timer changes from red to blue.

---

## Daily Limit

The daily limit is configured through `settings.txt`.

Default configuration:

```text
limit_minutes=5
```

The value is specified in minutes.

For example:

```text
limit_minutes=60
```

sets the daily limit to one hour.

---

## Parent Password

The parent password is configured in `settings.txt`.

Default:

```text
password=1234
```

When the daily limit reaches `00:00`, TimeLimiter displays a password window.

The user has 60 seconds to enter the correct password.

### Correct Password

If the password is correct:

1. The password window closes.
2. The session is extended by another full daily-limit period.
3. The usage data is updated.
4. The timer resumes.

For example, with:

```text
limit_minutes=30
```

entering the correct password provides another:

```text
30 minutes
```

of available usage time.

### Incorrect Password

An incorrect password does not extend the session.

The user can continue trying while the 60-second timeout is running.

### Password Timeout

If the correct password is not entered within 60 seconds:

```text
shutdown /s /t 0
```

is executed and Windows shuts down immediately.

> **Security note:** The current implementation stores the parent password as plain text in `settings.txt`. This is intentional for the current version and should not be considered secure against a technically experienced user.

---

## Automatic Daily Reset

Usage is reset automatically at midnight.

For example:

```text
date=2026-09-04
used_seconds=270
```

After midnight, TimeLimiter detects the new date and changes the usage to:

```text
date=2026-09-05
used_seconds=0
```

The configured daily limit is then available again.

---

## Configuration

TimeLimiter uses a simple text file:

```text
settings.txt
```

Example:

```text
limit_minutes=5
password=1234
timer_enabled=true
```

### `limit_minutes`

Controls the daily usage limit.

Example:

```text
limit_minutes=60
```

One hour of available usage per day.

### `password`

Parent password used to extend the session.

Example:

```text
password=123456
```

### `timer_enabled`

Controls whether the timer overlay is displayed.

Enable:

```text
timer_enabled=true
```

Disable:

```text
timer_enabled=false
```

When the timer display is disabled, the usage tracking logic still runs.

---

## Application Files

TimeLimiter stores its files in the **same directory as the running application**.

When running from Python:

```text
TimeLimiter/
├── main.py
├── settings.txt
├── usage.txt
├── timelimiter.log
└── requirements.txt
```

When running the compiled executable:

```text
TimeLimiter/
├── TimeLimiter.exe
├── settings.txt
├── usage.txt
└── timelimiter.log
```

This behavior makes the application portable.

If `TimeLimiter.exe` is moved to another directory, its configuration, usage data, and log file are created next to the new executable.

---

## Usage Data

Usage information is stored in:

```text
usage.txt
```

Example:

```text
date=2026-09-04
used_seconds=127
```

### `date`

The date for which the usage data applies.

### `used_seconds`

The number of seconds counted toward the current day's limit.

TimeLimiter saves this information every 10 seconds.

This helps prevent significant loss of usage information if the application or Windows unexpectedly closes.

---

## Logging

Application activity is recorded in:

```text
timelimiter.log
```

The log contains information such as:

* Application startup
* Configuration loading
* Usage loading
* Remaining time
* Keyboard/mouse monitoring startup
* Inactivity detection
* Timer pause
* Timer resume
* Password attempts
* Password timeout
* Daily reset
* Windows shutdown
* Application errors

Example:

```text
2026-09-04 12:00:00 | INFO | TimeLimiter started
2026-09-04 12:00:00 | INFO | Usage loaded: date=2026-09-04, used_seconds=0
2026-09-04 12:00:00 | INFO | Keyboard and mouse activity monitoring started.
2026-09-04 12:00:10 | INFO | User inactive for 10 seconds. Timer paused.
2026-09-04 12:00:15 | INFO | User activity detected. Timer resumed.
```

---

## Inactivity Detection

TimeLimiter uses the `pynput` library to monitor keyboard and mouse activity.

### Keyboard

* Key presses

### Mouse

* Mouse movement
* Mouse clicks
* Mouse scrolling

If no activity is detected for:

```text
10 seconds
```

the usage timer pauses.

The inactivity threshold is controlled by:

```python
INACTIVITY_TIMEOUT = 10
```

in `main.py`.

When the timer is paused because of inactivity:

* The countdown stops.
* No usage time is consumed.
* The timer changes to blue.
* The application continues monitoring for activity.

As soon as keyboard or mouse activity is detected, the timer resumes and returns to its normal time-based color.

---

## Timer Overlay

The timer is displayed as a transparent overlay at the top center of the screen.

Example:

```text
          04:37
```

The window:

* Has no standard Windows border
* Is always on top
* Is horizontally centered
* Uses a transparent background
* Displays the remaining time as `MM:SS`

The timer can be disabled through:

```text
timer_enabled=false
```

---

## Project Structure

The project currently has a simple structure:

```text
TimeLimiter/
│
├── main.py
├── requirements.txt
├── README.md
│
├── settings.txt
├── usage.txt
└── timelimiter.log
```

The following files are generated automatically when the application is first launched:

* `settings.txt`
* `usage.txt`
* `timelimiter.log`

---

## Requirements

### Operating System

* Windows 10
* Windows 11

### Python

Development currently uses Python 3.12.

### Python Dependencies

The project uses:

```text
pynput==1.8.2
pyinstaller==6.22.2
```

`pynput` is required by the application for global keyboard and mouse activity monitoring.

`pyinstaller` is used to build the standalone Windows executable.

---

## Installation for Development

Clone the repository:

```powershell
git clone https://github.com/golgi-complex/TimeLimiter.git
```

Enter the project directory:

```powershell
cd TimeLimiter
```

Create a virtual environment:

```powershell
python -m venv myenv
```

Activate it:

```powershell
.\myenv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## Running from Python

Start the application with:

```powershell
python main.py
```

On the first launch, TimeLimiter automatically creates:

```text
settings.txt
usage.txt
timelimiter.log
```

in the same directory as `main.py`.

---

## Building the Windows Executable

TimeLimiter can be packaged into a standalone `.exe` using PyInstaller.

Build command:

```powershell
pyinstaller --onefile --noconsole --name TimeLimiter main.py
```

After a successful build, the executable will be located at:

```text
dist\TimeLimiter.exe
```

The application does not require Python to be installed on the target computer when using the compiled executable.

---

## Installing the Executable

A recommended installation directory is:

```text
C:\ProgramData\TimeLimiter
```

The final installation can look like:

```text
C:\ProgramData\TimeLimiter\
│
├── TimeLimiter.exe
├── settings.txt
├── usage.txt
└── timelimiter.log
```

Because TimeLimiter stores its files relative to the executable, keeping the executable and configuration files together makes the application easy to manage and move.

---

## Windows Startup

TimeLimiter can be configured to start automatically when Windows starts.

The recommended approach is:

1. Keep the executable here:

```text
C:\ProgramData\TimeLimiter\TimeLimiter.exe
```

2. Create a Windows Startup shortcut pointing to:

```text
C:\ProgramData\TimeLimiter\TimeLimiter.exe
```

3. Place the shortcut in the Windows Startup folder.

For system-wide startup, the Startup folder is:

```text
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

### Important

Do **not** simply move the executable itself into the Startup folder if you want application files to remain in:

```text
C:\ProgramData\TimeLimiter
```

TimeLimiter intentionally stores `settings.txt`, `usage.txt`, and `timelimiter.log` next to the executable.

Therefore, the executable should remain in:

```text
C:\ProgramData\TimeLimiter
```

and the Startup folder should contain a shortcut to it.

---

## Testing

For development and testing, the default limit is intentionally small:

```text
limit_minutes=5
```

This makes it possible to test the complete workflow without waiting for a long period.

### Testing the Inactivity Pause

1. Start TimeLimiter.
2. Do not touch the mouse or keyboard.
3. Wait 10 seconds.
4. The timer should turn blue.
5. The countdown should stop.
6. Move the mouse or press a key.
7. The timer should return to its normal color.
8. The countdown should continue.

### Testing the Daily Limit

For faster testing, temporarily change:

```text
limit_minutes=5
```

to:

```text
limit_minutes=1
```

The timer will count down from:

```text
01:00
```

After reaching:

```text
00:00
```

the password window should appear.

### Testing the Password

Default password:

```text
1234
```

Enter the correct password.

The timer should receive another full session.

For example, when the configured limit is 5 minutes:

```text
05:00
```

### Testing the Password Timeout

When the password window appears, do not enter the password.

After 60 seconds, TimeLimiter executes:

```text
shutdown /s /t 0
```

and Windows shuts down.

> Use this test carefully on a real system. Save your work before testing the shutdown behavior.

---

## Design Decisions

### Active Usage Only

TimeLimiter counts only periods during which the user is actively interacting with the computer.

If there is no keyboard or mouse activity for 10 seconds, the timer stops.

This prevents idle periods from consuming the daily allowance.

### Local Configuration

Configuration is stored in a simple text file instead of the Windows Registry.

Advantages:

* Easy to edit
* Easy to back up
* Easy to inspect
* Portable
* No installer required

### Relative Application Storage

Application files are stored next to the executable.

This avoids hard-coded paths and makes the application portable.

### Simple Architecture

The application intentionally uses a small number of dependencies and relies heavily on Python's standard library.

---

## Security Considerations

TimeLimiter is designed as a **simple parental-control utility**, not as a hardened security product.

The current version does not attempt to protect itself against an experienced Windows user.

For example, it does not currently prevent:

* Terminating the process through Task Manager
* Editing `settings.txt`
* Deleting `usage.txt`
* Modifying the executable
* Booting another operating system
* Running Windows with administrative tools

The application is intentionally kept simple because its primary purpose is to provide a basic time limit for ordinary use.

---

## Known Limitations

* The parent password is stored as plain text.
* The application does not protect its files from manual modification.
* The application does not prevent process termination.
* The application does not provide a graphical settings interface.
* The application does not synchronize usage between multiple computers.
* The application does not provide remote parental management.
* Only keyboard and mouse activity are currently used to determine user activity.
* The inactivity threshold is currently defined in the source code.
* The application is currently Windows-only.

---

## Technology Stack

TimeLimiter is built with:

* **Python 3.12** — application runtime
* **Tkinter** — graphical user interface
* **pynput** — keyboard and mouse monitoring
* **PyInstaller** — Windows executable packaging
* **Windows shutdown command** — automatic system shutdown
* **Python logging** — application logging

---

## Disclaimer

TimeLimiter is provided as-is.

The application directly uses the Windows shutdown command when the password-entry timeout expires. Always test the application in a controlled environment before deploying it on a production computer.
