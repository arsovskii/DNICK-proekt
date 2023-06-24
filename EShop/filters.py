import django_filters
from django.forms import CheckboxInput
from django_filters.widgets import RangeWidget, BooleanWidget

from EShop.models import Product


class ProductFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)

        for field in self.form:
            field.field.widget.attrs["id"] = "genre-select"
            field.field.widget.attrs["class"] = "form-select"

    class Meta:
        model = Product
        fields = ["genre"]
