from django.shortcuts import render,get_object_or_404
from django.views import generic

from Users.models import Organization

class ListView(generic.ListView):
    model=Organization
    context_object_name='org'
    template_name='Users/ListView.html'



def MainView(request):
    
    if request.method=='POST':
        search_term= request.POST.get('searched','')
        results= Organization.objects.filter(establishment_name__icontains=search_term)

        return render(request,'Search/MainView.html',{'search_term':search_term,'results':results})
    else:
        return render(request,'Search/MainView.html')
    

def DetailView(request,pk):
    org=get_object_or_404(Organization,pk=pk)
    return render(request,'Users/DetailView.html',{'org':org})