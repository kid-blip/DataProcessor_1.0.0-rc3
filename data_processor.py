import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time
import hashlib
import datetime
import threading
import queue
import sys # Добавлено для PyInstaller

# --- Константы приложения ---
APP_VERSION = "1.0.0-rc3" # Обновляем версию
CONFIG_FILE = 'config.json'
MONITORING_LOG_FILE = 'monitoring_log.txt'

# --- Словарь для многоязычной поддержки ---
LOCALIZED_TEXTS = {
    "ru": {
        "welcome_message": "Приветствуем в Data Processor v{}!\nЭта программа предназначена для анализа и генерации отчетов по данным из различных источников: CSV-файлов, текстовых логов и веб-страниц. Выберите язык и начните работу!",
        "app_title": "Data Processor",
        "menu_monitor_url": "Мониторинг URL",
        "menu_csv_analysis": "Анализ CSV файла",
        "menu_text_log_analysis": "Анализ текстового лога",
        "menu_web_page_analysis": "Анализ веб-страницы",
        "menu_settings": "Настройки",
        "menu_exit": "Выход",
        "config_loaded_success": "Конфигурация успешно загружена из {}.",
        "config_not_found": "Файл конфигурации '{}' не найден. Использование настроек по умолчанию.",
        "config_read_error": "Ошибка чтения файла конфигурации '{}': {}. Использование настроек по умолчанию.",
        "config_unexpected_error_load": "Произошла непредвиденная ошибка при загрузке конфигурации: {}. Использование настроек по умолчанию.",
        "language_set": "Язык установлен на {}.",
        "current_language": "Текущий язык: {}",
        "select_language_gui": "Выберите язык:",
        "save_config_button": "Сохранить настройки",
        "config_saved_success": "Конфигурация успешно сохранена в {}.",
        "config_save_error": "Ошибка при сохранении конфигурации в {}: {}.",
        "config_unexpected_error_save": "Произошла непредвиденная ошибка при сохранении конфигурации: {}.",
        "dir_created_success": "Создана директория для отчетов: {}.",
        "dir_create_error": "Ошибка при создании директории для отчетов '{}': {}.",
        "error_dialog_title": "Ошибка",
        "info_dialog_title": "Информация",
        "monitoring_start": "Запуск мониторинга URL: {}",
        "monitoring_stop_button": "Остановить мониторинг",
        "monitoring_url_label": "URL для мониторинга:",
        "monitoring_interval_label": "Интервал (сек, по умолчанию 300):",
        "start_monitoring_button": "Начать мониторинг",
        "invalid_url": "Пожалуйста, введите корректный URL.",
        "invalid_interval": "Неверный интервал. Используется значение по умолчанию (300 секунд).",
        "initial_fetch": "Инициализация: получение содержимого {}...",
        "no_content_for_monitoring": "Не удалось получить содержимое для мониторинга URL: {}. Мониторинг остановлен.",
        "no_changes": "{} - Без изменений (Последняя проверка: {})",
        "changes_detected": "!!! ИЗМЕНЕНИЯ ОБНАРУЖЕНЫ на {} !!! (Время: {})",
        "monitoring_log_entry": "[{}] Изменения обнаружены на URL: {}",
        "monitoring_stopped": "Мониторинг остановлен.",
        "prompt_monitoring_url": "Введите URL для мониторинга: ",
        "prompt_monitoring_interval": "Введите интервал проверки в секундах (по умолчанию 300 - 5 минут): ",
        "error_url_empty": "Это поле обязательно! Пожалуйста, введите URL.",
        "error_invalid_or_unavailable_url": "Этот адрес неправильный или недоступен, попробуйте еще раз. Ошибка: {}",
        "prompt_save_url": "Сохранить этот URL как последний использованный? (да/нет): ",
        "url_saved_success": "URL успешно сохранен как последний использованный.",
        "url_not_saved": "URL не сохранен.",
        "using_last_saved_url": "Используем последний сохраненный URL: {}",
        "yes_option": "да",
        "no_option": "нет",
        "select_file": "Выберите файл",
        "process_file_button": "Обработать файл",
        "select_csv_file": "Выберите CSV файл",
        "select_text_file": "Выберите текстовый файл",
        "enter_tag_name": "Введите имя HTML-тега (например, 'a', 'p', 'h1'):",
        "process_web_page_button": "Обработать веб-страницу",
        "report_saved_text": "Отчет успешно сохранен в текстовый файл: {}.",
        "report_save_text_error": "Ошибка при сохранении отчета в текстовый файл {}: {}.",
        "report_saved_md": "Отчет успешно сохранен в Markdown-файл: {}.",
        "report_save_md_error": "Ошибка при сохранении отчета в Markdown-файл {}: {}.",
        "data_saved_json": "Данные успешно сохранены в JSON-файл: {}.",
        "data_save_json_error": "Ошибка при сохранении данных в JSON-файл {}: {}.",
        "prompt_save_report": "Сохранить отчет?",
        "prompt_report_filename": "Введите имя файла для отчета (без расширения): ",
        "prompt_report_format": "Выберите формат файла (txt/md): ",
        "invalid_report_format": "Неверный формат. Используется txt.",
        "report_not_saved": "Отчет не сохранен.",
        "csv_read_success": "Успешно прочитаны данные из CSV-файла: {}.",
        "csv_file_not_found": "Ошибка: CSV-файл не найден по пути: {}.",
        "csv_read_error": "Произошла ошибка при чтении CSV-файла: {}.",
        "csv_no_data": "Отчет по CSV: Данные не найдены.",
        "csv_summary_generated": "Сводка по CSV данным успешно сгенерирована.",
        "csv_total_records": "Всего записей: {}",
        "csv_headers": "Заголовки столбцов: {}",
        "csv_example_records": "Пример первых 3-х записей:",
        "csv_report_header": "--- Отчет по CSV данным ---",
        "csv_filter_applying": "Применяем фильтр к CSV: {} {} {}.",
        "csv_filter_count": "Отфильтровано CSV записей: {}.",
        "csv_unknown_operator": "Предупреждение: Неизвестный оператор фильтрации для CSV: {}.",
        "text_read_success": "Успешно прочитаны данные из текстового файла: {}.",
        "text_file_not_found": "Ошибка: Текстовый файл не найден по пути: {}.",
        "text_read_error": "Произошла ошибка при чтении текстового файла: {}.",
        "text_no_data": "Отчет по текстовому логу: Данные не найдены.",
        "text_summary_generated": "Сводка по текстовому логу успешно сгенерирована.",
        "text_total_lines": "Всего строк: {}",
        "text_example_first_lines": "Пример первых 5-ти строк:",
        "text_example_last_lines": "Пример последних 5-ти строк:",
        "text_report_header": "--- Отчет по текстовому логу ---",
        "text_filter_keyword_applying": "Применяем фильтр к логу по ключевому слову: '{}'.",
        "text_filter_regex_applying": "Применяем фильтр к логу по регулярному выражению: '{}'.",
        "text_filter_regex_error": "Ошибка в регулярном выражении '{}': {}.",
        "text_filter_no_criteria": "Предупреждение: Не задан ни ключевое слово, ни регулярное выражение для фильтрации лога.",
        "text_filter_count": "Отфильтровано строк лога: {}.",
        "web_fetch_success": "Успешно скачан контент с URL: {}.",
        "web_fetch_error": "Ошибка при скачивании веб-страницы с {}: {}.",
        "web_parse_full_text_success": "Успешно извлечен текст из HTML-контента.",
        "web_parse_error": "Ошибка при парсинге HTML-контента: {}.",
        "web_parse_elements_warning": "Предупреждение: HTML-контент пуст для парсинга '{}'.",
        "web_parse_elements_success": "Успешно извлечены элементы <{}> из HTML-контента.",
        "web_parse_elements_error": "Ошибка при парсинге HTML-контента для тега '{}': {}.",
        "web_summary_generated": "Сводка по веб-странице успешно сгенерирована.",
        "web_report_header": "--- Отчет по веб-странице ---",
        "web_total_length": "Длина всего текста (символов): {}",
        "web_first_chars": "Первые {} символов текста:",
        "web_no_text_content": "Текстовое содержимое не найдено.",
        "web_extracted_elements_header": "\nИзвлеченные элементы:",
        "web_tag_count": "  <{}> (количество: {}):",
        "web_tag_not_found": "  <{}>: Не найдено.",
        "web_and_more": "    (и еще...)",
        "invalid_language": "Неверный код языка. Доступные языки: {}. Использование текущего языка: {}.",
    },
    "en": {
        "welcome_message": "Welcome to Data Processor v{}!\nThis program is designed to analyze and generate reports from various data sources: CSV files, text logs, and web pages. Select your language and get started!",
        "app_title": "Data Processor",
        "menu_monitor_url": "Monitor URL",
        "menu_csv_analysis": "CSV File Analysis",
        "menu_text_log_analysis": "Text Log Analysis",
        "menu_web_page_analysis": "Web Page Analysis",
        "menu_settings": "Settings",
        "menu_exit": "Exit",
        "config_loaded_success": "Configuration successfully loaded from {}.",
        "config_not_found": "Configuration file '{}' not found. Using default settings.",
        "config_read_error": "Error reading configuration file '{}': {}. Using default settings.",
        "config_unexpected_error_load": "An unexpected error occurred while loading configuration: {}. Using default settings.",
        "language_set": "Language set to {}.",
        "current_language": "Current language: {}",
        "select_language_gui": "Select language:",
        "save_config_button": "Save Settings",
        "config_saved_success": "Configuration successfully saved to {}.",
        "config_save_error": "Error saving configuration to {}: {}.",
        "config_unexpected_error_save": "An unexpected error occurred while saving configuration: {}.",
        "dir_created_success": "Report directory created: {}.",
        "dir_create_error": "Error creating report directory '{}': {}.",
        "error_dialog_title": "Error",
        "info_dialog_title": "Information",
        "monitoring_start": "Starting URL monitoring: {}",
        "monitoring_stop_button": "Stop Monitoring",
        "monitoring_url_label": "URL to monitor:",
        "monitoring_interval_label": "Interval (sec, default 300):",
        "start_monitoring_button": "Start Monitoring",
        "invalid_url": "Please enter a valid URL.",
        "invalid_interval": "Invalid interval. Using default (300 seconds).",
        "initial_fetch": "Initialization: Fetching content of {}...",
        "no_content_for_monitoring": "Failed to get content for monitoring URL: {}. Monitoring stopped.",
        "no_changes": "{} - No changes (Last check: {})",
        "changes_detected": "!!! CHANGES DETECTED on {} !!! (Time: {})",
        "monitoring_log_entry": "[{}] Changes detected on URL: {}",
        "monitoring_stopped": "Monitoring stopped.",
        "prompt_monitoring_url": "Enter URL to monitor: ",
        "prompt_monitoring_interval": "Enter check interval in seconds (default 300 - 5 minutes): ",
        "error_url_empty": "This field is required! Please enter a URL.",
        "error_invalid_or_unavailable_url": "This URL is invalid or unavailable, please try again. Error: {}",
        "prompt_save_url": "Save this URL as last used? (yes/no): ",
        "url_saved_success": "URL successfully saved as last used.",
        "url_not_saved": "URL not saved.",
        "using_last_saved_url": "Using last saved URL: {}",
        "yes_option": "yes",
        "no_option": "no",
        "select_file": "Select File",
        "process_file_button": "Process File",
        "select_csv_file": "Select CSV File",
        "select_text_file": "Select Text File",
        "enter_tag_name": "Enter HTML tag name (e.g., 'a', 'p', 'h1'):",
        "process_web_page_button": "Process Web Page",
        "report_saved_text": "Report successfully saved to text file: {}.",
        "report_save_text_error": "Error saving report to text file {}: {}.",
        "report_saved_md": "Report successfully saved to Markdown file: {}.",
        "report_save_md_error": "Error saving report to Markdown file {}: {}.",
        "data_saved_json": "Data successfully saved to JSON file: {}.",
        "data_save_json_error": "Error saving data to JSON file {}: {}.",
        "prompt_save_report": "Save report?",
        "prompt_report_filename": "Enter report filename (without extension): ",
        "prompt_report_format": "Choose file format (txt/md): ",
        "invalid_report_format": "Invalid format. Using txt.",
        "report_not_saved": "Report not saved.",
        "csv_read_success": "Successfully read data from CSV file: {}.",
        "csv_file_not_found": "Error: CSV file not found at path: {}.",
        "csv_read_error": "An error occurred while reading the CSV file: {}.",
        "csv_no_data": "CSV Report: No data found.",
        "csv_summary_generated": "CSV data summary successfully generated.",
        "csv_total_records": "Total records: {}",
        "csv_headers": "Column Headers: {}",
        "csv_example_records": "Example first 3 records:",
        "csv_report_header": "--- CSV Data Report ---",
        "csv_filter_applying": "Applying CSV filter: {} {} {}.",
        "csv_filter_count": "Filtered CSV records: {}.",
        "csv_unknown_operator": "Warning: Unknown CSV filter operator: {}.",
        "text_read_success": "Successfully read data from text file: {}.",
        "text_file_not_found": "Error: Text file not found at path: {}.",
        "text_read_error": "An error occurred while reading the text file: {}.",
        "text_no_data": "Text Log Report: No data found.",
        "text_summary_generated": "Text log summary successfully generated.",
        "text_total_lines": "Total lines: {}",
        "text_example_first_lines": "Example first 5 lines:",
        "text_example_last_lines": "Example last 5 lines:",
        "text_report_header": "--- Text Log Report ---",
        "text_filter_keyword_applying": "Applying log filter by keyword: '{}'.",
        "text_filter_regex_applying": "Applying log filter by regex: '{}'.",
        "text_filter_regex_error": "Error in regular expression '{}': {}.",
        "text_filter_no_criteria": "Warning: No keyword or regex pattern specified for log filtering.",
        "text_filter_count": "Filtered log lines: {}.",
        "web_fetch_success": "Successfully fetched content from URL: {}.",
        "web_fetch_error": "Error fetching web page from {}: {}.",
        "web_parse_full_text_success": "Successfully extracted text from HTML content.",
        "web_parse_error": "Error parsing HTML content: {}.",
        "web_parse_elements_warning": "Warning: HTML content is empty for parsing '{}'.",
        "web_parse_elements_success": "Successfully extracted <{}> elements from HTML content.",
        "web_parse_elements_error": "Error parsing HTML content for tag '{}': {}.",
        "web_summary_generated": "Web page summary successfully generated.",
        "web_report_header": "--- Web Page Report ---",
        "web_total_length": "Total text length (characters): {}",
        "web_first_chars": "First {} characters of text:",
        "web_no_text_content": "Text content not found.",
        "web_extracted_elements_header": "\nExtracted elements:",
        "web_tag_count": "  <{}> (count: {}):",
        "web_tag_not_found": "  <{}>: Not found.",
        "web_and_more": "    (and more...)",
        "invalid_language": "Invalid language code. Available languages: {}. Using current language: {}.",
    },
    "es": {
        "welcome_message": "¡Bienvenido a Data Processor v{}!\nEste programa está diseñado para analizar y generar informes a partir de diversas fuentes de datos: archivos CSV, registros de texto y páginas web. ¡Seleccione su idioma y comience!",
        "app_title": "Procesador de Datos",
        "menu_monitor_url": "Monitorear URL",
        "menu_csv_analysis": "Análisis de Archivo CSV",
        "menu_text_log_analysis": "Análisis de Registro de Texto",
        "menu_web_page_analysis": "Análisis de Página Web",
        "menu_settings": "Configuración",
        "menu_exit": "Salir",
        "config_loaded_success": "Configuración cargada exitosamente desde {}.",
        "config_not_found": "Archivo de configuración '{}' no encontrado. Usando configuración predeterminada.",
        "config_read_error": "Error al leer el archivo de configuración '{}': {}. Usando configuración predeterminada.",
        "config_unexpected_error_load": "Ocurrió un error inesperado al cargar la configuración: {}. Usando configuración predeterminada.",
        "language_set": "Idioma establecido en {}.",
        "current_language": "Idioma actual: {}",
        "select_language_gui": "Seleccionar idioma:",
        "save_config_button": "Guardar Configuración",
        "config_saved_success": "Configuración guardada exitosamente en {}.",
        "config_save_error": "Error al guardar la configuración en {}: {}.",
        "config_unexpected_error_save": "Ocurrió un error inesperado al guardar la configuración: {}.",
        "dir_created_success": "Directorio de informes creado: {}.",
        "dir_create_error": "Error al crear el directorio de informes '{}': {}.",
        "error_dialog_title": "Error",
        "info_dialog_title": "Información",
        "monitoring_start": "Iniciando monitoreo de URL: {}",
        "monitoring_stop_button": "Detener Monitoreo",
        "monitoring_url_label": "URL a monitorear:",
        "monitoring_interval_label": "Intervalo (seg, predeterminado 300):",
        "start_monitoring_button": "Iniciar monitoreo",
        "invalid_url": "Por favor, introduzca una URL válida.",
        "invalid_interval": "Intervalo inválido. Usando el valor predeterminado (300 segundos).",
        "initial_fetch": "Inicialización: Obteniendo contenido de {}...",
        "no_content_for_monitoring": "No se pudo obtener contenido para la URL de monitoreo: {}. Monitoreo detenido.",
        "no_changes": "{} - Sin cambios (Última verificación: {})",
        "changes_detected": "!!! CAMBIOS DETECTADOS en {} !!! (Hora: {})",
        "monitoring_log_entry": "[{}] Cambios detectados en la URL: {}",
        "monitoring_stopped": "Monitoreo detenido.",
        "prompt_monitoring_url": "Ingrese la URL a monitorear: ",
        "prompt_monitoring_interval": "Ingrese el intervalo de verificación en segundos (predeterminado 300 - 5 minutos): ",
        "error_url_empty": "¡Este campo es obligatorio! Por favor, ingrese una URL.",
        "error_invalid_or_unavailable_url": "Esta URL es inválida o no está disponible, inténtelo de nuevo. Error: {}",
        "prompt_save_url": "¿Guardar esta URL como la última utilizada? (sí/no): ",
        "url_saved_success": "URL guardada exitosamente como última utilizada.",
        "url_not_saved": "URL no guardada.",
        "using_last_saved_url": "Usando la última URL guardada: {}",
        "yes_option": "si",
        "no_option": "no",
        "select_file": "Seleccionar Archivo",
        "process_file_button": "Procesar Archivo",
        "select_csv_file": "Seleccionar Archivo CSV",
        "select_text_file": "Seleccionar Archivo de Texto",
        "enter_tag_name": "Ingrese el nombre de la etiqueta HTML (ej., 'a', 'p', 'h1'):",
        "process_web_page_button": "Procesar Página Web",
        "report_saved_text": "Informe guardado exitosamente en archivo de texto: {}.",
        "report_save_text_error": "Error al guardar el informe en archivo de texto {}: {}.",
        "report_saved_md": "Informe guardado exitosamente en archivo Markdown: {}.",
        "report_save_md_error": "Error al guardar el informe en archivo Markdown {}: {}.",
        "data_saved_json": "Datos guardados exitosamente en archivo JSON: {}.",
        "data_save_json_error": "Error al guardar datos en archivo JSON {}: {}.",
        "prompt_save_report": "¿Guardar informe?",
        "prompt_report_filename": "Ingrese el nombre de archivo del informe (sin extensión): ",
        "prompt_report_format": "Elija el formato de archivo (txt/md): ",
        "invalid_report_format": "Formato inválido. Usando txt.",
        "report_not_saved": "Informe no guardado.",
        "csv_read_success": "Datos leídos exitosamente del archivo CSV: {}.",
        "csv_file_not_found": "Error: Archivo CSV no encontrado en la ruta: {}.",
        "csv_read_error": "Ocurrió un error al leer el archivo CSV: {}.",
        "csv_no_data": "Informe CSV: No se encontraron datos.",
        "csv_summary_generated": "Resumen de datos CSV generado exitosamente.",
        "csv_total_records": "Registros totales: {}",
        "csv_headers": "Encabezados de columna: {}",
        "csv_example_records": "Primeros 3 registros de ejemplo:",
        "csv_report_header": "--- Informe de Datos CSV ---",
        "csv_filter_applying": "Aplicando filtro CSV: {} {} {}.",
        "csv_filter_count": "Registros CSV filtrados: {}.",
        "csv_unknown_operator": "Advertencia: Operador de filtro CSV desconocido: {}.",
        "text_read_success": "Datos leídos exitosamente del archivo de texto: {}.",
        "text_file_not_found": "Error: Archivo de texto no encontrado en la ruta: {}.",
        "text_read_error": "Ocurrió un error al leer el archivo de texto: {}.",
        "text_no_data": "Informe de Registro de Texto: No se encontraron datos.",
        "text_summary_generated": "Resumen de registro de texto generado exitosamente.",
        "text_total_lines": "Líneas totales: {}",
        "text_example_first_lines": "Primeras 5 líneas de ejemplo:",
        "text_example_last_lines": "Últimas 5 líneas de ejemplo:",
        "text_report_header": "--- Informe de Registro de Texto ---",
        "text_filter_keyword_applying": "Aplicando filtro de registro por palabra clave: '{}'.",
        "text_filter_regex_applying": "Aplicando filtro de registro por regex: '{}'.",
        "text_filter_regex_error": "Error en la expresión regular '{}': {}.",
        "text_filter_no_criteria": "Advertencia: No se especificó ninguna palabra clave o patrón regex para el filtrado del registro.",
        "text_filter_count": "Líneas de registro filtradas: {}.",
        "web_fetch_success": "Contenido obtenido exitosamente de la URL: {}.",
        "web_fetch_error": "Error al obtener la página web de {}: {}.",
        "web_parse_full_text_success": "Texto extraído exitosamente del contenido HTML.",
        "web_parse_error": "Error al analizar el contenido HTML: {}.",
        "web_parse_elements_warning": "Advertencia: El contenido HTML está vacío para analizar '{}'.",
        "web_parse_elements_success": "Elementos <{}> extraídos exitosamente del contenido HTML.",
        "web_parse_elements_error": "Error al analizar el contenido HTML para la etiqueta '{}': {}.",
        "web_summary_generated": "Resumen de página web generado exitosamente.",
        "web_report_header": "--- Informe de Página Web ---",
        "web_total_length": "Longitud total del texto (caracteres): {}",
        "web_first_chars": "Primeros {} caracteres del texto:",
        "web_no_text_content": "No se encontró contenido de texto.",
        "web_extracted_elements_header": "\nElementos extraídos:",
        "web_tag_count": "  <{}> (cantidad: {}):",
        "web_tag_not_found": "  <{}>: No encontrado.",
        "web_and_more": "    (y más...)",
        "invalid_language": "Código de idioma no válido. Idiomas disponibles: {}. Usando el idioma actual: {}.",
    }
}

