from django import forms
from .models import Verse, Sorat, Quran


class QuranForm(forms.ModelForm):
    d={'---------':('---------','---------')}
    for i in list(Sorat.objects.all()):
        d[i.sid]=(i.sid,i.sorat_name)
    v={'---------':('---------','---------')}
    for i in list(Verse.objects.all()):
        v[i.v_lid]=(i.v_lid,i.v_lid)
    sorat_e = forms.ChoiceField(choices=d.values(), )
    verse_e=forms.ChoiceField(choices=v.values())

    class Meta:
        model = Quran
        fields = ('sorat','verse')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['verse'].queryset = Verse.objects.none()
#        self.fields['sorat_e'].queryset = Sorat.objects.all()
#        print(self.sorat_e)
#        self.fields['verse_e'].queryset = Verse.objects.none()