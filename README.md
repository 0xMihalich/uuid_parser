# UUIDParser
## Вывод информации, содержащейся в UUID(GUID) строке

Данный класс не предназначен для генерации или конвертации версии UUID. Его задача только в выводе верной информации о UUID-строке
Может быть полезно при анализе базы данных.

Артибуты класса UUIDParser:
---------------------------
- uuid: UUIDStruct       - Базовый класс объекта UUID
- version: int           - Номер версии UUID как Integer
- time: datetime or None - Время генерации UUID
- varseq: UUIDVarSeq     - Класс NamedTuple, содержащий enum UUIDVariant и два Integer clock_seq
- stime: str             - Строка времени в формате "%Y-%m-%d %H:%M:%S" или "Undefined" если временная метка отсутствует
- secret: Secret         - Наследованный класс словаря, содержащий все уникальные значения объекта UUID в формате ключ: значение
- info: UUIDInfo         - Класс NamedTuple, содержащий enum UUIDVersion, enum UUIDVariant, атрибут time и словарь secret

Именованный кортеж UUIDStruct:
------------------------------
### Атрибуты:
---------
- time_low: str                                - Первый блок UUID (8 символов или 4 байта)
- time_mid: str                                - Второй блок UUID (4 символа или 2 байта)
- time_hi_and_version: str                     - Третий блок UUID (4 символа или 2 байта, первый символ определяет версию UUID)
- clock_seq_hi_and_reserved_clock_seq_low: str - Четвертый блок UUID (4 символа или 2 байта, первый символ определяет вариант UUID)
- node: str                                    - Пятый блок UUID (12 символов или 6 байт)

### Методы:
-------
- from_uuidstr - Инициализация именованного кортежа UUIDStruct из uuid-строки.
- str          - Возвращает uuid-строку.
- int          - Вовращает uuid как число.

Именованный кортеж UUIDVarSeq:
------------------------------
- variant: UUIDVariant - Объект enum UUIDVariant, содержащий вариант UUID
- clock_seq_hi: int    - 5-7 бит четвертого блока UUIDStruct, следующие после версии UUID
- clock_seq_low: int   - Последний байт четвертого блока

Именованный кортеж UUIDInfo:
----------------------------
- version: UUIDVersion - Объект enum UUIDVersion, содержащий версию UUID
- variant: UUIDVariant - Объект enum UUIDVariant, содержащий вариант UUID
- time: datetime       - Метка времени в формате datetime либо None
- secret: dict         - Словарь уникальных значений объекта UUID в формате ключ: значение

Исключения:
-----------
- UUIDParserError - Базовый класс ошибки
- UUIDTimeError   - Ошибка при получении временной метки
- UUIDVerionError - Получена не поддерживаемая версия UUID
- UUIDNotNilError - UUID версии 0, но не соответствует шаблону Nil UUID
- UUIDNotMaxError - UUID версии 15, но не соответствует шаблону Max UUID

Файл tests.py демонстрирует стандартную работу библиотеки

Пример использования:

```python
from uuid_parser import UUIDParser


uuid_string = "1eee415a-c0ba-6f04-b251-8d0ab452cbb7"
parser = UUIDParser(uuid_string)

print(parser)
```