current_language = "ru" # Инициализация

def set_language(lang_code):
    """Устанавливает текущий язык для вывода сообщений."""
    global current_language
    global app_config # Доступ к app_config для списка языков
    if lang_code in LOCALIZED_TEXTS:
        current_language = lang_code
        messagebox.showinfo(get_localized_text("info_dialog_title"), get_localized_text("language_set", lang_code.upper()))
    else:
        available_langs = ", ".join(app_config.get("available_languages", ["ru", "en", "es"]))
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("invalid_language", available_langs, current_language.upper()))


def get_localized_text(key, *args):
    """
    Возвращает локализованный текст по ключу.
    Использует current_language. Если перевод для текущего языка отсутствует,
    пробует получить из 'en'. Если и там нет, возвращает заглушку.
    """
    text = LOCALIZED_TEXTS.get(current_language, {}).get(key)

    if text is None:
        text = LOCALIZED_TEXTS.get("en", {}).get(key, f"MISSING_TRANSLATION_FOR_KEY: {key}")

    return text.format(*args)

# --- Функции для работы с файлом конфигурации ---
app_config = {}

def load_config():
    """
    Загружает настройки из файла config.json.
    Если файл не найден или некорректен, возвращает настройки по умолчанию.
    """
    default_config = {
        "default_language": "en",
        "available_languages": ["ru", "en", "es"],
        "last_used_urls": {
            "web_page_example": "",
            "another_web_example": "https://example.com"
        },
        "example_file_paths": {
            "csv_file": "example.csv",
            "text_log_file": "example.txt",
            "json_input_file": "input_data.json"
        },
        "output_directory": "reports/"
    }
    # Определяем базовую директорию для исполняемого файла
    # Это важно для PyInstaller, чтобы config.json был найден рядом с exe
    if getattr(sys, 'frozen', False):
        # Если приложение заморожено (PyInstaller)
        # sys._MEIPASS - это временная директория, куда PyInstaller распаковывает данные
        base_dir = sys._MEIPASS
    else:
        # Если запущено как обычный Python скрипт
        base_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(base_dir, CONFIG_FILE)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # Убеждаемся, что все ключи из default_config присутствуют
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
                elif isinstance(value, dict) and isinstance(config[key], dict):
                    # Если это словарь, проверяем вложенные ключи
                    for sub_key, sub_value in value.items():
                        if sub_key not in config[key]:
                            config[key][sub_key] = sub_value
        print(get_localized_text("config_loaded_success", config_path))
        return config
    except FileNotFoundError:
        print(get_localized_text("config_not_found", config_path))
        return default_config
    except json.JSONDecodeError as e:
        print(get_localized_text("config_read_error", config_path, e))
        return default_config
    except Exception as e:
        print(get_localized_text("config_unexpected_error_load", e))
        return default_config

