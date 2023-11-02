import argparse
import sys

from functools import wraps
import logging

log_format = '%(asctime)s.%(msecs)03d |%(levelname)-8s| %(message)s ( %(filename)s:%(lineno)s)'
logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)


class NegativeValueError(Exception):
    pass


class InvalidObject(Exception):
    def __init__(self):
        super().__init__("Объект должен быть класса Rectangle")


def class_check(class_name):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for param in list(args) + list(kwargs.values()):
                if param.__class__.__name__ != class_name:
                    raise InvalidObject

            return func(*args, **kwargs)

        return wrapper

    return inner


def log_dec(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is not None:
                logger.debug(
                    f'Функция Rectangle.{func.__name__} вернула результат: {result}, при аргументах {args}, {kwargs}')

                return result
            else:
                logger.debug(f'Функция Rectangle.{func.__name__} выполнилась успешно при аргументах {args}, {kwargs}')
        except Exception as e:
            logger.error(f'Ошибка {e} в функции Rectangle.{func.__name__} при аргументах {args}, {kwargs}')
            raise

        return None

    return wrapper


class Rectangle:
    """
    Класс, представляющий прямоугольник.
    Атрибуты:
    - width (int): ширина прямоугольника
    - height (int): высота прямоугольника
    Методы:
    - perimeter(): вычисляет периметр прямоугольника
    - area(): вычисляет площадь прямоугольника
    - __add__(other): определяет операцию сложения двух прямоугольников
    - __sub__(other): определяет операцию вычитания одного прямоугольника из другого
    - __lt__(other): определяет операцию "меньше" для двух прямоугольников
    - __eq__(other): определяет операцию "равно" для двух прямоугольников
    - __le__(other): определяет операцию "меньше или равно" для двух прямоугольников
    - __str__(): возвращает строковое представление прямоугольника
    - __repr__(): возвращает строковое представление прямоугольника, которое может быть использовано для создания нового объекта
    """

    @log_dec
    def __init__(self, width, height=None):
        self._width = 0
        self._height = 0
        self.width = width
        if height is None:
            self.height = width
        else:
            self.height = height

    @log_dec
    def perimeter(self):
        """
        Вычисляет периметр прямоугольника.
        Возвращает:
        - int: периметр прямоугольника
        """
        return 2 * (self.width + self.height)

    @log_dec
    def area(self):
        """
        Вычисляет площадь прямоугольника.
        Возвращает:
        - int: площадь прямоугольника
        """
        return self.width * self.height

    @property
    def width(self):
        return self._width

    @width.setter
    @log_dec
    def width(self, width):
        if width <= 0:
            raise NegativeValueError(f"Ширина должна быть положительной, а не {width}")
        else:
            self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    @log_dec
    def height(self, height):
        if height <= 0:
            raise NegativeValueError(f"Высота должна быть положительной, а не {height}")
        else:
            self._height = height

    @log_dec
    @class_check('Rectangle')
    def __add__(self, other):
        """
        Определяет операцию сложения двух прямоугольников.
        Аргументы:
        - other (Rectangle): второй прямоугольник
        Возвращает:
        - Rectangle: новый прямоугольник, полученный путем сложения двух исходных прямоугольников
        """
        width = self.width + other.width
        perimeter = self.perimeter() + other.perimeter()
        height = perimeter // 2 - width

        return Rectangle(width, height)

    @log_dec
    @class_check('Rectangle')
    def __sub__(self, other):
        """
        Определяет операцию вычитания одного прямоугольника из другого.
        Аргументы:
        - other (Rectangle): вычитаемый прямоугольник
        Возвращает:
        - Rectangle: новый прямоугольник, полученный путем вычитания вычитаемого прямоугольника из исходного
        """
        if self.perimeter() < other.perimeter():
            self, other = other, self
        width = abs(self.width - other.width)
        perimeter = self.perimeter() - other.perimeter()
        height = perimeter // 2 - width

        return Rectangle(width, height)

    @log_dec
    @class_check('Rectangle')
    def __lt__(self, other):
        """
        Определяет операцию "меньше" для двух прямоугольников.
        Аргументы:
        - other (Rectangle): второй прямоугольник
        Возвращает:
        - bool: True, если площадь первого прямоугольника меньше площади второго, иначе False
        """
        return self.area() < other.area()

    @log_dec
    @class_check('Rectangle')
    def __eq__(self, other):
        """
        Определяет операцию "равно" для двух прямоугольников.
        Аргументы:
        - other (Rectangle): второй прямоугольник
        Возвращает:
        - bool: True, если площади равны, иначе False
        """
        return self.area() == other.area()

    @log_dec
    @class_check('Rectangle')
    def __le__(self, other):
        """
        Определяет операцию "меньше или равно" для двух прямоугольников.
        Аргументы:
        - other (Rectangle): второй прямоугольник
        Возвращает:
        - bool: True, если площадь первого прямоугольника меньше или равна площади второго, иначе False
        """
        return self.area() <= other.area()

    def __str__(self):
        """
        Возвращает строковое представление прямоугольника.
        Возвращает:
        - str: строковое представление прямоугольника
        """
        return f"Прямоугольник со сторонами {self.width} и {self.height}"

    def __repr__(self):
        """
        Возвращает строковое представление прямоугольника, которое может быть использовано для создания нового объекта.
        Возвращает:
        - str: строковое представление прямоугольника
        """
        return f"Rectangle({self.width}, {self.height})"


if __name__ == '__main__':
    r1 = Rectangle(1, 1)
    r2 = Rectangle(1, 1)
    print(r1 > r2)
    print(r1 < 1)
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', type=str, default="INFO", help="loglevel, possible values: INFO, DEBUG")
    parser.add_argument('-x', '--width', type=int, help="width of the rectangle")
    parser.add_argument('-y', '--height', type=int, help="height of the rectangle")
    parser.add_argument('-a', '--area', action='append_const', dest='commands', const='area',
                        help="get area of the rectangle")
    parser.add_argument('-p', '--perimeter', action='append_const', dest='commands', const='perimeter',
                        help="get perimeter of the rectangle")
    args = parser.parse_args()
    logger.setLevel(args.loglevel)
    rect = Rectangle(args.width, args.height)
    for command in args.commands:
        if command == 'area':
            logger.info(f"{str(rect)}, площадь равна {rect.area()}")
        elif command == 'perimeter':
            logger.info(f"{str(rect)}, периметр равен {rect.perimeter()}")
        else:
            logger.error(f"Введена не верная команда: {command}, используйте -h для справки")
