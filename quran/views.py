from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from functools import reduce
from .models import Sorat, Verse, Quran
from .forms import QuranForm

class SoratView(generic.ListView):
    template_name = "quran/index.html"
    model = Sorat
    def get_queryset(self):
#        self.load_all_sorat()
#        self.fix_count()
#        s=Sorat.objects.get(sid=5)
#        for sl in s.verse_set.all() :
#            sl.v_lid=int(sl.v_lid)-10
#            sl.save()
        return Sorat.objects.all()

    def fix_count(self):
        s=Sorat.objects.all()
        for sorat in s:
            for verse in sorat.verse_set.all():
#                print(verse.chars_count)
                verse.init_counts()
                verse.save()


    def load_all_sorat(self):
        try:
            # read the db file
            with open("quran/Sorat.txt", encoding='utf8') as fin:
                for line in fin:
                    print(line[:-1])
                    sorat_name, sid = line[:-1].split(",")
                    print(sorat_name,type(sorat_name))
                    print(type(sid), sid)
                    st = Sorat(sid=int(sid), sorat_name=sorat_name)
                    st.save()
                    print(st, "has been inserted")
        except FileNotFoundError as e:
            print("File doesn't found")



class DetailView(generic.DetailView):
    model = Sorat
    template_name = "quran/detail.html"


class VerseView(generic.ListView):
    template_name = "quran/verse_detail.html"
    model = Verse
    def get_queryset(self):
        query=self.request.GET.get("q")
#        self.load_all_verse()
        print("query is here ",self.kwargs)
        r=Verse.objects.filter(v_d_text__icontains=query)
        for verse in r:
            verse.set_text()

            print(verse.chars_count)
        return r

    def load_all_verse(self):
        try:
            # read the db file
            with open("quran/Verse.txt", encoding='utf8') as fin:
                for line in fin:
                    print(line[:-1])
                    sid,gid,lid,txt = line[:-1].split(",")
                    s=Sorat.objects.get(id=sid)
                    vrs = Verse(v_g_id=int(gid), v_sid=s,v_lid=int(lid),v_text=txt)
                    vrs.save()
                    print(vrs, "has been inserted")
        except FileNotFoundError as e:
            print("File doesn't found")

    def get_context_data(self, **kwargs):
        query = self.request.GET.get("q")
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print("query:", query)
        t1=[vr.v_d_text.split(" ") for vr in self.get_queryset()]
        result =[]
        result1 = []

#        print("here", type(t1[0]))
        for t in t1:
#            print("t", t)
            [result.append(i) for i in t for _ in range(i.count(query)) if i.count(query) > 0 ]
            [result1.append(i) for i in t if i.count(query) > 0 ]
        print("result ",len(result))
        context['Search_statistics'] = "عدد نتائج ايات البحث = "+str(len(self.get_queryset()))+"   , في         "+str(len(result1))+" كلمات,    "+ "عدد التكرار       " +str(len(result))
        result_s = set(result)
        context['words_statistics'] =[str(x+": "+str(result.count(x))) for x in result_s]
        if len(t1)==0:
            context['error_message']="لا يوجد نتائج مطابقة للبحث"
        return context

class VerseWordsView(generic.ListView):
    template_name = "quran/verse_words_detail.html"
    model = Verse


    def get_queryset(self):
        query=self.request.GET.get("w")
        print("query is here VerseWordsView",query)
        query=str(query).strip()
        r=Verse.objects.filter(v_d_text__icontains=query)
        for verse in r:
#            verse.init_counts()
#            verse.set_v_w_max_rpt(query)
#            verse.save()
            result =[]
            t1=verse.v_d_text.split(" ")
            [result.append(str(i+str(i.count(query)))) for i in t1  if i.count(query) > 0]
            verse.v_w_max_rpt=reduce(lambda a, b: a+', '+b, [x for x in result] )
#            verse.v_w_max_rpt=""
#            print(verse.v_g_id)
#            verse.save()
        return r

    def get_context_data(self, **kwargs):
        query = self.request.GET.get("w")
        query = str(query).strip()
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print("query:", query)
        t1=[vr.v_d_text.split(" ") for vr in self.get_queryset()]
        result =[]
        result1 = []

#        print("here", type(t1[0]))
        for t in t1:
#            print("t", t)
            [result.append(i) for i in t for _ in range(i.count(query)) if i.count(query) > 0 ]
            [result1.append(i) for i in t if i.count(query) > 0 ]
        print("result ",len(result))
        context['Search_statistics'] = "عدد نتائج ايات البحث = "+str(len(self.get_queryset()))+"   , في         "+str(len(result1))+" كلمات,    "+ "عدد التكرار       " +str(len(result))
        result_s = set(result)
        context['words_statistics'] =[str(x+": "+str(result.count(x))) for x in result_s]
        if len(t1)==0:
            context['error_message']="لا يوجد نتائج مطابقة للبحث"
        return context

class QuranSearcheView(generic.CreateView):
#    template_name = "quran/verse_search.html"
    template_name = "quran/quran_form.html"
    model = Quran
    form_class = QuranForm

    success_url = reverse_lazy('index')


    def get_context_data(self, **kwargs):
        query = self.request.GET.get("w")
        query = str(query).strip()
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print("query:", query)
        t1 = [vr.v_d_text.split(" ") for vr in self.get_queryset()]
        result = []
        result1 = []
        return context


    def load_verses(request):
        v_sid = request.GET.get('sorat')
        verses = Verse.objects.filter(v_sid=v_sid).order_by('v_lid')
        return render(request, 'quran/verse_dropdown_list_options.html', {'verses': verses})
