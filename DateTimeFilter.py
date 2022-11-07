from datetime import datetime, timedelta
from typing import Union, Dict, Any
from aiogram.filters import BaseFilter, CommandObject
from aiogram.types import Message


class HasTimeFilter(BaseFilter):
    """
    Этот фильтр проверяет наличие указания времени в сообщении
    и, если находит, возвращает словарь с объектом `datetime`

    :returns: :class: <Dict["messageDateTime", None]> or :class: <Dict["messageDateTime", <datetime>]>
    """

    def __init__(self):
        super().__init__()

        # с версии Python 3.10 вместо "Union[type, type]" можно использовать "type | type"
    async def __call__(self, message: Message, command: CommandObject) -> Union[bool, Dict[str, Any]]:
        typesDateTime = {"year": ["год"], "month": ["месяца", "месяцев", "месяц"],
                         "week": ["неделя", "недели", "недель"],
                         "day": ["день", "дня", "дней"], "hour": ["часов", "часа", "час"],
                         "minutes": ["минуту", "минуты", "минут"],
                         "seconds": ["секунду", "секунды", "секунд"]}
        messageArgs = command.args.split()
        timedata = {"year": 0, "month": 0,
                    "week": 0, "day": 0,
                    "hour": 0, "minutes": 0,
                    "seconds": 0}
        for arg in messageArgs:
            editArg = arg
            for typeDateTime in typesDateTime:
                for variable in typesDateTime.get(typeDateTime):
                    if editArg.find(variable) != -1:
                        timedata[f"{typeDateTime}"] += int(editArg.split(variable)[0])
                        editArg = editArg.replace(f"{editArg.split(variable)[0]}{variable}", "")
        timedata["day"] += timedata["year"] * 365 + timedata["month"] * 30
        nowDateTime = datetime.now()
        messageDateTime = nowDateTime + timedelta(weeks=timedata["week"], days=timedata["day"], hours=timedata["hour"],
                                                  minutes=timedata["minutes"], seconds=timedata["seconds"])
        print(nowDateTime == messageDateTime)
        if nowDateTime == messageDateTime:
            return {"messageDateTime": None}
        else:
            return {"messageDateTime": messageDateTime}
