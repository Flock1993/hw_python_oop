from typing import List, Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращение сообщения о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # формула расчета
        # (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM
        # * время_тренировки_в_минутах
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        return ((coeff_calorie_1 * self.get_mean_speed()
                - coeff_calorie_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # формула расчета
        # (0.035 * вес + (средняя_скорость ** 2 // рост) * 0.029 * вес)
        #  * время_тренировки_в_минутах
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        return (
            coeff_calorie_1 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * coeff_calorie_2 * self.weight) * (self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        # формула расчета
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # формула расчета
        # (средняя_скорость + 1.1) * 2 * вес
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2
        return ((self.get_mean_speed() + coeff_calorie_1) * coeff_calorie_2
                * self.weight)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_dict: Dict[str, Type[Training]] = {'SWM': Swimming,
                                             'RUN': Running,
                                             'WLK': SportsWalking}
    if workout_type not in train_dict:
        raise ValueError(f'Запрашиваемого типа тренировки {workout_type}'
                         f'не существует.')
    return train_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
