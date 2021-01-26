import os
import csv


class CarBase:
    car_type = ""
    name_param_list = ['brand', 'photo_file_name', 'carrying']

    def __init__(self, brand, photo_file_name, carrying):
        if brand == '':
            raise ValueError
        self.brand = brand
        self.photo_file_name = self.validate_photo_filename(photo_file_name)
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]

    @staticmethod
    def validate_photo_filename(filename):
        if 0 < filename.find('.') < len(filename) and filename.count('.') == 1:
            return filename
        else:
            raise ValueError

    @classmethod
    def create_from_dict(cls, car_dict):
        parameters = [car_dict[parameter] for parameter in cls.name_param_list]
        return cls(*parameters)


class Car(CarBase):
    car_type = "car"
    name_param_list = ['brand', 'photo_file_name', 'carrying', 'passenger_seats_count']

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super(Car, self).__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = "truck"
    name_param_list = ['brand', 'photo_file_name', 'carrying', 'body_whl']

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super(Truck, self).__init__(brand, photo_file_name, carrying)

        try:
            specific_tuple = body_whl.split('x', 2)
            self.body_length, self.body_width, self.body_height = \
                float(specific_tuple[0]), float(specific_tuple[1]), float(specific_tuple[2])
        except (ValueError, IndexError):
            self.body_length, self.body_width, self.body_height = 0., 0., 0.

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = "spec_machine"
    name_param_list = ['brand', 'photo_file_name', 'carrying', 'extra']

    def __init__(self, brand, photo_file_name, carrying, extra):
        if extra == '':
            raise ValueError

        super(SpecMachine, self).__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    car_type_map = {'car': Car, 'truck': Truck, 'spec_machine': SpecMachine}
    csv.register_dialect('cars', delimiter=';')

    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file, dialect='cars')
        for row in reader:
            try:
                car_class = car_type_map[row['car_type']]
                car_list.append(car_class.create_from_dict(row))
            except (ValueError, KeyError):
                continue

    return car_list


car_list = get_car_list('car_base.csv')