def save_config(config):
    """
    Сохраняет текущие настройки в файл config.json.
    """
    # Определяем базовую директорию для сохранения config.json
    # При запуске из exe, config.json должен сохраняться рядом с exe, а не во временной папке MEIPASS
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(base_dir, CONFIG_FILE)

    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        messagebox.showinfo(get_localized_text("info_dialog_title"), get_localized_text("config_saved_success", config_path))
    except IOError as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("config_save_error", config_path, e))
    except Exception as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("config_unexpected_error_save", e))

def ensure_output_directory_exists(config):
    """
    Проверяет существование директории для отчетов, указанной в конфиге, и создает ее, если нужно.
    При запуске из EXE, директория будет создана рядом с EXE.
    """
    output_dir = config.get("output_directory", "reports/")
    
    # Определяем путь для папки отчетов.
    # Если это относительный путь, он будет относительным к месту запуска EXE.
    if getattr(sys, 'frozen', False):
        # Если output_dir - относительный путь, делаем его относительным к месту запуска exe
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(os.path.dirname(sys.executable), output_dir)
    else:
        # Для скрипта - относительный путь к месту скрипта
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_dir)


    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(get_localized_text("dir_created_success", output_dir))
        except OSError as e:
            print(get_localized_text("dir_create_error", output_dir, e))
            # Если создать не удалось, возвращаемся к текущей директории запуска exe/скрипта
            output_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(os.getcwd())
            messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("dir_create_error", config.get("output_directory"), e) + "\n" + f"Отчеты будут сохраняться в: {output_dir}")
    
    # Обновляем output_directory в конфиге на абсолютный или правильно относительный путь для дальнейшего использования
    config["output_directory"] = output_dir
    return config

