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
* 🌐 Поддержка английского и русского языков
* ⚙️ Простая текстовая конфигурация
* 📝 Ведение журнала работы приложения
* 🚀 Поддержка автоматического запуска Windows
* 📦 Возможность создания портативного `.exe`
* 🪟 Поддержка Windows 10 и Windows 11

---

## Как работает TimeLimiter

TimeLimiter поддерживает обратный отсчёт, показывающий количество доступного времени работы за компьютером в текущем дне.

Таймер отображается в формате:

```text
HH:MM:SS
```

Например, если установлен дневной лимит:

```text
5 минут
```

таймер начинается со значения:

```text
00:05:00
```

Если установлен лимит:

```text
90 минут
```

таймер начинается со значения:

```text
01:30:00
```

При активном использовании компьютера таймер постепенно уменьшается.

Если в течение 10 секунд не происходит никакой активности клавиатуры или мыши, таймер автоматически приостанавливается.

После возобновления активности отсчёт продолжается.

### Пример

```text
00:05:00
00:04:59
00:04:58
...
00:04:52

[10 секунд без активности клавиатуры/мыши]

00:04:52  ← таймер приостановлен

[движение мыши]

00:04:52
00:04:51
00:04:50
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
| `00:00:00`                        | 🔴 Мигающий красный | Дневной лимит достигнут |

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

Таймер при этом будет отображаться как:

```text
01:00:00
```

Можно устанавливать лимиты продолжительностью более одного часа.

---

## Родительский пароль

Родительский пароль также задаётся в файле `settings.txt`.

Значение по умолчанию:

```text
password=1234
```

Когда дневной лимит достигает:

```text
00:00:00
```

TimeLimiter отображает окно ввода пароля.

На ввод правильного пароля даётся 60 секунд.

Таймер ожидания также отображается в формате:

```text
HH:MM:SS
```

Начальное значение:

```text
00:01:00
```

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
00:30:00
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

## Поддержка языков

TimeLimiter поддерживает два языка интерфейса:

* 🇬🇧 English
* 🇷🇺 Русский

Язык задаётся в файле:

```text
settings.txt
```

Параметр:

```text
language=en
```

или:

```text
language=ru
```

### Английский интерфейс

```text
language=en
```

Пример окна:

```text
Time limit reached

Enter the parent password to continue.

Time remaining: 00:01:00
```

### Русский интерфейс

```text
language=ru
```

Пример окна:

```text
Время вышло

Введите родительский пароль, чтобы продолжить.

Осталось времени: 00:01:00
```

Если параметр `language` отсутствует или содержит неизвестное значение, TimeLimiter использует английский язык по умолчанию.

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
language=en
```

### `limit_minutes`

Определяет ежедневный лимит времени в минутах.

Например:

```text
limit_minutes=60
```

означает один час доступного времени в день.

Таймер будет отображаться как:

```text
01:00:00
```

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

### `language`

Определяет язык интерфейса приложения.

Английский:

```text
language=en
```

Русский:

```text
language=ru
```

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
          00:04:37
```

Формат отображения:

```text
HH:MM:SS
```

Окно таймера:

* не имеет стандартной рамки Windows;
* находится поверх остальных окон;
* располагается по центру экрана;
* имеет прозрачный фон;
* отображает оставшееся время в формате `HH:MM:SS`.

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
00:01:00
```

После достижения:

```text
00:00:00
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
00:05:00
```

### Тестирование таймера ввода пароля

После появления окна пароля не вводите пароль.

Таймер будет отсчитывать:

```text
00:01:00
00:00:59
00:00:58
...
00:00:01
00:00:00
```

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

### Локализация

Текст интерфейса вынесен в отдельную структуру переводов.

Это позволяет добавлять новые языки без изменения основной логики приложения.

В текущей версии поддерживаются:

* English
* Русский

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
* Данные об использовании сохраняются каждые 10 секунд, поэтому при неожиданном завершении приложения возможна небольшая потеря последних секунд.
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

**A simple parental control utility for limiting daily computer usage on Windows 10/11.**

TimeLimiter tracks active computer usage and limits the amount of time a user can spend on the computer each day. When the daily limit is reached, TimeLimiter asks for the parent password to continue the session. If the correct password is not entered within 60 seconds, Windows is automatically shut down.

The application runs in the background and can be configured to start automatically with Windows.

---

## Features

