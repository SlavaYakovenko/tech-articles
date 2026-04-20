I think, guys, that you already know that there is a possibility to connect your Claude Code to other models. For example, it is possible to use the Google Gemma 4 model with your Claude Code instance. This solution can potentially help you save a significant number of tokens and remove the limits imposed by Anthropic. 

This life hack can be achieved with Ollama properly configured on your local host. I believe this solution is already quite popular, with many videos and tutorials available on how to set it up. Therefore, I will not elaborate on the steps required to do so.

After creating the symbiosis of Claude Code, Ollama, and Gemma, you may encounter a situation where Ollama becomes the bottleneck during development. The next step is to address the proper configuration of Ollama locally.

Unfortunately, not everything can be configured in the Olama user interface. phase. And something should be performed on a low level. In this article, you will receive comprehensive instructions on how to configure your Ollama on Mac to achieve better performance in this symbiosis.


Настройка Ollama как производительного сервиса на macOS
Эта инструкция превращает Ollama из обычного приложения в мощный фоновый движок для Claude Code, Gemma 4 и других агентов, обеспечивая параллелизм и мгновенный отклик.

1. Подготовка системы (Очистка)
Перед установкой нового конфига нужно отключить стандартные механизмы запуска, чтобы избежать конфликта «Address already in use».

Отключите фоновую активность: * Зайдите в System Settings → General → Login Items.

В разделе Background Items найдите Ollama и выключите её.

Завершите текущие процессы:

Bash
killall Ollama 2>/dev/null; killall ollama 2>/dev/null
Убедитесь, что порт 11434 свободен:

Bash
lsof -i :11434
Если команда что-то вывела, убейте этот процесс через kill -9 [PID].

2. Создание конфигурации (LaunchAgent)
Использование LaunchAgent под вашим пользователем — это самый надежный способ в 2026 году, так как он имеет доступ к /Applications и вашим личным моделям.

Создайте файл (команда cat исключает ошибки форматирования):

Bash
cat <<EOF > ~/Library/LaunchAgents/ai.ollama.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.ollama</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Applications/Ollama.app/Contents/Resources/ollama</string>
        <string>serve</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_KEEP_ALIVE</key>
        <string>-1</string>
        <key>OLLAMA_NUM_PARALLEL</key>
        <string>4</string>
        <key>OLLAMA_CONTEXT_LENGTH</key>
        <string>65536</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ollama.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ollama.stderr.log</string>
</dict>
</plist>
EOF
3. Активация сервиса
Установите корректные права и зарегистрируйте агент в системе:

Bash
chmod 644 ~/Library/LaunchAgents/ai.ollama.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.ollama.plist
4. Контроль параметров (Check-list)
Параметр	Значение	Зачем это нужно
KEEP_ALIVE	-1	Модели не выгружаются из GPU. Ответ на запрос — мгновенный.
NUM_PARALLEL	4	Позволяет Claude Code одновременно сканировать файлы и вести чат.
CONTEXT_LENGTH	65536	Увеличивает «память» модели для работы с длинными файлами кода.
Проверка статуса:

Bash
launchctl list | grep ai.ollama
(Должен появиться PID в первой колонке).

Проверка активных настроек:

Bash
ps -ww -E -p $(pgrep -f "ollama serve") | grep OLLAMA
5. Обслуживание и обновления
Обновление Ollama: Просто обновите приложение Ollama.app как обычно. Сервис подхватит новый бинарник при следующем запуске системы.

Применение изменений: Если вы изменили .plist, перегрузите его:

Bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.ollama.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.ollama.plist
Удаление лишнего: Мы убедились, что файлы в /Library/LaunchDaemons/ не нужны и только мешают — их стоит удалить.

Теперь ваша конфигурация задокументирована и работает максимально эффективно. Есть ли какие-то технические детали в конфиге, которые вы хотели бы расширить (например, добавить логирование в другое место)?