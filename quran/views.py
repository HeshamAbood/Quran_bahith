import csv

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from functools import reduce
from .models import Sorat, Verse, Quran,Alphabet
from .forms import QuranForm
from django.core.paginator import Paginator


def trans(s):
    translation = {}
    for x in Alphabet.objects.all():
        translation[ord(x.char_name)] = ord(x.char_d_name)
    return s.translate(translation)

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
    paginate_by = 20

    def get_queryset(self):
        query=trans(self.request.GET.get("q"))
#        self.load_all_verse()
        print("query is here ",self.kwargs)
        r=Verse.objects.filter(v_d_text__icontains=query)
#        for verse in r:
#            verse.set_text()

#            print(verse.chars_count)
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
        query = trans(self.request.GET.get("q"))
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print("query:", query)
        t1=[vr.v_d_text.split(" ") for vr in self.get_queryset()]
        t2 = [vr.v_text.split(" ") for vr in self.get_queryset()]
        result =[]
        result1 = []

#        print("here", type(t1[0]))
        for a,t in enumerate(t1):
#            print("t", t)
            [result.append(t2[a][d]) for d, i in enumerate(t) for _ in range(i.count(query)) if i.count(query) > 0 ]
            [result1.append(t2[a][d]) for d, i in enumerate(t) if i.count(query) > 0 ]
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
    paginate_by = 20

    def get_queryset(self):
        query=trans(self.request.GET.get("w"))
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
        query = trans(self.request.GET.get("w"))
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

        if self.request.GET.get("page"):
            context.pop('page',None)
        return context

class QuranSearcheView(generic.CreateView):
#    template_name = "quran/verse_search.html"
    template_name = "quran/quran_form.html"
    model = Quran
    form_class = QuranForm
    paginate_by = 20

#    success_url = reverse_lazy('index')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.GET.get("f")):
            query = self.request.GET.get("f")
            # Call the base implementation first to get a context
            # Add in a QuerySet of all the books
            print("query:", query)
            s_from = 1
            s_to = 6236
            if self.request.GET.get("sorat") and self.request.GET.get("sorat") != "---------":
                s = self.request.GET.get("sorat")
                if self.request.GET.get("verse") and self.request.GET.get("verse") != "---------":
                    vf = int(self.request.GET.get("verse"))
                    s_from = (Verse.objects.get(v_sid=s, pk=vf)).v_g_id
                else:
                    s_from = Verse.objects.get(v_sid=s, v_lid=1).v_g_id

            if self.request.GET.get("sorat_e") and self.request.GET.get("sorat_e") != "---------":
                s = self.request.GET.get("sorat_e")
                if self.request.GET.get("verse_e") and self.request.GET.get("verse_e") != "---------":

                    vt = int(self.request.GET.get("verse_e"))
                    s_to = (Verse.objects.get(v_sid=s, pk=vt)).v_g_id
                else:
                    s_to = [v for v in Verse.objects.filter(v_sid=s)][-1].v_g_id
            if self.request.GET.get("options"):
                if int(self.request.GET.get("options"))==2:
                    qr = [v for v in Verse.objects.filter(v_d_text__istartswith=query) if
                      v.v_g_id >= s_from and v.v_g_id <= s_to]
                elif int(self.request.GET.get("options"))==3:
                    qr = [v for v in Verse.objects.filter(v_d_text__endswith=query) if
                          v.v_g_id >= s_from and v.v_g_id <= s_to]
                else:
                    qr = [v for v in Verse.objects.filter(v_d_text__icontains=query) if v.v_g_id >= s_from and v.v_g_id <= s_to]
            for verse in qr:
                verse.set_text()
            ## extract only specific query repetition count
            if (self.request.GET.get("qrpt")):
                print("before filter-len(qr):",len(qr))
                qr = [v for v in qr if v.v_d_text.count(query) == int(self.request.GET.get("qrpt"))]
                print("after filter-len(qr):", len(qr))

#                print("verse_id",verse.v_sid.sid)
            t1 = [vr.v_d_text.split(" ") for vr in qr]
            s=set([int(vq.v_sid.sid) for vq in qr])
            s_c=len(s)
            s_sum=sum(s)
            v_sum=sum([int(vq.v_lid) for vq in qr])
            result = []
            result1 = []

            #        print("here", type(t1[0]))
            for t in t1:
                #            print("t", t)
                [result.append(i) for i in t for _ in range(i.count(query)) if i.count(query) > 0]
                [result1.append(i) for i in t if i.count(query) > 0]
#            print("result ", len(result))
            context['Search_statistics'] = "عدد نتائج ايات البحث = " + str(
                len(qr)) + "   , في         " + str(
                len(result1)) + " كلمات,    " + "عدد التكرار       " + str(len(result))
            result_s = set(result)
            context['words_statistics'] = [str(x + ": " + str(result.count(x))) for x in result_s]
            context['s_c']=s_c
            context['s_sum'] = s_sum
            context['v_sum'] = v_sum

            if len(t1) == 0:
                context['error_message'] = "لا يوجد نتائج مطابقة للبحث"
            paginator = Paginator(qr, 20)
            if self.request.GET.get("page"):
                pn=self.request.GET.get("page")
                if pn>1:
#                    context["verse_list"] =paginator.page(pn)
                    context["verse_list"] = qr
            else:
