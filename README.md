# Project bonus track (методы анализа данных)
### Репозиторий состоит из: 
  * В папке parsers хранятся скрипты python, которые собирали и загружали данные в папку data.
    Использовались такие библиотеки, как: bs4, selenium.
    + в файле main.py находится скрипт на обработку файла full_info.
    + в файле agency_api.py находится скрипт на обработку файла agency_api.
  * В папке data хранятся непосредственно 2 файла данных.
    + agency_api - в нем преорбазовался json файл, собирая через api данные зарплат муниципальных учреждений, получилось 1119016 строк.
    + full_info - в нем собиралась информация с сайта bus.gov, в файле собранные данные муниципальных учреждений (регион, ИНН и названия учреждений), получилось 133231 строки.
  *  [Ссылка](https://colab.research.google.com/drive/1N1-nrSsibhjwCvRlw4YOn-_hxfepXWof#scrollTo=Ofkfd_ZNYsae) на google-colab данного исследования.
