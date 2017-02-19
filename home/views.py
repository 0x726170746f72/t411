from django.shortcuts import render


def homepage(request):
  try:
    from t411.settings import VERSION
  except Exception as e:
    VERSION = ''

  return render(request, 'index.html', {'version':VERSION})
