from django.test import TestCase

from rest_framework.exceptions import ValidationError

from .models import Category, Shape, Weight
from .serializers import CakeSerializer, CategoryField, ShapeField, WeightField


class CakeRelatedFieldTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Birthday cake")
        self.shape = Shape.objects.create(name="Round")
        self.weight = Weight.objects.create(name="1 kg")

    def test_related_fields_accept_names(self):
        for field_class, model, instance in (
            (CategoryField, Category, self.category),
            (ShapeField, Shape, self.shape),
            (WeightField, Weight, self.weight),
        ):
            with self.subTest(field=field_class.__name__):
                field = field_class(queryset=model.objects.all())
                self.assertEqual(field.run_validation(instance.name), instance)

    def test_related_fields_accept_primary_keys(self):
        for field_class, model, instance in (
            (CategoryField, Category, self.category),
            (ShapeField, Shape, self.shape),
            (WeightField, Weight, self.weight),
        ):
            with self.subTest(field=field_class.__name__):
                field = field_class(queryset=model.objects.all())
                self.assertEqual(field.run_validation(instance.pk), instance)

    def test_unknown_related_name_returns_validation_error(self):
        field = CategoryField(queryset=Category.objects.all())

        with self.assertRaises(ValidationError):
            field.run_validation("Unknown category")

    def test_cake_serializer_accepts_related_record_names(self):
        serializer = CakeSerializer(
            data={
                "category": self.category.name,
                "shape": self.shape.name,
                "weight": self.weight.name,
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["category"], self.category)
        self.assertEqual(serializer.validated_data["shape"], self.shape)
        self.assertEqual(serializer.validated_data["weight"], self.weight)

    def test_cake_serializer_accepts_related_record_ids(self):
        serializer = CakeSerializer(
            data={
                "category": self.category.pk,
                "shape": self.shape.pk,
                "weight": self.weight.pk,
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["category"], self.category)
        self.assertEqual(serializer.validated_data["shape"], self.shape)
        self.assertEqual(serializer.validated_data["weight"], self.weight)
