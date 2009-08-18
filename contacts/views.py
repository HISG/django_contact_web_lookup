from django.shortcuts import render_to_response, get_object_or_404
from dfs_contact_web_lookup.tiq_login import getSessionRpcClient
from dfs_contact_web_lookup.contacts.models import CachedContacts

def compare_by (fieldname):
   def compare_two_dicts (a, b):
      return cmp(a[fieldname], b[fieldname])
   return compare_two_dicts


def search(request):
   
   from forms import ContactSearchForm
   
   if request.method == 'POST':
      
      form = ContactSearchForm(request.POST)
      if form.is_valid():
         
         search_term = form.cleaned_data['search_term']
         
         sessionRpc = getSessionRpcClient(request.user.get_profile().session_id)
         results = sessionRpc.execute('addressBook.searchContacts', {'term': search_term})
         results.sort(compare_by(u'name'))
         # [{u'type': u'contact', u'id': 32516, u'name': u'Ann Harvey'}, ... ]
         return render_to_response('contacts/search_results.html', {'search_term': search_term, 'results':results, 'showlogout':True})
      
   else:
      form = ContactSearchForm()
   
   recent = CachedContacts.objects.order_by('last_viewed').reverse()[:5]
   favorite = CachedContacts.objects.order_by('viewed').reverse()[:5]
   
   return render_to_response('contacts/search.html', {'form': form, 'showlogout':True, 'recent':recent, 'favorite':favorite})


def detail(request, contact_id=None):
   
   if contact_id == None:
      form = ContactSearchForm()
      return render_to_response('contacts/search.html', {'form': form})

   
   sessionRpc = getSessionRpcClient(request.user.get_profile().session_id)
   
   contactDetails = sessionRpc.execute('addressBook.getContactDetails', {'id': contact_id})
   contactInfo = sessionRpc.execute('query.getContactInfo', {'id': contact_id})

   try:
       cc = CachedContacts.objects.get(contact_id=contact_id, user=request.user)
       cc.viewed = cc.viewed + 1
       cc.save()
   except CachedContacts.DoesNotExist:
       cc = CachedContacts()
       cc.user = request.user
       cc.contact_id = contact_id
       cc.contact_name = contactDetails['name']
       cc.viewed =  1
       cc.save()
       pass
   
   return render_to_response('contacts/detail.html', {'contactDetails': contactDetails, 'contactInfo': contactInfo, 'showlogout':True})
   