* ⏱️ Daily computer usage limit
* 🖱️⌨️ Automatic pause after 10 seconds of keyboard or mouse inactivity
* 🔐 Parent password protection
* ⏳ Password entry countdown
* 🛑 Automatic Windows shutdown after the password timeout
* 🌙 Automatic daily limit reset at midnight
* 📊 Usage time tracking
* 💾 Usage data saved every 10 seconds
* 🎨 Color-coded remaining time indicator
* 📌 Always-on-top timer overlay
* 🌐 English and Russian language support
* ⚙️ Simple text-based configuration
* 📝 Application logging
* 🚀 Windows startup support
* 📦 Portable `.exe` build
* 🪟 Windows 10 and Windows 11 support

---

## How TimeLimiter Works

TimeLimiter provides a countdown timer showing the amount of available computer usage time remaining for the current day.

The timer is displayed in the following format:

```text
HH:MM:SS
```

For example, if the daily limit is:

```text
5 minutes
```

the timer starts at:

```text
00:05:00
```

If the daily limit is:

```text
90 minutes
```

the timer starts at:

```text
01:30:00
```

The timer decreases while the user is actively using the computer.

If there is no keyboard or mouse activity for 10 seconds, the timer is automatically paused.

The countdown resumes as soon as activity is detected again.

### Example

```text
00:05:00
00:04:59
00:04:58
...
00:04:52

[10 seconds without keyboard/mouse activity]

00:04:52  ← timer paused

[mouse movement]

00:04:52
00:04:51
00:04:50
...
```

Inactive time **does not count toward the daily usage limit**.

---

## Timer Colors

The timer color changes depending on the remaining time.

| Remaining time           | Color           | Meaning                  |
| ------------------------ | --------------- | ------------------------ |
| More than 15 minutes     | 🟢 Green        | Plenty of time remaining |
| 5–15 minutes             | 🟠 Orange       | Time is running low      |
| Less than 5 minutes      | 🔴 Red          | Critical time remaining  |
| Paused due to inactivity | 🔵 Blue         | Timer is paused          |
| `00:00:00`               | 🔴 Blinking red | Daily limit reached      |

The blue inactivity state has priority over the normal time-based colors.

For example, if 3 minutes remain and the user stops using the computer, the timer changes from red to blue.

---

## Daily Time Limit

The daily limit is configured through:

```text
settings.txt
```

The default value is:

```text
limit_minutes=5
```

The value is specified in minutes.

For example:

```text
limit_minutes=60
```

sets the daily limit to one hour.

The timer will then display:

```text
01:00:00
```

Limits longer than one hour are supported.

---

## Parent Password

The parent password is also configured in `settings.txt`.

The default password is:

```text
password=1234
```

When the daily limit reaches:

```text
00:00:00
```

TimeLimiter displays a password entry window.

The parent has 60 seconds to enter the correct password.

The password countdown is also displayed in:

```text
HH:MM:SS
```

The initial value is:

```text
00:01:00
```

### Correct Password

If the correct password is entered:

1. The password window closes.
2. The session is extended by one full daily-limit period.
3. Usage data is updated.
4. The timer continues counting down.

For example, if:

```text
limit_minutes=30
```

the user receives another:

```text
00:30:00
```

of available time after entering the correct password.

### Incorrect Password

An incorrect password does not extend the session.

The user can continue attempting to enter the password until the 60-second countdown expires.

### Password Timeout

If the correct password is not entered within 60 seconds:

```text
shutdown /s /t 0
```

is executed automatically, and Windows is immediately shut down.

> **Security note:** In the current version, the parent password is stored as plain text in `settings.txt`. This is intentional for simplicity in the current version. This storage method does not protect the password from a technically experienced user.

---

## Language Support

TimeLimiter supports two interface languages:

* 🇬🇧 English
* 🇷🇺 Russian

The language is configured in:

```text
settings.txt
```

using the `language` parameter.

English:

```text
language=en
```

Russian:

```text
language=ru
```

### English Interface

```text
language=en
```

Example:

```text
Time limit reached

Enter the parent password to continue.

Time remaining: 00:01:00
```

### Russian Interface

```text
language=ru
```

Example:

```text
Время вышло

Введите родительский пароль, чтобы продолжить.

Осталось времени: 00:01:00
```

If the `language` parameter is missing or contains an unsupported value, TimeLimiter uses English by default.

---

## Automatic Daily Reset

Usage data is automatically reset at the beginning of a new day.

For example:

```text
date=2026-09-04
used_seconds=270
```

After midnight, TimeLimiter detects the date change and resets the data to:

```text
date=2026-09-05
used_seconds=0
```

The full daily limit then becomes available again.

---

## Configuration

TimeLimiter uses a simple text configuration file:

```text
settings.txt
```

Example:

```text
limit_minutes=5
password=1234
timer_enabled=true
language=en
```

### `limit_minutes`

Defines the daily usage limit in minutes.

For example:

```text
limit_minutes=60
```

