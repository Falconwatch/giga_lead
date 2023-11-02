# Запуск
## Интернет
Для запуска приложения во внешнем контуре необходимо разместить файл dotenv в корневой папке
Содержание файла:
AUTH=[Ваш AUTH]

## Внутренний/внешний контур
Для запуска в контурах альфа/сигма необходимо сложить сертификаты в папку certs и заполнить файл certs.cfg

# Разработка
Доска с задачами: https://jira.delta.sbrf.ru/secure/RapidBoard.jspa?rapidView=27075 

Про GigaChat API: https://developers.sber.ru/docs/ru/gigachat/api/overview

# Быстрый старт
1) Нужно установить компилятор python версии >=3.10. С личного компьютера можно скачать с: https://www.python.org/downloads/. Или с SberUserSoft.
2) Установить расширение Jupyter.
3) Прописать в терминале where python3 и скопировать путь к питону.
3) Далее открыв Notebook.ipynb и справа сверху выбрать select kernel. Указать select another kernel -> python environments -> create python environment -> venv -> Python версии >= 3.10. (Или если не появился указываем скопированный ранее путь). -> Указываем jupyter_requirements.txt

# Описание 
В текущей реализации есть два ноутбука: Notebook и Prompt_experiments.  
В файле Notebook присутствует рабочий пример отправки новостей в гигачат с