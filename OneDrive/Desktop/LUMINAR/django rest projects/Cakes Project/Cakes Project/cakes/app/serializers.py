from rest_framework import serializers

from .models import Cakes,Category,Shape,Weight

class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = '__all__'

class ShapeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Shape

        fields = '__all__'

class WeightSerializer(serializers.ModelSerializer):

    class Meta:

        model = Weight

        fields = '__all__'

class NamedPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    default_error_messages = {
        'does_not_exist': 'No matching record with name "{name}".',
    }

    def to_internal_value(self, data):
        if isinstance(data, str) and not data.isdecimal():
            queryset = self.get_queryset()
            try:
                return queryset.get(name=data)
            except queryset.model.DoesNotExist:
                self.fail('does_not_exist', name=data)

        return super().to_internal_value(data)


class CategoryField(NamedPrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0])

    def to_representation(self,value):

        return CategorySerializer(value).data
    
class ShapeField(NamedPrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0])

    def to_representation(self,value):

        return ShapeSerializer(value).data
    
class WeightField(NamedPrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0])

    def to_representation(self,value):

        return WeightSerializer(value).data

class CakeSerializer(serializers.ModelSerializer):

    category = CategoryField(queryset=Category.objects.all())

    shape = ShapeField(queryset=Shape.objects.all())

    weight = WeightField(queryset=Weight.objects.all())

    status = serializers.SerializerMethodField()

    def get_status(self, obj):

        if obj.price < 1000:

            return 'max saver'

        return None

    class Meta:

        model = Cakes

        # fields = ['name','description','photo']
        fields = '__all__'
        # exclude = ''