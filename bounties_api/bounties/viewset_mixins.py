from django.shortcuts import get_object_or_404

class CaseInsensitiveLookupMixin(object):
  def get_object(self):
    queryset = self.get_queryset()
    queryset = self.filter_queryset(queryset)
    filter = {self.lookup_field: self.kwargs[self.lookup_field].lower()}

    return get_object_or_404(queryset, **filter)
