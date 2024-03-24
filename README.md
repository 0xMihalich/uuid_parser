# UUIDParser
## Вывод информации, содержащейся в UUID строке

Пример вывода в консоль:

```
┌────────────────────────────────────────────────────────────────┐
│                    UUIDParser v0.1.5 result                    │
╞════════════════════════════════════════════════════════════════╡
│       UUID        │    573e0100-1364-ffff-000d-b3e35e8b3c41    │
│-------------------│--------------------------------------------│
│      Version      │ UUIDv1.5 [Apollo Network Computing System] │
│-------------------│--------------------------------------------│
│      Variant      │                 0 [Apollo]                 │
│-------------------│--------------------------------------------│
│  Generated time   │            1992-02-27 22:01:05             │
│-------------------│--------------------------------------------│
│  Address Family   │                     13                     │
│-------------------│--------------------------------------------│
│      Host ID      │              197789125131329               │
└────────────────────────────────────────────────────────────────┘
```

Данный класс не предназначен для генерации или конвертации версии UUID. Его задача только в выводе верной информации о UUID
Может быть полезно при анализе базы данных.

TODO
----
- Сделать метод сравнения двух разных версий UUID, например является ли UUIDv6 результатом обновления UUIDv1 до этой версии

### `История изменения версий`:

Изменения в версии 0.1.5:
-------------------------
- Добавлено изменение версии UUID
- Рефактор кода в `time.py` для устранения цифлического импорта
- Рефактор кода в `__init__.py`
- Обновлен `tests.py`

Изменения в версии 0.1.4:
-------------------------
- Добавлено преобразование в формат 1С UUID
- Добавлено чтение из формата 1С UUID
- Обновлен `tests.py`

Изменения в версии 0.1.3:
-------------------------
- Добавлено изменение варианта
- Добавлено изменение даты
- Добавлен класс ошибки UUIDVariantError
- Добавлены методы `__int__` и `__hash__`
- Добавлены методы `change_variant` и `change_time`
- Проведен рефактор `time.py`
- В footer таблицы убрана нижняя перегородка

Изменения в версии 0.1.2:
-------------------------
- Исправлено определение варианта
- Добавлен Microsoft COM IUnknown UUID
- Добавлены функции конвертации UUID->bytes, bytes->UUID
- Добавлена возможность инициализации класса не только из строки, но и из байт и UUID-объекта
- Добавлен метод `__bytes__`
- Метод `__str__` теперь выводит UUID строку вместо таблицы
- Отображение класса в виде таблицы перенесено в метод `__repr__`

Изменения в версии 0.1.1:
-------------------------
- Новое отображение строкового представления класса в виде таблицы
- Добавлена поддержка UUID Apollo 1.5
- Добавлен класс UUIDDict
- Изменена логика получения варианта

Первый релиз. Версия 0.1.0:
---------------------------
- Вывод информации о UUID версии 1, 2, 3, 4, 5, 6, 7, 8, Nil UUID, Max UUID
- Строковое представление класса в упрощенном виде

Артибуты класса UUIDParser:
---------------------------
- uuid: UUIDStruct       - Базовый класс объекта UUID
- version: int           - Номер версии UUID как Integer
- time: datetime or None - Время генерации UUID
- varseq: UUIDVarSeq     - Класс NamedTuple, содержащий enum UUIDVariant и два Integer clock_seq
- secret: dict           - Словарь, содержащий уникальные параметры объекта UUID
- dict: UUIDDict         - OrderedDict объект, содержащий все параметры объекта в виде ключ: str, значение: Union[str, int]
- info: UUIDInfo         - Класс NamedTuple, содержащий enum UUIDVersion, enum UUIDVariant, атрибут time и словарь secret

Именованный кортеж UUIDStruct:
------------------------------
Атрибуты:
---------
- time_low: str                                - Первый блок UUID (8 символов или 4 байта)
- time_mid: str                                - Второй блок UUID (4 символа или 2 байта)
- time_hi_and_version: str                     - Третий блок UUID (4 символа или 2 байта, первый символ определяет версию UUID)
- clock_seq_hi_and_reserved_clock_seq_low: str - Четвертый блок UUID (4 символа или 2 байта, первый символ определяет вариант UUID)
- node: str                                    - Пятый блок UUID (12 символов или 6 байт)

Методы:
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
- UUIDParserError  - Базовый класс ошибки
- UUIDTimeError    - Ошибка при получении временной метки
- UUIDVariantError - Ошибка при изменении варианта
- UUIDVerionError  - Получена не поддерживаемая версия UUID
- UUIDNotNilError  - UUID версии 0, но не соответствует шаблону Nil UUID
- UUIDNotMaxError  - UUID версии 15, но не соответствует шаблону Max UUID

Файл tests.py демонстрирует стандартную работу библиотеки

Пример использования:

```python
from uuid_parser import UUIDParser


uuid_string = "1eee415a-c0ba-6f04-b251-8d0ab452cbb7"
parser = UUIDParser(uuid_string)

print(parser)
```