# --- Функции обработки данных ---

def read_csv_data(file_path):
    """
    Считывает данные из CSV-файла.
    """
    data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                data.append(row)
        return data
    except FileNotFoundError:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("csv_file_not_found", file_path))
    except Exception as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("csv_read_error", e))
    return []

def read_text_log(file_path):
    """
    Считывает данные из простого текстового файла (лога).
    """
    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("text_file_not_found", file_path))
    except Exception as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("text_read_error", e))
    return [line.strip() for line in lines]

def fetch_web_page_content(url):
    """
    Скачивает полное HTML-содержимое веб-страницы.
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() # Вызывает HTTPError для плохих ответов (4xx или 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("web_fetch_error", url, e))
    return None

def parse_web_page_text(html_content):
    """
    Парсит HTML-контент и извлекает весь видимый текст.
    """
    if not html_content:
        return ""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract() # Удаляем теги <script> и <style>
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("web_parse_error", e))
        return ""

def parse_web_page_elements(html_content, tag_name):
    """
    Парсит HTML-контент и извлекает текст из указанных HTML-элементов.
    """
    if not html_content:
        messagebox.showwarning(get_localized_text("info_dialog_title"), get_localized_text("web_parse_elements_warning", tag_name))
        return []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all(tag_name)
        extracted_texts = [element.get_text(strip=True) for element in elements]
        return extracted_texts
    except Exception as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("web_parse_elements_error", tag_name, e))
        return []

def generate_csv_summary(data):
    """
    Генерирует простую сводку для CSV-данных.
    """
    if not data:
        return get_localized_text("csv_no_data")

    num_records = len(data)
    headers = list(data[0].keys()) if data else []

    report = f"{get_localized_text('csv_report_header')}\n"
    report += f"{get_localized_text('csv_total_records', num_records)}\n"
    report += f"{get_localized_text('csv_headers', ', '.join(headers))}\n"
    report += f"{get_localized_text('csv_example_records')}\n"
    for i, row in enumerate(data[:3]):
        report += f"  Пример {i+1}: {row}\n"
    report += "---------------------------\n"
    return report

def generate_text_log_summary(lines):
    """
    Генерирует простую сводку для текстовых логов.
    """
    if not lines:
        return get_localized_text("text_no_data")

    num_lines = len(lines)
    report = f"{get_localized_text('text_report_header')}\n"
    report += f"{get_localized_text('text_total_lines', num_lines)}\n"
    report += f"{get_localized_text('text_example_first_lines')}\n"
    for i, line in enumerate(lines[:5]):
        report += f"  {line}\n"
    if num_lines > 5:
        report += "...\n"
        report += f"{get_localized_text('text_example_last_lines')}\n"
        for i, line in enumerate(lines[-5:]):
            report += f"  {line}\n"
    report += "---------------------------------\n"
    return report

def generate_web_page_summary(text_content, url, extracted_elements=None):
    """
    Генерирует простую сводку для текстового содержимого веб-страницы.
    """
    report = f"{get_localized_text('web_report_header')}\n"
    report += f"URL: {url}\n"

    if text_content:
        summary_length = 500
        summary_text = text_content[:summary_length] + ("..." if len(text_content) > summary_length else "")
        report += f"{get_localized_text('web_total_length', len(text_content))}\n"
        report += f"{get_localized_text('web_first_chars', summary_length)}\n"
        report += f"--------------------------------------------------\n"
        report += f"{summary_text}\n"
        report += f"--------------------------------------------------\n"
    else:
        report += f"{get_localized_text('web_no_text_content')}\n"

    if extracted_elements:
        report += get_localized_text("web_extracted_elements_header")
        for tag, texts in extracted_elements.items():
            if texts:
                report += f"\n{get_localized_text('web_tag_count', tag, len(texts))}\n"
                for i, text in enumerate(texts[:3]):
                    report += f"    - {text[:100]}...\n" # Обрезаем для краткости в отчете
                if len(texts) > 3:
                    report += get_localized_text("web_and_more")
            else:
                report += f"  {get_localized_text('web_tag_not_found', tag)}\n"
    report += "--------------------------------------------------\n"
    return report

def filter_csv_data(data, column_name, operator, value):
    """
    Фильтрует CSV-данные по заданному критерию.
    """
    filtered_data = []
    for row in data:
        if column_name not in row:
            continue

        row_value = row[column_name]

        try:
            row_value_num = float(row_value)
            value_num = float(value)
        except (ValueError, TypeError):
            row_value_num = None
            value_num = None

        match = False
        if operator == '==':
            match = (row_value == str(value))
        elif operator == '!=':
            match = (row_value != str(value))
        elif operator == '>':
            if row_value_num is not None and value_num is not None:
                match = (row_value_num > value_num)
        elif operator == '<':
            if row_value_num is not None and value_num is not None:
                match = (row_value_num < value_num)
        elif operator == '>=':
            if row_value_num is not None and value_num is not None:
                match = (row_value_num >= value_num)
        elif operator == '<=':
            if row_value_num is not None and value_num is not None:
                match = (row_value_num <= value_num)
        elif operator == 'contains':
            match = (str(value).lower() in row_value.lower())
        elif operator == 'not contains':
            match = (str(value).lower() not in row_value.lower())
        else:
            messagebox.showwarning(get_localized_text("info_dialog_title"), get_localized_text("csv_unknown_operator", operator))
            continue

        if match:
            filtered_data.append(row)
    return filtered_data

def filter_text_log(lines, keyword=None, regex_pattern=None):
    """
    Фильтрует текстовые строки лога по ключевому слову или регулярному выражению.
    """
    filtered_lines = []
    if keyword:
        search_keyword = keyword.lower()
        for line in lines:
            if search_keyword in line.lower():
                filtered_lines.append(line)
    elif regex_pattern:
        try:
            compiled_regex = re.compile(regex_pattern)
            for line in lines:
                if compiled_regex.search(line):
                    filtered_lines.append(line)
        except re.error as e:
            messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("text_filter_regex_error", regex_pattern, e))
            return [] # Возвращаем пустой список при ошибке регулярного выражения
    else:
        return lines # Если ни ключевое слово, ни regex не заданы, возвращаем все строки

    return filtered_lines

def save_report_to_text_file(config, report_content, file_path):
    """
    Сохраняет строковое содержимое отчета в текстовый файл.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        messagebox.showinfo(get_localized_text("info_dialog_title"), get_localized_text("report_saved_text", file_path))
    except IOError as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("report_save_text_error", file_path, e))

