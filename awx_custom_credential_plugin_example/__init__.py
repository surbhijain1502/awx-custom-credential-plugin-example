from .plugin import CredentialPlugin, raise_for_status
import collections
from django.utils.translation import ugettext_lazy as _
import requests
import base64
CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

pas_inputs = {
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
}

def handle_auth(**kwargs):
    token = None
    post_data = {
        "grant_type": "client_credentials", 
        "scope":"siem" 
    }
    post_header = {
     "Authorization": 'Basic ' + base64.b64encode(bytes(kwargs['client_id'] + ":" + kwargs['client_secret'], 'ascii')).decode('ascii')
    }
    response = requests.post(
        endpoint,
        data = post_data,
        headers = post_header, 
        verify = True,
        proxies = {
         'https': proxy_url
        },
        timeout = (5, 30)
    )
    raise_for_status(response)
    print(response.text)
    tokens = json.loads(response.text)
    return tokens['access_token']



def get_ID(**kwargs):
    endpoint = urljoin(kwargs['url'],'/Redrock/query')
    post_data = json.dumps({'Script': query})
    post_headers = {
        "Authorization": "Bearer " + access_token, 
        "X-CENTRIFY-NATIVE-CLIENT":"true"
    }
    response = requests.post(
        endpoint,
        data = post_data,
        headers = post_headers, 
        proxies = {
           'https': proxy_url
        },
        timeout = (5, 30)
    )
    raise_for_status(response)
    tokens = json.loads(response.text)
    result_str=tokens["Result"]["Results"]
    acc_ID=result_str[0]["Row"]["ID"]
    raise_for_status(response)
    return acc_ID

def get_Pwd(**kwargs):
    endpoint = urljoin(kwargs['url'],'/ServerManage/CheckoutPassword')
    post_data = json.dumps({'ID': kwargs['acc_ID']})
    response = requests.post(
        endpoint,
        data = post_data,
        headers = post_headers,
        proxies = {
         'https': proxy_url
        },
        timeout = (5, 30)
    )
    raise_for_status(response)
    print(response.text)
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
    inputs=pas_inputs,
    backend = centrify_backend
)
