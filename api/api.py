import requests

class T411:
  token     = None
  base_url  = None

  '''API T411

  api t411
  '''
  def __init__(self, settings):
    if 'base_url' not in settings:
      raise Exception('aucune base_url n\'a été fournie à l\'API.')

    self.base_url = settings['base_url']

    if 'token' not in settings:
      self.auth(settings)
    else:
      self.token = settings['token']

  def auth(self, settings):
    if 'username' not in settings or 'password' not in settings:
      raise Exception('username ou password vide.')
    
    data      = {'username':settings['username'], 'password':settings['password']}
    r         = requests.post(self.base_url+'/auth', data=data) 
    response  = self.__check_request(r)
    
    if 'token' not in response:
      raise Exception('Aucun token renvoyé par l\'API.')
    
    self.token = response['token']
    return self.token


  '''CheckMinimumConfig'''
  def __cmc(self):
    return (self.token != None and self.base_url != None)


  '''Get auth headers'''
  def __get_auth_headers(self):
    return {'Authorization':str(self.token)}


  '''Vérifier si la requête n'a pas de soucis'''
  def __check_request(self, r):
    if r.status_code != 200:
      raise Exception('statut HTTP invalide : '+str(r.status_code))

    try:
      response = r.json()
    except Exception as e:
      raise Exception('Réponse invalide de l\'API (non JSON)')

    if 'error' in response:
      raise Exception('Une erreur a été renvoyée par l\'API: '+str(response['error'])+' (code '+str(response['code'])+')')   
    
    return response
  
  def search(self, q, offset=None, limit=None, cat=None):
    if not self.__cmc():
      raise Exception('API non initialisée correctement.')

    url   = '/torrents/search/'+str(q+'*')
    args  = {}
    if offset != None:
      args['offset']  = offset
    if limit != None:
      args['limit']   = limit
    if cat != None:
      args['cat']     = cat
    url += '?'+('&'.join([str(u)+'='+str(args[u]) for u in args]))
    
    r = requests.get(self.base_url+url, headers=self.__get_auth_headers())
    response = self.__check_request(r)
    return response

  def details(self, id):
    if not self.__cmc():
      raise Exception('API non initialisée correctement.')

    r = requests.get(self.base_url+'/torrents/details/'+str(id), headers=self.__get_auth_headers())
    response = self.__check_request(r)
    return response

  def download(self, id):
    if not self.__cmc():
      raise Exception('API non initialisée correctement.')

    r = requests.get(self.base_url+'/torrents/download/'+str(id), headers=self.__get_auth_headers(), stream=True)
    if r.status_code != 200:
      raise Exception('Téléchargement impossible. Code HTTP: '+str(r.status_code))
    if r.headers.get('content-type') != 'application/x-bittorrent':
      raise Exception('Téléchargement impossible. Aucun torrent trouvé.')
    
    data = r.raw.read(int(r.headers.get('content-length')))
    return data
    

