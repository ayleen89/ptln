from django.db import models
import re
from datetime import datetime
# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers
    
    def get_distribution(self) -> list:
        distribution = []
        cant_rows = int(self.passengers/2)
        par = True
        if self.passengers % 2 == 1:
            cant_rows += 1
            par = False

        for x in range(cant_rows):
            if (x+1) == cant_rows and not par:
                taken = [True,False]
            else:
                taken = [True,True]
            distribution.append(taken)

        return distribution


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"
    
    def is_finished(self) -> bool:
        if self.end is None:
            return False
        else:
            return True


def validate_number_plate(number_plate):
    correct_valid = [False,True,True]
    list_number_plate = number_plate.split('-')
    if len(list_number_plate) == 3:
        is_valid = []
        for x in list_number_plate:  
            is_valid.append(bool(re.search(r'\d', x)))

        if is_valid == correct_valid:
            return True
        else:
            return False
    else:
        return False