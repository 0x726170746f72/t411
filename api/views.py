from django.shortcuts import render
from django.http import HttpResponse
from api.api import T411
from api.models import Token
from torrent_editor.torrent import Torrent
from time import time as ts
from t411.local_settings import T411_SETTINGS

import json

def error_response(errstr):
  data = {'errstr':str(errstr)}  
  response = HttpResponse(json.dumps(data), content_type='application/json')
  return response

def load_token():
  tokens = Token.objects.filter(ts__gte=ts())
  if len(tokens) == 0:
    settings = T411_SETTINGS
    try:
      t411 = T411(settings)
    except Exception as e:
      raise e
    t = Token(token=t411.token, ts=ts()+3600*24*90)
    t.save()
    token = t411.token
  else:
    token = tokens[0].token
  return token

def get_api():
  token = load_token()
  return T411({'token': token, 'base_url':T411_SETTINGS['base_url']})

def search(request):
  if 'q' not in request.GET:
    return error_response('`q` inexistant.')
  q = request.GET['q'][0:64]
  args = {'offset':None, 'limit': None, 'cat': None}
  for a in args:
    if a in request.GET:
      args[a] = request.GET
  
  if args['limit'] == None:
    args['limit'] = 300

  try:
    t411 = get_api()
    response  = t411.search(q, offset=args['offset'], limit=args['limit'], cat=args['cat'])
  except Exception as e:
    return error_response(str(e))
   
  return HttpResponse(json.dumps(response), content_type='application/json')

def download(request, id, name):
  print("download "+str(id)+" ("+str(name)+")")
  try:
    t411 = get_api()
    data = t411.download(id)
  except Exception as e:
    return error_response(str(e))

  try:
    t = Torrent(data)
    t.set_tracker(request.scheme + '://'+request.META['HTTP_HOST']+'/announce')
    t.set_comment('Téléchargé avec t411_unblocked')
    t.set_author('t411_unblocked')
    data = t.build()
  except Exception as e:
    return error_response(str(e))

  response = HttpResponse(data, content_type="application/x-bittorrent")
  response['Content-Disposition'] = 'attachment; filename="'+str(name).replace('\n','')+'-[t411_unblocked].torrent"'
  return response

