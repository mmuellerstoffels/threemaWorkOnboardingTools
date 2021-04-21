import requests

class ThreemaWorkManagementAPI:
    def __init__(self, apiKey, host='work.threema.ch', apiRoot='/api/v1'):
        self.url = "https://" + host + apiRoot
        self.headers = { 'X-API-KEY': apiKey }

    def getSubscription(self):
        endpoint = self.url + "/"
        response = requests.get(endpoint, headers=self.headers)
        return response

    #TODO
    def getShowCredential(self, id):
        pass

    def putUpdateCredential(self, id):
        pass

    def deleteRemoveCredential(self, id):
        pass

    def getListCredentials(self, pageSize='20', page='0'):
        '''
        TODO
        :param pageSize:
        :param page:
        :return:
        '''
        endpoint = self.url + "/credentials"
        params = {'pageSize': pageSize, 'page': page}
        response = requests.get(endpoint, params=params, headers=self.headers)
        return response

    #TODO
    def postCreateCredential(self, credentialUpdate):
        pass

    #### USERS #####
    # TODO
    def getListUsers(self, filterCredential, filterUsername, filterQuery, pageSize='20', page='0'):
        pass


