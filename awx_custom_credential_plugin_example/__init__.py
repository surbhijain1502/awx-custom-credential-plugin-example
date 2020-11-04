import collections
from django.utils.translation import ugettext_lazy as _
import requests
import base64
CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

def handle_auth(**kwargs):
    token = None
    post_data = {
        "grant_type": "client_credentials", 
        "scope":"siem" 
    }
    post_header = {
     "Authorization": 'Basic ' + base64.b64encode(bytes(kwargs['client_id'] + ":" + kwargs['client_secret'], 'ascii')).decode('ascii')2
    }
    response = requests.post(
        endpoint,
        data = post_data,
        headers = post_header, 
        verify = True,
        proxies = {
         'https': proxy_url
        },
        timeout = (5, 30))
    print(response.text)



def get_ID(**kwargs):
    return 1


def get_Pwd(**kwargs):
    return 1

def centrify_backend(**kwargs):
    url = kwargs.get('url')
    acc_name = kwargs.get('account-name')
    system_name = kwargs.get('system-name')
    client_id = kwargs.get('client_id')
    client_password = kwargs.get('client_password')
    endpoint = urljoin(url,'/oauth2/token/oauthsiem')
    token = handle_auth(endpoint,client_id,client_password)
    acc_id = get_ID(token,system_name,acc_name)
    return get_Pwd(acc_id,token,url)

example_plugin = CredentialPlugin(
    'Example AWX Credential Plugin',
    # see: https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_types.html
    # inputs will be used to create a new CredentialType() instance
    #
    # inputs.fields represents fields the user will specify *when they create*
    # a credential of this type; they generally represent fields
    # used for authentication (URL to the credential management system, any
    # fields necessary for authentication, such as an OAuth2.0 token, or
    # a username and password). They're the types of values you set up _once_
    # in AWX
    #
    # inputs.metadata represents values the user will specify *every time
    # they link two credentials together*
    # this is generally _pathing_ information about _where_ in the external
    # management system you can find the value you care about i.e.,
    #
    # "I would like Machine Credential A to retrieve its username using
    # Credential-O-Matic B at identifier=some_key"
    inputs={
     'fields': [{
        'id': 'url',
        'label': _('PAS TENANT URL'),
        'type': 'string',
        'format': 'url',
     }, {
        'id': 'account-name',
        'label': _('Account Name'),
        'type': 'string',
        'secret': True,
     }, {
        'id': 'system-name',
        'label': _('System Name'),
        'type': 'string',
     }, {
         'id':'client_id',
         'label':_('PAS TENANT USER'),
         'type':'string',
     }, {
          'id':'client_password',
          'label':_('PAS TENANT PASSWORD'),
          'type':'string',
          'secret':True,
     }],
     'required': ['url', 'account-name', 'system-name','client_id','client_password'],
    },
    # backend is a callable function which will be passed all of the values
    # defined in `inputs`; this function is responsible for taking the arguments,
    # interacting with the third party credential management system in question
    # using Python code, and returning the value from the third party
    # credential management system
    backend = centrify_backend
)
