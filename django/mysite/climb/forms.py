import django.forms

import climb.models

class route_create(django.forms.Form):
    name   = django.forms.CharField(max_length=256)

    location = django.forms.ModelChoiceField(queryset=climb.models.Location.objects.all(), required=False)
    area     = django.forms.ModelChoiceField(queryset=climb.models.Area.objects.all(), required=False)
    wall     = django.forms.ModelChoiceField(queryset=climb.models.Wall.objects.all(), required=False)
    
    def clean(self):
        cleaned_data = super(route_create, self).clean()

        location = cleaned_data.get("location")
        area     = cleaned_data.get("area")
        wall     = cleaned_data.get("wall")
       
        l = [location, area, wall]

        c = list(bool(f) for f in l).count(True)

        if c != 1:
            raise django.forms.ValidationError("must choose exavtly one of either location, area, or wall {}".format(l))
    


