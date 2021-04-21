from notifications_python_client import NotificationsAPIClient
import yaml
import csv
from tqdm import tqdm


# Get config data
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
APIKEY = cfg["api_key"]
NEW_FORMAT = cfg["new"]
DEBUG = cfg["debug"]
TEMPLATE = cfg["template"]
VERSION = cfg["version"]

# Setup notify client and get failures
notifications_client = NotificationsAPIClient(APIKEY)
response = notifications_client.get_all_notifications(status='failed')


def setup_header():
    if NEW_FORMAT:
        notification_writer.writerow(["email address",
                                      "employerName",
                                      "applicationID",
                                      "claimantName",
                                      "vacancyTitle",
                                      "vacancyHolderName",
                                      "introductionId",
                                      "employerJobReference",
                                      "vacancyLocationCity",
                                      "vacancyLocationPostcode",
                                      "sentAtTime", "status"])
    else:
        notification_writer.writerow(["email address",
                                      "applicationID",
                                      "claimantName",
                                      "vacancyTitle",
                                      "vacancyHolderName",
                                      "introductionId",
                                      "employerJobReference",
                                      "vacancyLocationCity",
                                      "vacancyLocationPostcode",
                                      "sentAtTime", "status"])
    return ()


def extract_body(body):

    vacancy_holder_name_start = body.find("Dear") + 5
    vacancy_holder_name_end = body.find("\r\n", vacancy_holder_name_start)
    vacancyHolderName = body[vacancy_holder_name_start:vacancy_holder_name_end]
    introduction_id_start = body.find("Introduction ID:") + 17
    introduction_id_end = introduction_id_start + 9
    introductionId = body[introduction_id_start:introduction_id_end]
    employer_job_reference_start = body.find("your job reference:") + 20
    employer_job_reference_end = body.find("\r\n", employer_job_reference_start)
    employerJobReference = body[employer_job_reference_start:employer_job_reference_end]
    vacancyLocationCityStart = body.find("location:") + 10
    vacancyLocationCityEnd = body.find("\r\n", vacancyLocationCityStart)
    vacancyLocationCity = body[vacancyLocationCityStart:vacancyLocationCityEnd]
    vacancyLocationPostcodeStart = body.find("postcode:") + 10
    vacancyLocationPostcodeEnd = body.find("\r\n", vacancyLocationPostcodeStart)
    vacancyLocationPostcode = body[vacancyLocationPostcodeStart:vacancyLocationPostcodeEnd]


    return (vacancyHolderName, introductionId, employerJobReference, vacancyLocationCity, vacancyLocationPostcode)


# open file and write csv column names
with open("downloaded.csv", "w", newline='') as csvfilewriter:
    notification_writer = csv.writer(csvfilewriter, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    setup_header()

    # Parse data to isolate details from body and subject lines
    for i in tqdm(range(len(response['notifications']))):

        if DEBUG:
            print(response)

        employerName = ""
        originalEmailAddress = response['notifications'][i]['email_address']
        subject = response['notifications'][i]['subject']
        template_ID = response['notifications'][i]['template']['id']
        templateversion = response['notifications'][i]['template']['version']

        if templateversion == VERSION and template_ID == TEMPLATE:

            employerNameStart = subject.find("to")
            employerNameEnd = subject.find(",")
            employerName = subject[employerNameStart + 3:employerNameEnd]
            appIdStart = subject.find("KS")
            appId = subject[appIdStart:appIdStart + 10]
            claimantNameEnd = subject.find("for", appIdStart + 10)
            claimantName = subject[appIdStart + 12:claimantNameEnd - 1]
            vacancyTitle = subject[claimantNameEnd + 4:]
            body = response['notifications'][i]['body']
            sentAtTime = response['notifications'][i]['sent_at']


            vacancyHolderName, introductionId, employerJobReference, vacancyLocationCity, vacancyLocationPostcode = extract_body(body)

        else:
            appIdStart = subject.find("ID")
            appId = subject[appIdStart + 3:appIdStart + 13]
            claimantNameEnd = subject.find(",", appIdStart + 15)
            claimantName = subject[appIdStart + 15:claimantNameEnd]
            vacancyTitle = subject[claimantNameEnd + 2:]
            body = response['notifications'][i]['body']
            sentAtTime = response['notifications'][i]['sent_at']

            vacancyHolderName, introductionId, employerJobReference, vacancyLocationCity, vacancyLocationPostcode = extract_body(body)


            # write line
        if NEW_FORMAT:
            notification_writer.writerow([originalEmailAddress,
                                          employerName,
                                          appId,
                                          claimantName,
                                          vacancyTitle,
                                          vacancyHolderName,
                                          introductionId,
                                          employerJobReference,
                                          vacancyLocationCity,
                                          vacancyLocationPostcode,
                                          sentAtTime, response['notifications'][i]['status']])
        else:
            notification_writer.writerow([originalEmailAddress,
                                          appId,
                                          claimantName,
                                          vacancyTitle,
                                          vacancyHolderName,
                                          introductionId,
                                          employerJobReference,
                                          vacancyLocationCity,
                                          vacancyLocationPostcode,
                                          sentAtTime, response['notifications'][i]['status']])
    csvfilewriter.close()
print(f"File downloaded.csv created with {i+1} records")