means one hour of available computer usage per day.

The timer will display:

```text
01:00:00
```

### `password`

The parent password required to extend the session.

Example:

```text
password=123456
```

### `timer_enabled`

Controls whether the timer is displayed on the screen.

Enable:

```text
timer_enabled=true
```

Disable:

```text
timer_enabled=false
```

When the timer display is disabled, usage tracking continues to work in the background.

### `language`

Defines the application interface language.

English:

```text
language=en
```

Russian:

```text
language=ru
```

---

## Application Files

TimeLimiter stores its files **in the same directory as the running application**.

When running through Python:

```text
TimeLimiter/
├── main.py
├── settings.txt
├── usage.txt
├── timelimiter.log
└── requirements.txt
```

When running as a compiled `.exe`:

```text
TimeLimiter/
├── TimeLimiter.exe
├── settings.txt
├── usage.txt
└── timelimiter.log
```

This approach makes the application portable.

If `TimeLimiter.exe` is moved to another directory, the configuration, usage and log files will be created next to the new `.exe` location.

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

The date associated with the usage data.

### `used_seconds`

The number of seconds counted as active usage during the current day.

TimeLimiter saves usage data every 10 seconds.

This minimizes potential data loss if the application or Windows is unexpectedly terminated.

---

## Logging

Application activity is recorded in:

```text
timelimiter.log
```

The log may contain information about:

* application startup;
* configuration loading;
* usage data loading;
* remaining time;
* keyboard and mouse monitoring;
* inactivity detection;
* timer pause;
* timer resume;
* password attempts;
* password timeout;
* daily limit reset;
* Windows shutdown;
* application errors.

Example:

```text
2026-09-04 12:00:00 | INFO | TimeLimiter started
2026-09-04 12:00:00 | INFO | Usage loaded: date=2026-09-04, used_seconds=0
2026-09-04 12:00:00 | INFO | Keyboard and mouse activity monitoring started.
2026-09-04 12:00:10 | INFO | User inactive for 10 seconds. Timer paused.
2026-09-04 12:00:15 | INFO | User activity detected. Timer resumed.
```

---

## Activity Detection

TimeLimiter uses the `pynput` library to monitor keyboard and mouse activity.

### Keyboard

The application monitors:

* key presses.

### Mouse

The application monitors:

* mouse movement;
* mouse button clicks;
* mouse wheel scrolling.

If no activity is detected for:

```text
10 seconds
```

the usage timer is paused.

The inactivity threshold is defined in `main.py`:

```python
INACTIVITY_TIMEOUT = 10
```

When the timer is paused because of inactivity:

* the countdown stops;
* usage time is not consumed;
* the timer turns blue;
* the application continues monitoring user activity.

As soon as mouse movement or a key press is detected, the timer resumes and returns to the normal color indicator.

---

## On-Screen Timer

The timer is displayed as a transparent overlay at the top center of the screen.

Example:

```text
          00:04:37
```

The timer uses the:

```text
HH:MM:SS
```

format.

The timer window:

* has no standard Windows window frame;
* stays above other windows;
* is centered horizontally;
* has a transparent background;
* displays the remaining time in `HH:MM:SS` format.

The timer display can be disabled using:

```text
timer_enabled=false
```

---

## Project Structure

The project has a simple structure:

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

The following files are automatically created on the first application launch:

* `settings.txt`
* `usage.txt`
* `timelimiter.log`

---

## Requirements

### Operating System

* Windows 10
* Windows 11

### Python

Python 3.12 is used for development.

### Python Dependencies

The project uses:

```text
pynput==1.8.2
pyinstaller==6.22.2
```

`pynput` is used for global keyboard and mouse activity monitoring.

`pyinstaller` is used to create a standalone Windows executable.

---

## Development Installation

Clone the repository:

```powershell
git clone https://github.com/golgi-complex/TimeLimiter.git
```

Navigate to the project directory:

```powershell
cd TimeLimiter
```

Create a virtual environment:

```powershell
python -m venv myenv
```

Activate the virtual environment:

