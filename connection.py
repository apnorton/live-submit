import requests
from bs4 import BeautifulSoup

##
# This object acts as an interface to the live archive
##
class LAConnection:
  archive_url = 'https://icpcarchive.ecs.baylor.edu/index.php'
  login_form  = '?option=com_comprofiler&task=login'
  submit_form = '?option=com_onlinejudge&Itemid=25'

  def __init__(self, uname, pword):
    self.uname   = uname
    self.pword   = pword
    self.session = requests.Session()

    # Perform the login request
    self.login()

  def login(self):
    s = self.session
    print('Performing login...')

    # Get data from login page to spoof being a real user
    homepage = s.get(self.archive_url)
    soup = BeautifulSoup(homepage.text, 'html.parser')
    hiddenInputs = soup.findAll(name='input', type='hidden')

    payload = { 'username':self.uname, 'passwd':self.pword, 'remember':'yes' }
    for hidden in hiddenInputs:
      if hidden['name'] != 'option' and hidden['value'] != 'search':
        payload[hidden['name']] = hidden['value']

    headers = { 'User-Agent':'Mozilla/5.0', 'Referrer':'https://icpcarchive.ecs.baylor.edu/index.php' }
    self.session.post(LAConnection.archive_url+LAConnection.login_form, data=payload).text

    # TODO check to see if this actually logged in with some confirmation page
    print('Login complete.')