#                    context["verse_list"] = paginator.page(1)
                    context["verse_list"] = qr

            s_result_count=0
            v_q_rpt={}
            for v in qr:
                c_r=v.v_d_text.count(query)
                s_result_count+=c_r
                if c_r in v_q_rpt.keys():
                    v_q_rpt[c_r]=v_q_rpt[c_r]+1
                else:
                    v_q_rpt[c_r]=1
            v_q_rpt={k: v for k, v in sorted(v_q_rpt.items(), key=lambda item: item[1])}
            context["v_q_rpt"] =list(v_q_rpt.items())
            context["s_result_count"] = s_result_count
        context["enter_s"] = "enter"

        return context


    def load_verses(request):
        v_sid = request.GET.get('sorat')
        verses = Verse.objects.filter(v_sid=v_sid).order_by('v_lid')
        return render(request, 'quran/verse_dropdown_list_options.html', {'verses': verses})

    def load_search_result( request):
        print("ajax_activated")
        print(request.GET.get("f"),request.GET.get("verse"),request.GET.get("sorat"),request.GET.get("verse_e"),request.GET.get("sorat_e"))
        if (request.GET.get("f")):
            query = request.GET.get("f")
            # Call the base implementation first to get a context
            # Add in a QuerySet of all the books
            print("query:", query)
            s_from = 1
            s_to = 6236
            if request.GET.get("sorat") and request.GET.get("sorat") != "---------":
                s = request.GET.get("sorat")
                if request.GET.get("verse") and request.GET.get("verse") != "---------":
                    vf = int(request.GET.get("verse"))
                    s_from = (Verse.objects.get(v_sid=s, pk=vf)).v_g_id
                else:
                    s_from = Verse.objects.get(v_sid=s, v_lid=1).v_g_id

            if request.GET.get("sorat_e") and request.GET.get("sorat_e") != "---------":
                s = request.GET.get("sorat_e")
                if request.GET.get("verse_e") and request.GET.get("verse_e") != "---------":

                    vt = int(request.GET.get("verse_e"))
                    s_to = (Verse.objects.get(v_sid=s, pk=vt)).v_g_id
                else:
                    s_to = [v for v in Verse.objects.filter(v_sid=s)][-1].v_g_id
            if request.GET.get("options"):
                if int(request.GET.get("options")) == 2:
                    qr = [v for v in Verse.objects.filter(v_d_text__istartswith=query) if
                          v.v_g_id >= s_from and v.v_g_id <= s_to]
                elif int(request.GET.get("options")) == 3:
                    qr = [v for v in Verse.objects.filter(v_d_text__endswith=query) if
                          v.v_g_id >= s_from and v.v_g_id <= s_to]
                else:
                    qr = [v for v in Verse.objects.filter(v_d_text__icontains=query) if
                          v.v_g_id >= s_from and v.v_g_id <= s_to]
            for verse in qr:
                verse.set_text()
                print(verse)

            if (request.GET.get("qrpt")):
                qr = [v for v in qr if v.v_d_text.count(query) == int(request.GET.get("qrpt"))]

            verse_list = qr

            t1 = [vr.v_d_text.split(" ") for vr in qr]
            s=set([int(vq.v_sid.sid) for vq in qr])
            s_c=len(s)
            s_sum=sum(s)
            v_sum=sum([int(vq.v_lid) for vq in qr])
            result = []
            result1 = []

            for t in t1:
                [result.append(i) for i in t for _ in range(i.count(query)) if i.count(query) > 0]
                [result1.append(i) for i in t if i.count(query) > 0]
            Search_statistics = "عدد نتائج ايات البحث = " + str(
                len(qr)) + "   , في         " + str(
                len(result1)) + " كلمات,    " + "عدد التكرار       " + str(len(result))
            result_s = set(result)
            words_statistics = [str(x + ": " + str(result.count(x))) for x in result_s]
            s_c=s_c
            s_sum = s_sum
            v_sum = v_sum

            if len(t1) == 0:
                error_message = "لا يوجد نتائج مطابقة للبحث"
            else:
                error_message=None

            s_result_count=0
            v_q_rpt={}
            for v in qr:
                c_r=v.v_d_text.count(query)
                s_result_count+=c_r
                if c_r in v_q_rpt.keys():
                    v_q_rpt[c_r]=v_q_rpt[c_r]+1
                else:
                    v_q_rpt[c_r]=1
            v_q_rpt={k: v for k, v in sorted(v_q_rpt.items(), key=lambda item: item[1])}
            v_q_rpt =list(v_q_rpt.items())
            s_result_count = s_result_count

        else:
            verse_list = None
            Search_statistics = None
            words_statistics = None
            s_c = None
            s_sum = None
            v_sum = None
            v_q_rpt = None
            s_result_count = None

        return render(request, 'quran/verse_search.html',
                      {'verse_list': verse_list,
                       'Search_statistics': Search_statistics,
                       'words_statistics': words_statistics,
                       's_c': s_c,
                       's_sum': s_sum,
                       'v_sum': v_sum,
                       'v_q_rpt':v_q_rpt,
                       's_result_count': s_result_count,
                       'error_message': error_message})

class QuranSearcheExport(generic.CreateView):
    def _get_csv(request, from_date, to_date):

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reports-%s/%s.csv"' % (from_date, to_date)

        for client in request.GET.getlist('client[]'):
            account = Sorat.objects.all().filter(
                client_id=client
            )[0]
            writer = csv.writer(response)
            writer.writerow([account.account_name])
            writer.writerow(['Date', 'Daily Total MBs'])
            company_report = sorted(client, from_date, to_date)
            company_report = sorted(company_report, key=lambda item: item['date'])
            for report in company_report:
                writer.writerow([report['date'], report['daily_totalmbs']])

        return response