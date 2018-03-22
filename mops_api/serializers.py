from mops_api.models import MOP, Operator
from rest_framework import serializers


class CoordinateField(serializers.Field):

    def to_representation(self, obj):
        ret = {
            "latitude": obj.x,
            "longitude": obj.y
        }
        return ret


class FacilitiesField(serializers.Field):

    def to_representation(self, obj):
        ret = {
            "lighting": obj.lighting,
            "garage": obj.garage,
            "dangerous_cargo_places": obj.dangerous_cargo_places,
            "car_wash": obj.car_wash,
            "fence": obj.fence,
            "sleeping_places": obj.sleeping_places,
            "monitoring": obj.monitoring,
            "security": obj.security,
            "toilets": obj.toilets,
            "restaurant": obj.restaurant,
            "petrol_station": obj.petrol_station,
        }
        return ret

class TakenField(serializers.Field):

    def to_representation(self, obj):
        ret = {
            "bus": obj.taken_bus_dedicated_places,
            "car": obj.taken_passenger_places,
            "truck": obj.taken_truck_places,
        }
        return ret

class AvailableField(serializers.Field):

    def to_representation(self, obj):
        ret = {
            "bus": obj.bus_dedicated_places,
            "car": obj.passenger_places,
            "truck": obj.truck_places,
        }
        return ret

class OperatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operator
        fields = ['email', 'name', 'phone']

class MOPSerializer(serializers.HyperlinkedModelSerializer):
    coords = CoordinateField(source='*')
    available = AvailableField(source='*')
    taken = TakenField(source='*')
    facilities = FacilitiesField(source='*')
    operator = OperatorSerializer(many=False, read_only=True)

    class Meta:
        model = MOP
        fields = ['id', 'title', 'coords', 'available', 'taken', 'facilities',
                  'chainage', 'direction', 'road_number', 'town', 'operator']


class TakenSerializer(serializers.HyperlinkedModelSerializer):
    taken = TakenField(source='*')
    class Meta:
        model = MOP
        fields = ['taken']
