from notifications_python_client import NotificationsAPIClient
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
APIKEY = cfg["api_key"]

notifications_client = NotificationsAPIClient(APIKEY)

response = notifications_client.get_all_notifications(status='permanent-failure')


for i in range(len(response['notifications'])):
        originalEmailAddress = response['notifications'][i]['email_address']
        print(originalEmailAddress)
        subject = response['notifications'][i]['subject']
        appIdStart = subject.find("ID")
        appId = subject[appIdStart+3:appIdStart+13]
        print(appId)

        claimantNameEnd = subject.find(",", appIdStart+15)
        claimantName = subject[appIdStart+15:claimantNameEnd]
        print(claimantName)

        vacancyTitle = subject[claimantNameEnd+2:]
        print(vacancyTitle)

        body = response['notifications'][i]['body']
        vacancyHolderNameStart = body.find("Dear")+5
        vacancyHolderNameEnd = body.find("\r\n", vacancyHolderNameStart)
        vacancyHolderName = body[vacancyHolderNameStart:vacancyHolderNameEnd]
        print(vacancyHolderName)

        introductionIdStart = body.find("Introduction ID:")+17
        introductionIdEnd = introductionIdStart+9
        introductionId = body[introductionIdStart:introductionIdEnd]
        print(introductionId)

        employerJobReferenceStart = body.find("your job reference:")+20
        employerJobReferenceEnd = body.find("\r\n", employerJobReferenceStart)
        employerJobReference = body[employerJobReferenceStart:employerJobReferenceEnd]
        print(employerJobReference)

        vacancyLocationCityStart = body.find("location:")+10
        vacancyLocationCityEnd = body.find("\r\n", vacancyLocationCityStart)
        vacancyLocationCity = body[vacancyLocationCityStart:vacancyLocationCityEnd]
        print(vacancyLocationCity)

        vacancyLocationPostcodeStart = body.find("postcode:")+10
        vacancyLocationPostcodeEnd = body.find("\r\n", vacancyLocationPostcodeStart)
        vacancyLocationPostcode = body[vacancyLocationPostcodeStart:vacancyLocationPostcodeEnd]
        print(vacancyLocationPostcode)
        sentAtTime = response['notifications'][i]['sent_at']
        print(sentAtTime)






#notifications_client = NotificationsAPIClient('test-592e9258-8b62-47a9-bd21-72aa1f22219a-b0e1e234-80d7-455c-a07d-3ed6c9aceff1')