def save_report_to_markdown_file(config, report_content, file_path):
    """
    Сохраняет строковое содержимое отчета в Markdown-файл.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        messagebox.showinfo(get_localized_text("info_dialog_title"), get_localized_text("report_saved_md", file_path))
    except IOError as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("report_save_md_error", file_path, e))

def save_data_to_json_file(config, data, file_path):
    """
    Сохраняет структурированные данные (например, список словарей) в JSON-файл.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo(get_localized_text("info_dialog_title"), get_localized_text("data_saved_json", file_path))
    except IOError as e:
        messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("data_save_json_error", file_path, e))


def log_monitoring_event(config, message):
    """
    Записывает сообщение о событии мониторинга в специальный лог-файл.
    """
    # output_dir уже содержит корректный путь после вызова ensure_output_directory_exists
    output_dir = config.get("output_directory")
    log_file_path = os.path.join(output_dir, MONITORING_LOG_FILE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except IOError as e:
        print(f"Error writing to monitoring log file {log_file_path}: {e}")

# Глобальные переменные для мониторинга
monitoring_stop_event = threading.Event()
input_command_queue = queue.Queue()

# --- Класс основного приложения Tkinter ---

class DataProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Initial Title") # Временный заголовок, будет обновлен после загрузки языка
        self.root.geometry("1000x700")

        global app_config, current_language

        # 1. Загрузка конфигурации и обеспечение директории
        app_config = load_config()
        app_config = ensure_output_directory_exists(app_config)

        # 2. Установка начального языка
        initial_language = app_config.get("default_language", "ru")
        if initial_language in LOCALIZED_TEXTS:
            current_language = initial_language
        else:
            current_language = "en" # Fallback на английский

        # 3. Обновляем заголовок окна после установки языка
        self.root.title(get_localized_text("app_title"))

        # 4. Создаем Notebook (вкладки) для разных разделов
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # 5. Создаем фреймы для каждой вкладки
        self.main_frame = ttk.Frame(self.notebook)
        self.monitor_frame = ttk.Frame(self.notebook)
        self.csv_frame = ttk.Frame(self.notebook)
        self.text_log_frame = ttk.Frame(self.notebook)
        self.web_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)

        # 6. Добавляем фреймы как вкладки в Notebook
        self.notebook.add(self.main_frame, text=get_localized_text("app_title"))
        self.notebook.add(self.monitor_frame, text=get_localized_text("menu_monitor_url"))
        self.notebook.add(self.csv_frame, text=get_localized_text("menu_csv_analysis"))
        self.notebook.add(self.text_log_frame, text=get_localized_text("menu_text_log_analysis"))
        self.notebook.add(self.web_frame, text=get_localized_text("menu_web_page_analysis"))
        self.notebook.add(self.settings_frame, text=get_localized_text("menu_settings"))

        # 7. Инициализация содержимого каждой вкладки
        self._setup_main_frame()
        self._setup_monitor_frame()
        self._setup_csv_frame()
        self._setup_text_log_frame()
        self._setup_web_frame()
        self._setup_settings_frame()

        # 8. Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # 9. Переменная для потока мониторинга
        self.monitoring_thread = None

        # 10. Запускаем периодическую проверку очереди сообщений
        self.root.after(100, self.check_monitoring_queue)


    def update_notebook_texts(self):
        """Обновляет тексты вкладок Notebook и содержимое фреймов при смене языка."""
        self.root.title(get_localized_text("app_title"))
        self.notebook.tab(0, text=get_localized_text("app_title"))
        self.notebook.tab(1, text=get_localized_text("menu_monitor_url"))
        self.notebook.tab(2, text=get_localized_text("menu_csv_analysis"))
        self.notebook.tab(3, text=get_localized_text("menu_text_log_analysis"))
        self.notebook.tab(4, text=get_localized_text("menu_web_page_analysis"))
        self.notebook.tab(5, text=get_localized_text("menu_settings"))

        # Пересоздаем содержимое каждого фрейма, чтобы обновить тексты виджетов внутри них
        # Это важно, чтобы все Label, Button и т.д. получили новые локализованные тексты
        self._setup_main_frame()
        self._setup_monitor_frame()
        self._setup_csv_frame()
        self._setup_text_log_frame()
        self._setup_web_frame()
        self._setup_settings_frame()

    def _setup_main_frame(self):
        """Настраивает содержимое основной вкладки."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        welcome_label = ttk.Label(self.main_frame, text=get_localized_text("welcome_message", APP_VERSION),
                                  font=("Arial", 12), wraplength=700, justify="center")
        welcome_label.pack(pady=50)

        current_lang_label = ttk.Label(self.main_frame, text=get_localized_text("current_language", current_language.upper()),
                                       font=("Arial", 10))
        current_lang_label.pack(pady=10)

        exit_button = ttk.Button(self.main_frame, text=get_localized_text("menu_exit"), command=self._on_closing)
        exit_button.pack(pady=20)

    def _setup_monitor_frame(self):
        """Настраивает содержимое вкладки мониторинга URL."""
        for widget in self.monitor_frame.winfo_children():
            widget.destroy()

        # Поле для URL
        ttk.Label(self.monitor_frame, text=get_localized_text("monitoring_url_label")).pack(pady=5)
        self.url_entry = ttk.Entry(self.monitor_frame, width=50)
        self.url_entry.pack(pady=5)
        last_url = app_config["last_used_urls"].get("web_page_example", "")
        if last_url:
            self.url_entry.insert(0, last_url)

        # Поле для интервала
        ttk.Label(self.monitor_frame, text=get_localized_text("monitoring_interval_label")).pack(pady=5)
        self.interval_entry = ttk.Entry(self.monitor_frame, width=10)
        self.interval_entry.insert(0, "300")
        self.interval_entry.pack(pady=5)

        # Кнопки
        self.start_monitor_button = ttk.Button(self.monitor_frame, text=get_localized_text("start_monitoring_button"), command=self._start_monitoring_gui)
        self.start_monitor_button.pack(pady=10)

        self.stop_monitor_button = ttk.Button(self.monitor_frame, text=get_localized_text("monitoring_stop_button"), command=self._stop_monitoring_gui, state=tk.DISABLED)
        self.stop_monitor_button.pack(pady=5)

        # Поле для вывода логов мониторинга
        self.monitor_log_text = tk.Text(self.monitor_frame, height=15, width=90, state=tk.DISABLED)
        self.monitor_log_text.pack(pady=10)

    def _setup_csv_frame(self):
        """Настраивает содержимое вкладки CSV анализа."""
        for widget in self.csv_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.csv_frame, text=get_localized_text("menu_csv_analysis"), font=("Arial", 14)).pack(pady=10)

        # Фрейм для выбора файла
        file_frame = ttk.Frame(self.csv_frame)
        file_frame.pack(pady=10)

        self.csv_file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.csv_file_path_var, width=50, state='readonly').pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text=get_localized_text("select_file"), command=self._select_csv_file).pack(side=tk.LEFT)

        # Поля для фильтрации
        ttk.Label(self.csv_frame, text="Фильтрация CSV:").pack(pady=5)
        filter_frame = ttk.Frame(self.csv_frame)
        filter_frame.pack(pady=5)
        ttk.Label(filter_frame, text="Колонка:").pack(side=tk.LEFT)
        self.csv_filter_column = ttk.Entry(filter_frame, width=15)
        self.csv_filter_column.pack(side=tk.LEFT, padx=5)
        ttk.Label(filter_frame, text="Оператор:").pack(side=tk.LEFT)
        self.csv_filter_operator = ttk.Combobox(filter_frame, values=["==", "!=", ">", "<", ">=", "<=", "contains", "not contains"], width=10)
        self.csv_filter_operator.set("==") # Значение по умолчанию
        self.csv_filter_operator.pack(side=tk.LEFT, padx=5)
        ttk.Label(filter_frame, text="Значение:").pack(side=tk.LEFT)
        self.csv_filter_value = ttk.Entry(filter_frame, width=20)
        self.csv_filter_value.pack(side=tk.LEFT, padx=5)

        ttk.Button(self.csv_frame, text=get_localized_text("process_file_button"), command=self._process_csv_data).pack(pady=10)

        # Текстовое поле для вывода отчета
        self.csv_report_text = tk.Text(self.csv_frame, height=15, width=90, state=tk.DISABLED)
        self.csv_report_text.pack(pady=10)

        self.csv_save_report_button = ttk.Button(self.csv_frame, text=get_localized_text("prompt_save_report"), command=lambda: self._prompt_and_save_report_gui(self.csv_report_text.get(1.0, tk.END), "csv_report"), state=tk.DISABLED)
        self.csv_save_report_button.pack(pady=5)


    def _select_csv_file(self):
        file_path = filedialog.askopenfilename(
            title=get_localized_text("select_csv_file"),
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if file_path:
            self.csv_file_path_var.set(file_path)
            self.csv_save_report_button.config(state=tk.DISABLED) # Сброс состояния кнопки сохранения при смене файла
            # Очищаем поля фильтрации при выборе нового файла
            self.csv_filter_column.delete(0, tk.END)
            self.csv_filter_operator.set("==")
            self.csv_filter_value.delete(0, tk.END)


    def _process_csv_data(self):
        file_path = self.csv_file_path_var.get()
        if not file_path:
            messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("select_csv_file"))
            return

        data = read_csv_data(file_path)
        if not data:
            self._display_report_in_text_widget(self.csv_report_text, get_localized_text("csv_no_data"))
            self.csv_save_report_button.config(state=tk.DISABLED)
            return

        original_data_len = len(data) # Для отчета по фильтрации

        # Применяем фильтр
        column = self.csv_filter_column.get().strip()
        operator = self.csv_filter_operator.get().strip()
        value = self.csv_filter_value.get().strip()

        filtered_data_used_for_report = data # По умолчанию, весь датасет

        report_text_filter_info = ""

        if column and operator and value:
            filtered_data = filter_csv_data(data, column, operator, value)
            report_text_filter_info = "\n" + get_localized_text("csv_filter_applying", column, operator, value) + "\n"
            report_text_filter_info += get_localized_text("csv_filter_count", len(filtered_data)) + f" (из {original_data_len} исходных записей)\n"
            filtered_data_used_for_report = filtered_data
        else:
            report_text_filter_info = get_localized_text("text_filter_no_criteria") + "\n" # Нет фильтрации

        # Генерируем сводку по (отфильтрованным) данным
        summary_report = generate_csv_summary(filtered_data_used_for_report)

        final_report = report_text_filter_info + summary_report
        self._display_report_in_text_widget(self.csv_report_text, final_report)
        self.csv_save_report_button.config(state=tk.NORMAL)


    def _setup_text_log_frame(self):
        """Настраивает содержимое вкладки анализа текстового лога."""
        for widget in self.text_log_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.text_log_frame, text=get_localized_text("menu_text_log_analysis"), font=("Arial", 14)).pack(pady=10)

        # Фрейм для выбора файла
        file_frame = ttk.Frame(self.text_log_frame)
        file_frame.pack(pady=10)

        self.text_log_file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.text_log_file_path_var, width=50, state='readonly').pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text=get_localized_text("select_file"), command=self._select_text_log_file).pack(side=tk.LEFT)

        # Поля для фильтрации
        ttk.Label(self.text_log_frame, text="Фильтрация лога").pack(pady=5)
        filter_frame = ttk.Frame(self.text_log_frame)
        filter_frame.pack(pady=5)
        ttk.Label(filter_frame, text="Ключевое слово:").pack(side=tk.LEFT)
        self.text_filter_keyword = ttk.Entry(filter_frame, width=20)
        self.text_filter_keyword.pack(side=tk.LEFT, padx=5)
        ttk.Label(filter_frame, text="Regex:").pack(side=tk.LEFT)
        self.text_filter_regex = ttk.Entry(filter_frame, width=30)
        self.text_filter_regex.pack(side=tk.LEFT, padx=5)
        ttk.Label(filter_frame, text="(Используется либо ключевое слово, либо regex)").pack(side=tk.LEFT, padx=5)


        ttk.Button(self.text_log_frame, text=get_localized_text("process_file_button"), command=self._process_text_log_data).pack(pady=10)

        # Текстовое поле для вывода отчета
        self.text_log_report_text = tk.Text(self.text_log_frame, height=15, width=90, state=tk.DISABLED)
        self.text_log_report_text.pack(pady=10)

        self.text_log_save_report_button = ttk.Button(self.text_log_frame, text=get_localized_text("prompt_save_report"), command=lambda: self._prompt_and_save_report_gui(self.text_log_report_text.get(1.0, tk.END), "text_log_report"), state=tk.DISABLED)
        self.text_log_save_report_button.pack(pady=5)

    def _select_text_log_file(self):
        file_path = filedialog.askopenfilename(
            title=get_localized_text("select_text_file"),
            filetypes=(("Text files", "*.txt"), ("Log files", "*.log"), ("All files", "*.*"))
        )
        if file_path:
            self.text_log_file_path_var.set(file_path)
            self.text_log_save_report_button.config(state=tk.DISABLED)
            # Очищаем поля фильтрации при выборе нового файла
            self.text_filter_keyword.delete(0, tk.END)
            self.text_filter_regex.delete(0, tk.END)


    def _process_text_log_data(self):
        file_path = self.text_log_file_path_var.get()
        if not file_path:
            messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("select_text_file"))
            return

        lines = read_text_log(file_path)
        if not lines:
            self._display_report_in_text_widget(self.text_log_report_text, get_localized_text("text_no_data"))
            self.text_log_save_report_button.config(state=tk.DISABLED)
            return

        original_lines_len = len(lines) # Для отчета по фильтрации

        keyword = self.text_filter_keyword.get().strip()
        regex_pattern = self.text_filter_regex.get().strip()

        filtered_lines_used_for_report = lines # По умолчанию, все строки

        report_text_filter_info = ""

        if keyword and regex_pattern:
            messagebox.showwarning(get_localized_text("info_dialog_title"), "Пожалуйста, используйте либо ключевое слово, либо регулярное выражение, но не оба сразу.")
            self._display_report_in_text_widget(self.text_log_report_text, "Ошибка: Используйте только один фильтр.")
            self.text_log_save_report_button.config(state=tk.DISABLED)
            return
        elif keyword:
            filtered_lines_used_for_report = filter_text_log(lines, keyword=keyword)
            report_text_filter_info = "\n" + get_localized_text("text_filter_keyword_applying", keyword) + "\n"
            report_text_filter_info += get_localized_text("text_filter_count", len(filtered_lines_used_for_report)) + f" (из {original_lines_len} исходных строк)\n"
        elif regex_pattern:
            filtered_lines_used_for_report = filter_text_log(lines, regex_pattern=regex_pattern)
            # filter_text_log теперь выводит messagebox и возвращает [], если regex_pattern некорректен
            if not filtered_lines_used_for_report and regex_pattern and "Ошибка в регулярном выражении" in self.text_log_report_text.get(1.0, tk.END):
                 self.text_log_save_report_button.config(state=tk.DISABLED)
                 return
            report_text_filter_info = "\n" + get_localized_text("text_filter_regex_applying", regex_pattern) + "\n"
            report_text_filter_info += get_localized_text("text_filter_count", len(filtered_lines_used_for_report)) + f" (из {original_lines_len} исходных строк)\n"
        else:
            report_text_filter_info = get_localized_text("text_filter_no_criteria") + "\n"


        summary_report = generate_text_log_summary(filtered_lines_used_for_report)
        final_report = report_text_filter_info + summary_report

        self._display_report_in_text_widget(self.text_log_report_text, final_report)
        self.text_log_save_report_button.config(state=tk.NORMAL)


    def _setup_web_frame(self):
        """Настраивает содержимое вкладки анализа веб-страницы."""
        for widget in self.web_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.web_frame, text=get_localized_text("menu_web_page_analysis"), font=("Arial", 14)).pack(pady=10)

        # Поле для URL
        ttk.Label(self.web_frame, text=get_localized_text("monitoring_url_label")).pack(pady=5)
        self.web_url_entry = ttk.Entry(self.web_frame, width=70)
        self.web_url_entry.pack(pady=5)
        # Можно загрузить последний использованный URL из конфига, если нужно
        # self.web_url_entry.insert(0, app_config["last_used_urls"].get("web_page_example", ""))

        # Поле для HTML-тега
        ttk.Label(self.web_frame, text=get_localized_text("enter_tag_name")).pack(pady=5)
        self.web_tag_entry = ttk.Entry(self.web_frame, width=20)
        self.web_tag_entry.pack(pady=5)

        ttk.Button(self.web_frame, text=get_localized_text("process_web_page_button"), command=self._process_web_page_data).pack(pady=10)

        # Текстовое поле для вывода отчета
        self.web_report_text = tk.Text(self.web_frame, height=15, width=90, state=tk.DISABLED)
        self.web_report_text.pack(pady=10)

        self.web_save_report_button = ttk.Button(self.web_frame, text=get_localized_text("prompt_save_report"), command=lambda: self._prompt_and_save_report_gui(self.web_report_text.get(1.0, tk.END), "web_page_report"), state=tk.DISABLED)
        self.web_save_report_button.pack(pady=5)

    def _process_web_page_data(self):
        url = self.web_url_entry.get().strip()
        if not url:
            messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("invalid_url"))
            return

        tag_name = self.web_tag_entry.get().strip()
        
        self._display_report_in_text_widget(self.web_report_text, "Загрузка и обработка...")
        self.root.update_idletasks() # Обновить GUI немедленно

        html_content = fetch_web_page_content(url)
        if html_content is None:
            # fetch_web_page_content уже покажет messagebox об ошибке, просто выходим
            self._display_report_in_text_widget(self.web_report_text, get_localized_text("web_fetch_error", url, "Не удалось загрузить страницу"))
            self.web_save_report_button.config(state=tk.DISABLED)
            return

        text_content = parse_web_page_text(html_content)
        
        extracted_elements = {}
        if tag_name:
            elements = parse_web_page_elements(html_content, tag_name)
            if elements is not None: # parse_web_page_elements возвращает [] при ошибке
                extracted_elements[tag_name] = elements

        report = generate_web_page_summary(text_content, url, extracted_elements)
        self._display_report_in_text_widget(self.web_report_text, report)
        self.web_save_report_button.config(state=tk.NORMAL)


    def _setup_settings_frame(self):
        """Настраивает содержимое вкладки настроек."""
        for widget in self.settings_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.settings_frame, text=get_localized_text("select_language_gui"), font=("Arial", 12)).pack(pady=20)
        self.language_var = tk.StringVar(self.settings_frame)
        self.language_var.set(current_language)

        lang_options = app_config.get("available_languages", ["ru", "en", "es"])
        # Убедимся, что текущий язык есть в списке доступных, иначе выбираем первый
        if current_language not in lang_options:
            self.language_var.set(lang_options[0])

        self.language_menu = ttk.OptionMenu(self.settings_frame, self.language_var, self.language_var.get(), *lang_options, command=self._change_language_gui)
        self.language_menu.pack(pady=10)

        save_button = ttk.Button(self.settings_frame, text=get_localized_text("save_config_button"), command=self._save_settings_gui)
        save_button.pack(pady=30)

    def _change_language_gui(self, new_lang_code):
        """Обработчик смены языка из GUI."""
        global current_language, app_config
        set_language(new_lang_code)
        app_config["default_language"] = new_lang_code
        self.update_notebook_texts() # Обновляем все тексты в интерфейсе

    def _save_settings_gui(self):
        """Обработчик сохранения настроек из GUI."""
        save_config(app_config)

    def _display_report_in_text_widget(self, text_widget, report_content):
        """Вспомогательная функция для отображения отчета в текстовом виджете."""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, report_content)
        text_widget.see(tk.END) # Прокручиваем к концу
        text_widget.config(state=tk.DISABLED)

    def _prompt_and_save_report_gui(self, report_content, default_filename="report"):
        """
        Запрашивает у пользователя имя файла и формат, затем сохраняет отчет.
        Использует filedialog для выбора пути и имени файла.
        """
        if not report_content.strip(): # Проверяем, есть ли что сохранять
            messagebox.showwarning(get_localized_text("info_dialog_title"), get_localized_text("report_not_saved"))
            return

        file_formats = [
            (get_localized_text("report_saved_text").split(":")[0].strip() + " (*.txt)", "*.txt"),
            (get_localized_text("report_saved_md").split(":")[0].strip() + " (*.md)", "*.md"),
            ("All files", "*.*")
        ]
        
        # Начальная директория для сохранения отчетов берется из конфига
        # app_config["output_directory"] уже содержит корректный абсолютный путь
        initial_dir = app_config.get("output_directory")


        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialdir=initial_dir, # Устанавливаем начальную директорию
            initialfile=f"{default_filename}.txt",
            filetypes=file_formats,
            title=get_localized_text("prompt_report_filename")
        )

        if file_path:
            filename, ext = os.path.splitext(file_path)
            ext = ext.lower()

            if ext == ".md":
                save_report_to_markdown_file(app_config, report_content, file_path)
            elif ext == ".txt":
                save_report_to_text_file(app_config, report_content, file_path)
            else:
                # Если пользователь выбрал "All files" и не указал расширение, или указал неизвестное
                messagebox.showwarning(get_localized_text("info_dialog_title"), get_localized_text("invalid_report_format"))
                save_report_to_text_file(app_config, report_content, f"{filename}.txt")
        else:
            messagebox.showinfo(get_localized_text("info_dialog_title"), get_localized_text("report_not_saved"))


    def _start_monitoring_gui(self):
        """Запускает мониторинг URL в отдельном потоке для GUI."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror(get_localized_text("error_dialog_title"), get_localized_text("invalid_url"))
            return

        interval_str = self.interval_entry.get().strip()
        interval = 300 # Значение по умолчанию
        try:
            if interval_str:
                parsed_interval = int(interval_str)
                if parsed_interval > 0:
                    interval = parsed_interval
                else:
                    messagebox.showwarning(get_localized_text("info_dialog_title"), get_localized_text("invalid_interval"))
            else:
                # Если поле пустое, также используем дефолт
                messagebox.showwarning(get_localized_text("info_dialog_title"), get_localized_text("invalid_interval"))
        except ValueError:
            messagebox.showwarning(get_localized_text("info_dialog_title"), get_localized_text("invalid_interval"))
            
        # Сохраняем последний использованный URL в конфиг
        app_config["last_used_urls"]["web_page_example"] = url
        save_config(app_config) # Сохраняем конфиг

        self.start_monitor_button.config(state=tk.DISABLED)
        self.stop_monitor_button.config(state=tk.NORMAL)
        self._display_report_in_text_widget(self.monitor_log_text, get_localized_text("monitoring_start", url) + "\n")
        self.root.update_idletasks() # Обновляем GUI немедленно

        # Запускаем мониторинг в отдельном потоке
        self.monitoring_thread = threading.Thread(target=self._run_monitoring_thread, args=(url, interval))
        self.monitoring_thread.daemon = True # Позволяет потоку завершиться при закрытии главного окна
        self.monitoring_thread.start()

    def _run_monitoring_thread(self, url, interval):
        """
        Функция, выполняющаяся в отдельном потоке для мониторинга URL.
        Отправляет обновления в очередь GUI.
        """
        global monitoring_stop_event
        monitoring_stop_event.clear() # Сбрасываем флаг остановки

        self._add_to_gui_queue(("log", get_localized_text("initial_fetch", url)))
        initial_content = fetch_web_page_content(url)
        if initial_content is None:
            self._add_to_gui_queue(("log", get_localized_text("no_content_for_monitoring", url)))
            self._add_to_gui_queue(("stop_monitoring_signal", None)) # Сигнал GUI для очистки
            return

        last_known_text = parse_web_page_text(initial_content)
        last_known_hash = hashlib.sha256(last_known_text.encode('utf-8')).hexdigest()

        while not monitoring_stop_event.is_set():
            current_time = datetime.datetime.now()
            current_content = fetch_web_page_content(url) # Эта функция уже покажет messagebox при ошибке

            if current_content is None:
                # Если не удалось получить контент, просто пропускаем этот интервал
                # messagebox уже выведено в fetch_web_page_content
                self._add_to_gui_queue(("log", f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Не удалось получить контент. Повтор через {interval} секунд."))
            else:
                current_text = parse_web_page_text(current_content)
                current_hash = hashlib.sha256(current_text.encode('utf-8')).hexdigest()

                if current_hash != last_known_hash:
                    message = get_localized_text("changes_detected", url, current_time.strftime("%Y-%m-%d %H:%M:%S"))
                    self._add_to_gui_queue(("log", message))
                    log_monitoring_event(app_config, get_localized_text("monitoring_log_entry", current_time.strftime("%Y-%m-%d %H:%M:%S"), url))
                    last_known_hash = current_hash
                else:
                    message = get_localized_text("no_changes", url, current_time.strftime("%Y-%m-%d %H:%M:%S"))
                    self._add_to_gui_queue(("log", message))

            # Ждем интервал, но проверяем флаг остановки, чтобы быстро реагировать
            for _ in range(int(interval * 10)): # Проверяем 10 раз в секунду
                if monitoring_stop_event.is_set():
                    break
                time.sleep(0.1)

        self._add_to_gui_queue(("log", get_localized_text("monitoring_stopped")))
        self._add_to_gui_queue(("stop_monitoring_signal", None))

    def _add_to_gui_queue(self, item):
        """Добавляет элемент (сообщение или команду) в очередь для обработки в главном потоке Tkinter."""
        input_command_queue.put(item)

    def check_monitoring_queue(self):
        """
        Периодически проверяет очередь сообщений из потока мониторинга и обновляет GUI.
        """
        try:
            while True:
                item = input_command_queue.get_nowait()
                if isinstance(item, tuple) and item[0] == "log":
                    message = item[1]
                    self.monitor_log_text.config(state=tk.NORMAL)
                    self.monitor_log_text.insert(tk.END, message + "\n")
                    self.monitor_log_text.see(tk.END)
                    self.monitor_log_text.config(state=tk.DISABLED)
                elif isinstance(item, tuple) and item[0] == "stop_monitoring_signal":
                    self._stop_monitoring_gui_cleanup()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_monitoring_queue)

    def _stop_monitoring_gui(self):
        """Останавливает мониторинг URL, устанавливая флаг."""
        global monitoring_stop_event
        monitoring_stop_event.set()
        self.start_monitor_button.config(state=tk.NORMAL)
        self.stop_monitor_button.config(state=tk.DISABLED)
        # Сообщение о остановке будет добавлено потоком мониторинга

    def _stop_monitoring_gui_cleanup(self):
        """
        Вызывается, когда поток мониторинга сообщает о завершении.
        Обновляет состояние GUI.
        """
        # Если кнопка уже активна (пользователь нажал стоп), то не меняем ее
        if self.start_monitor_button['state'] == tk.DISABLED:
            self.start_monitor_button.config(state=tk.NORMAL)
            self.stop_monitor_button.config(state=tk.DISABLED)

    def _on_closing(self):
        """Обработчик закрытия окна."""
        global monitoring_stop_event
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            monitoring_stop_event.set()
            # Даем потоку немного времени на завершение, чтобы он мог отправить последнее сообщение в очередь
            self.monitoring_thread.join(timeout=1.0) 
        self.root.destroy()

# --- Точка входа в программу ---

if __name__ == "__main__":
    root = tk.Tk()
    app = DataProcessorApp(root)
    root.mainloop()