from t411.local_settings import T411_SETTINGS
from django.http import HttpResponse
from django.utils.http import urlquote_plus
import requests, re
import bencodepy as bencode

'''extract_info_hash

Extraire l'info_hash directement depuis request.META['QUERY_STRING'],
car Django fait n'imp lors du decodage de l'URI.
'''
def extract_info_hash(query_string):
  m = re.search('info_hash=(?P<info_hash>[^&]+)', query_string)
  if not m:
    return None
  return m.groupdict()['info_hash']


'''scrape

Méthode `scrape`
Voir http://jonas.nitro.dk/bittorrent/bittorrent-rfc.html#anchor17
'''
def scrape(request):

  # extraction du info_hash
  info_hash = extract_info_hash(request.META['QUERY_STRING'])
  if info_hash == None:
    return failed_response('`info_hash` manquant!')
  url = T411_SETTINGS['tracker_url'] + 'scrape?info_hash='+info_hash
  
  # T411 capricieux...
  done = False
  for i in range(2):
    r = requests.get(url)
    if r.status_code != 200:
      continue
    done = True
  if not done:
    return failed_response('scrape a échoué: le tracker distant est indisponible.')
  return HttpResponse(r.text, content_type='text/plain')


'''announce

Méthode `announce`.
Voir http://jonas.nitro.dk/bittorrent/bittorrent-rfc.html#anchor17
'''
def announce(request):

  # dictionnaire des configurations de la requête.
  # On envoie rien de 'uploaded' ou 'downloaded' pour ne pas faire
  # bouger les stats sur t411
  settings = {'info_hash':'', 
              'peer_id':'',
              'port':'',
              }
  for val in settings:
    if val in request.GET:
      settings[val] = request.GET[val]
  
  settings['info_hash'] = extract_info_hash(request.META['QUERY_STRING'])

  # On a pas trouvé le info_hash ?
  if settings['info_hash'] == None:
    return failed_response('`info_hash` est manquant.!')
 
  # Création d'un faux peer_id
  # peer_id identifie un client BT
  if 'fake_btclient' in T411_SETTINGS:
    if len(T411_SETTINGS['fake_btclient']) != 20:
      raise Exception('T411_SETTINGS[\'fake_btclient\'] doit faire 20 caractères.')
    settings['peer_id'] = T411_SETTINGS['fake_btclient']
  else:
    # TODO: un programme qui en génère un aléatoirement
    settings['peer_id'] = '-UT1111-000000000001'

  # Nombre de pairs par défaut
  if 'default_nbr_peers' in T411_SETTINGS:
    if type(T411_SETTINGS['default_nbr_peers']) != int:
      raise Exception('T411_SETTINGS[\'default_nbr_peers\'] doit être un nombre')

    dnp = T411_SETTINGS['default_nbr_peers']
    if dnp < 0:
      raise Exception('T411_SETTINGS[\'default_nbr_peers\'] doit être compris entre 0 et infini compris.')
    settings['numwant'] = dnp
  else:
    settings['numwant'] = 75

  # Création de l'URI
  url = T411_SETTINGS['tracker_url'] + T411_SETTINGS['tracker_key'] + '/announce?info_hash='+settings['info_hash']+'&left=-1' 
  url +='&peer_id='+settings['peer_id']
  url += '&numwant='+str(settings['numwant'])
  url += '&port='+str(settings['port'])
  
  # le tracker de T411 est parfois capricieux
  done = False
  for i in range(2):
    r = requests.get(url, stream=True)
  
    # problème
    if r.status_code != 200:
      try:
        data = bencode.decode(r.raw.read(4096))
      except Exception as e:
        continue
        return failed_response('Le tracker distant a renvoyé une réponse illisible.')

      if 'failure reason' not in data:
        return failed_response('Le tracker distant est erroné.')

      return failed_response('Le tracker distant renvoie une erreur: '+str(data['failure reason']))
    else:
      done = True
  if done:
    data      = r.raw.read(4096)
    response  = HttpResponse(data, content_type='text/plain')
  else:
    response  =failed_response('Le tracker distant est indisponible pour le moment.')
  url = T411_SETTINGS['tracker_url'] + T411_SETTINGS['tracker_key'] + '/announce?info_hash='+settings['info_hash']+'&left=0&event=completed' 
  url +='&peer_id='+settings['peer_id']
  url += '&numwant='+str(settings['numwant'])
  url += '&port='+str(settings['port'])
  r = requests.get(url)
  return response

'''failed_response

Renvoyer un message d'erreur en respectant les conventions du protocole BT
'''
def failed_response(errstr):
  return HttpResponse(bencode.encode({'failure reason':errstr}), content_type='text/plain')

