from django.db import models
import json
from functools import reduce



def trans(s):
    translation = {}
    for x in Alphabet.objects.all():
        translation[ord(x.char_name)] = ord(x.char_d_name)
    return s.translate(translation)


d = {}
ad={"ا": 0, "ب": 0, "ج": 0, "د": 0, "ه": 0, "و": 0, "ز": 0, "ح": 0, "ط": 0, "ي": 0, "ك": 0, "ل": 0, "م": 0, "ن": 0, "س": 0, "ع": 0, "ف": 0, "ص": 0, "ق": 0, "ر": 0, "ش": 0, "ت": 0, "ث": 0, "خ": 0, "ذ": 0, "ض": 0, "ظ": 0, "غ": 0, "أ": 0, "إ": 0,  "ء": 0, "ئ": 0, "ى": 0, "ؤ": 0, " ": 0, "ة": 0,"آ":0}
for i, x in enumerate("ابجدهوزحطيكلمنسعفصقرشتثخذضظغأءئىؤآإ ة"):
    if x in["أ","ء","ى","ئ","إ","آ"]:
        d[x]=1
    elif x =="ؤ":
        d[x] = 6
    elif x =="غ":
        d[x] = 1000
    elif x== " ":
        d[x] = 0
    elif x=="ة":
        d[x] = 400
    elif x=="ق":
        d[x] = 100
    elif x in "كلمنسعفص":
        d[x] = ((i%9)+1)*10
    elif x in "رشتثخذضظ":
        d[x] = ((i%19)+2)*100
    else:
        d[x] = i + 1

class Alphabet(models.Model):
    char_name = models.CharField(max_length=10)
    char_d_name = models.CharField(max_length=10)
    char_vlaue = models.IntegerField()

    def __str__(self):
        return str(self.pk)+" "+str(self.char_name)

class Sorat(models.Model):
    sid = models.IntegerField()
    sorat_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.sorat_name)


class Verse(models.Model):
    v_g_id = models.IntegerField(default=0)
    v_sid = models.ForeignKey(Sorat, on_delete=models.CASCADE, help_text="Sorat", )
    v_lid = models.IntegerField(default=0)
    v_text = models.TextField(max_length=10000,default="",null=True)
    v_d_text = models.TextField(max_length=10000, default="", null=True)
    chars_count = models.CharField(max_length=10000, default=ad, null=True, db_column=None)
    chars_count_d = models.CharField(max_length=10000, default="", null=True, db_column=None)
    v_words_count = models.IntegerField(default=0, null=True, db_column=None)
    v_joumla_sum= models.IntegerField(default=0, null=True, db_column=None)
    v_words=models.CharField(max_length=10000, default="", null=True, db_column=None)
    v_w_max_rpt = models.CharField(max_length=100, default="", null=True, db_column=None)


    def init_counts(self):
        self.set_text()
        self.count_words()
        self.jomal_calculate()

    def set_text(self):
        self.v_d_text=""
        t={}
        for x in Alphabet.objects.all():
           t[x.char_name]=x.char_d_name
        for c in self.v_text:
            if c in t.keys():
                self.v_d_text+=t[c]
#        print("type(ad) ",type(ad))
#        print("type(self.chars_count) ",type(self.chars_count))
        self.chars_count={}
#        print("type(self.chars_count) after load ", type(self.chars_count))
        for k in self.v_d_text:
            if k in self.chars_count.keys():
                self.chars_count[k]+=1
            else:
                self.chars_count[k] = 1

        self.chars_count_d='<table class="table col-sm-8 col-md-10"> <thead> <tr>'
        self.chars_count_d += '<th>' + 'عدد<br>الحروف' + '</th>'
        self.chars_count_d += '<th>' + 'مجموع<br>الحروف' + '</th>'
        for k in self.chars_count.keys():
            if k!=" ":
                self.chars_count_d += '<th>'+ str(k)+ '</th>'

        self.chars_count_d +='</tr> </thead> <tbody> <tr>'
        self.chars_count_d += '<td>' + str(len([ x for x in self.chars_count if x in "ابجدهوزحطيكلمنسعفصقرشتثخذضظغأءىؤإآة"])) + '</td>'
        self.chars_count_d += '<td>' + str(self.get_chars_count()) + '</td>'
        for k in self.chars_count.keys():
            if k != " ":
                self.chars_count_d += '<td>'+ str(self.chars_count[k])+ '</td>'
        self.chars_count_d += '</tr> </tbody> </table>'


    def count_words(self):
        print("count words",self.v_g_id)
        self.v_words=self.v_text.split(" ")
        self.v_words_count=len(self.v_words)
        return self.v_words_count

    def get_chars_count(self):
        s = [0]
        for c,r in self.chars_count.items():
            if c in "ابجدهوزحطيكلمنسعفصقرشتثخذضظغأءىؤإآة":
                s[0]+=r
        return s[0]

    def jomal_calculate(self):
        s=[0]
        for c,r in self.chars_count.items():
            s[0]+=d[c]*r
        self.v_joumla_sum=s[0]
        return s[0]

    def set_v_w_max_rpt(self, c):
        m=[]
        for word in self.v_words:
            if word.count(c)>0:
                for i in range(word.count(c)):
                    m.append(word)

        self.v_w_max_rpt="عدد التكرار: "+str(len(m))+" \n"+ reduce(lambda a, b: a+', '+b, [x for x in m] )
#        print(self.v_w_max_rpt)

    def __str__(self):
        return self.v_text

class Quran(models.Model):
    name = models.CharField(max_length=200)
    sorat=models.ForeignKey(Sorat,null=True, on_delete=models.SET_NULL, default=1)
    verse=models.ForeignKey(Verse , null=True, on_delete=models.SET_NULL)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def __str__(self):
        return str(self.name)