```powershell
.\myenv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

---

## Running with Python

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

## Building the Windows `.exe`

TimeLimiter can be packaged as a standalone `.exe` using PyInstaller.

Build command:

```powershell
pyinstaller --onefile --noconsole --name TimeLimiter main.py
```

After a successful build, the executable will be located at:

```text
dist\TimeLimiter.exe
```

Python is not required on the target computer when using the compiled executable.

---

## Installing the Executable

The recommended installation directory is:

```text
C:\ProgramData\TimeLimiter
```

The final structure may look like:

```text
C:\ProgramData\TimeLimiter\
│
├── TimeLimiter.exe
├── settings.txt
├── usage.txt
└── timelimiter.log
```

Because TimeLimiter stores its files relative to the executable location, keeping the `.exe` and configuration files in the same directory makes the application easier to manage and move.

---

## Windows Startup

TimeLimiter can be configured to start automatically with Windows.

The recommended approach is:

1. Keep the executable here:

```text
C:\ProgramData\TimeLimiter\TimeLimiter.exe
```

2. Create a Windows shortcut pointing to:

```text
C:\ProgramData\TimeLimiter\TimeLimiter.exe
```

3. Place the shortcut in the Windows Startup folder.

The system-wide Startup folder is:

```text
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

### Important

**It is not recommended to place `TimeLimiter.exe` directly inside the Startup folder** if you want the application's files to remain in:

```text
C:\ProgramData\TimeLimiter
```

TimeLimiter intentionally stores:

```text
settings.txt
usage.txt
timelimiter.log
```

next to the executable.

Therefore, the `.exe` should remain here:

```text
C:\ProgramData\TimeLimiter
```

while the Startup folder should contain a **shortcut** pointing to the executable.

---

## Testing

For development and testing, the default limit is intentionally small:

```text
limit_minutes=5
```

This makes it possible to test the application quickly.

### Testing the Inactivity Pause

1. Start TimeLimiter.
2. Do not move the mouse or press any keys.
3. Wait 10 seconds.
4. The timer should turn blue.
5. The countdown should stop.
6. Move the mouse or press a key.
7. The timer should return to its normal color.
8. The countdown should resume.

### Testing the Daily Limit

For faster testing, temporarily change:

```text
limit_minutes=5
```

to:

```text
limit_minutes=1
```

The timer will start at:

```text
00:01:00
```

When it reaches:

```text
00:00:00
```

the password entry window should appear.

### Testing the Password

The default password is:

```text
1234
```

Enter the correct password.

The timer should receive another full usage period.

For example, with a 5-minute limit:

```text
00:05:00
```

### Testing the Password Countdown

After the password window appears, do not enter a password.

The countdown will proceed:

```text
00:01:00
00:00:59
00:00:58
...
00:00:01
00:00:00
```

After 60 seconds, TimeLimiter will execute:

```text
shutdown /s /t 0
```

and Windows will shut down.

> Be careful when testing this feature on a real computer. Save all important work before testing.

---

## Architectural Decisions

### Active Usage Only

TimeLimiter counts only periods when the user actively interacts with the computer.

If there is no keyboard or mouse activity for 10 seconds, the timer pauses.

This prevents the daily limit from being consumed while the computer is idle.

### Local Configuration

Configuration is stored in a plain text file instead of the Windows Registry.

Advantages:

* simple editing;
* easy backup;
* easy inspection;
* portability;
* no installer required.

### Files Stored Next to the Application

Application files are stored next to the executable.

This avoids hard-coded paths and makes the application portable.

### Simple Architecture

The application intentionally uses a small number of dependencies and relies on the Python standard library whenever possible.

### Localization

Interface strings are stored separately from the main application logic.

This makes it possible to add additional languages without modifying the core functionality.

The current version supports:

* English
* Russian

---

## Security

TimeLimiter is designed as a **simple parental control utility**, not as a hardened security system.

The current version does not attempt to protect the application against a technically experienced user.

For example, it does not prevent:

* terminating the process through Task Manager;
* editing `settings.txt`;
* deleting `usage.txt`;
* modifying the executable;
* booting another operating system;
* using Windows administrative tools.

The application is intentionally kept simple because its primary purpose is to provide a basic usage-time restriction for normal everyday computer use.

---

## Known Limitations

* The parent password is stored as plain text.
* Application files are not protected from manual modification.
* The process can be terminated through Task Manager.
* There is no graphical settings interface.
* Usage data is not synchronized between multiple computers.
* There is no remote parental management.
* Only keyboard and mouse activity are currently monitored.
* The inactivity threshold is currently defined directly in the source code.
* Usage data is saved every 10 seconds, so a small amount of recent usage data may be lost if the application or Windows is unexpectedly terminated.
* The application currently works only on Windows.

---

## Technology Stack

TimeLimiter uses:

* **Python 3.12** — main programming language and runtime
* **Tkinter** — graphical user interface
* **pynput** — keyboard and mouse monitoring
* **PyInstaller** — Windows `.exe` packaging
* **Windows shutdown command** — automatic system shutdown
* **Python logging** — application logging

---

## Disclaimer

TimeLimiter is provided **as is**.

When the password-entry timeout expires, the application directly executes the Windows shutdown command. Test the application carefully in a controlled environment before using it on a production or shared computer.
