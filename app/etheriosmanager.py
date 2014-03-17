import httplib
import base64
import xmlParse



class etheriosData:
    #username = "pgSatterlee" # enter your username
    #password = "Pgecs-2322" # enter your password
    username = "TestMe"
    password = "Password_123"
    auth = base64.encodestring("%s:%s"%(username,password))[:-1]
    def __init__(self):
        self.deviceListInfo = []
        self.streamListInfo = []

    #Group->Users
    #Group->Devices

    def setUserNamePassword(self,usern,passw):
        username = usern
        password = passw

    def setDeviceLocation(self,deviceID,lat,longit):
        message = """<DeviceCore>
              <devConnectwareId>{0}</devConnectwareId> 
                <dpMapLat>{1}</dpMapLat>
                <dpMapLong>{2}</dpMapLong>
            </DeviceCore>
            """.format(self.deviceID,lat,longit)
        self.genericWebServiceCall("/DeviceCore","PUT",message)

    def listDevices(self):
        response_body = self.genericWebServiceCall("/DeviceCore","GET")
        self.deviceListInfo = xmlParse.parseDeviceListing(response_body)
        return self.deviceListInfo
    def getUserList(self):
        pass

    def getControllerListing(self):
        pass

    def getStreamListData(self):
        response_body = self.genericWebServiceCall("/DataStream/","GET")
        self.streamListInfo = xmlParse.parseStreamListingXML(response_body)
        return self.streamListInfo

    def getDataStream(self,devID,dataStr):
        response_body = self.genericWebServiceCall("/DataPoint/{0}/{1}".format(devID,dataStr),"GET")
        print response_body
        return xmlParse.parseDataStreamXML(response_body)

    def getDeviceSettings(self,devID):
        message = """<sci_request version="1.0"> 
          <send_message cache="false"> 
            <targets> 
              <device id="%s"/> 
            </targets> 
            <rci_request version="1.1"> 
              <query_setting/></rci_request>
          </send_message></sci_request>"""%devID

        webservice = httplib.HTTP("login.etherios.com",80)
        # to what URL to send the request with a given HTTP method
        webservice.putrequest("POST", "/ws/sci")

        # add the authorization string into the HTTP header
        webservice.putheader("Authorization", "Basic %s"%self.auth)
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % len(message))
        webservice.endheaders()
        webservice.send(message)

    def genericWebServiceCall(self,request,getpost,message=""):
        print request
        webservice = httplib.HTTP("login.etherios.com",80)
        # to what URL to send the request with a given HTTP method
        webservice.putrequest(getpost, "/ws"+request)
        # add the authorization string into the HTTP header
        webservice.putheader("Authorization", "Basic %s"%self.auth)
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        if len(message):
            webservice.putheader("Content-length", "%d" % len(message))
        webservice.endheaders()
        if len(message):
            webservice.send(message)
        statuscode, statusmessage, header = webservice.getreply()
        response_body = webservice.getfile().read()
        return response_body
