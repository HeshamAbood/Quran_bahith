from django import forms
from .models import Verse, Sorat, Quran


class QuranForm(forms.ModelForm):
    d={}
    for i in list(Sorat.objects.all()):
        d[i.sid]=(i.sid,i.sorat_name)
    v={}
    for i in list(Verse.objects.filter(v_sid=1)):
        v[i.v_lid]=(i.pk,i.v_lid)
    sorat_e = forms.ChoiceField(choices=d.values(), )
    verse_e=forms.ChoiceField(choices=v.values())

    class Meta:
        model = Quran
        fields = ('sorat','verse')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        v = {}
        for i in list(Verse.objects.filter(v_sid=1)):
            v[i.v_lid] = (i.pk, i.v_lid)
        self.fields['verse']=forms.ChoiceField(choices=v.values())
#        self.fields['sorat_e'].queryset = Sorat.objects.all()
#        print(self.sorat_e)
#        self.fields['verse_e'].queryset = Verse.objects.none()