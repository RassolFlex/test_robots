from datetime import datetime, timedelta

import xlsxwriter

from robots.models import Robot


def get_robots_in_a_period():
    """
    Получение списка роботов за определённый период в виде словаря.

    Возвращает словарь вида:
        {model: {version: count}}

    Период по умолчанию - 7 дней.
    """

    REQUIRED_DAYS = 7

    today = datetime.today().strftime('%Y-%m-%d 23:59:59')
    period_ago = (datetime.today() - timedelta(days=REQUIRED_DAYS)
                  ).strftime('%Y-%m-%d')

    robots = Robot.objects.filter(
        created__gte=period_ago, created__lte=today
    )

    robots_in_a_period = {}
    for robot in robots:
        if robot.model not in robots_in_a_period:
            robots_in_a_period[robot.model] = {}
        if robot.version not in robots_in_a_period[robot.model]:
            robots_in_a_period[robot.model][robot.version] = 1
        else:
            robots_in_a_period[robot.model][robot.version] += 1

    return robots_in_a_period


def get_file(robots):
    """
    Создание файла в формате xlsx на основе входящего словаря.

    Файл имеет следующую структуру:
        Модель | Версия | Количество
    """

    workbook = xlsxwriter.Workbook('robots.xlsx')

    for model in robots:
        worksheet = workbook.add_worksheet(name=model)
        row = 0
        col = 0
        worksheet.write(row, col, 'Модель')
        worksheet.write(row, col + 1, 'Версия')
        worksheet.write(row, col + 2, 'Количество')
        row += 1
        for version in robots[model]:
            worksheet.write(row, col, model)
            worksheet.write(row, col + 1, version)
            worksheet.write(row, col + 2, robots[model][version])
            row += 1

    workbook.close()
