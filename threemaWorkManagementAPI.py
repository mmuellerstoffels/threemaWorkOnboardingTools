import requests

class ThreemaWorkManagementAPI:
    def __init__(self, apiKey, host='work.threema.ch', apiRoot='/api/v1'):
        self.url = "https://" + host + apiRoot
        self.headers = { 'X-API-KEY': apiKey }

    def getSubscription(self):
        '''
        THIS CALL DOES NOT SEEM TO WORK!
        Returns information about the subscription.
        :return: JSON
        '''
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

    # TODO
    def getShowUser(self, id):
        pass

    # TODO
    def deleteRevokeUser(self, id):
        pass

    # TODO
    def postUnlinkUser(self, id):
        pass

    #### CONTACTS ########
    # TODO
    def getShowContact(self, id):
        pass

    # TODO
    def putUpdateContact(self, id):
        pass

    # TODO
    def deleteRemoveContact(self, id):
        pass

    # TODO
    def getShowContacts(self, filterType, pageSize='20', page='0'):
        pass

    # TODO
    def postCreateContact(self):
        pass

    ##### THREEMA MDM #######
    # TODO
    def getTMDMCredentialShow(self, id, propertyId):
        pass

    # TODO
    def putTMDMCredentialUpdate(self, id, propertyId):
        pass

    # TODO
    def deleteTMDMGlobalRemove(self, id, propertyId):
        pass

    # TODO
    def getTMDMCredentialList(self, id):
        pass

    # TODO
    def postTMDMCredentialCreate(self, id):
        pass

    # TODO
    def getTMDMGlobalShow(self, propertyId):
        pass

    # TODO
    def putTMDMGlobalUpdate(self, propertyId):
        pass

    # TODO
    def deleteTMDMGlobalRemove(self, propertyId):
        pass

    # TODO
    def getTMDMGlobalList(self):
        pass

    # TODO
    def postTMDMGlobalCreate(self, mdmValue):
        pass

    ##### LOGOS ######

    def getShowLogos(self):
        '''
        Returns the location of the in-app logos.

        :return: JSON
        '''
        endpoint = self.url + "/logos"
        response = requests.get(endpoint, headers=self.headers)
        return response

    # TODO
    def putUpdateLogos(self, logosUpdate):
        pass


