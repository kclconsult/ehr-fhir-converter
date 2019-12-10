from __future__ import print_function
from builtins import str
from past.builtins import basestring
from builtins import object
from requests.auth import HTTPBasicAuth
import json, requests, configparser, os, base64

class Utilities(object):

  @staticmethod
  def callFHIRServer(url, method, body, username, password):

    request = requests.request(
      method,
      headers = {
       "Content-Type": "application/fhir+json; charset=UTF-8"
      },
      auth=HTTPBasicAuth(username, password),
      url=url,
      data=body,
      verify=True
    );

    if (request.status_code == 201):
      return 200;
    else:
      print("Error calling FHIR server. Status: " + str(request.status_code) + ". Details: " + str(request.content));
      return 400;

  @staticmethod
  def anonymise(resource, data):

    if resource == "Patient":

      if data['birthDate']:

        data['birthDate'] = data['birthDate'][0:4] + "-01-01";

    return data;

  @staticmethod
  def createFHIRResource(resource, data):

    config = configparser.ConfigParser();

    if 'FHIR_SERVER_ADDRESS' in os.environ:

      config.read('config/config.prod.ini');
      FHIR_HOST = config.get('FHIR_SERVER', 'URL', vars=os.environ);
      FHIR_USERNAME = config.get('FHIR_SERVER', 'USERNAME', vars=os.environ);
      FHIR_PASSWORD = config.get('FHIR_SERVER', 'PASSWORD', vars=os.environ);

    else:

      config.read('config/config.dev.ini');
      FHIR_HOST = config.get('FHIR_SERVER', 'URL');
      FHIR_USERNAME = config.get('FHIR_SERVER', 'USERNAME');
      FHIR_PASSWORD = config.get('FHIR_SERVER', 'PASSWORD');

    data = Utilities.anonymise(resource, json.loads(data));

    with open("FHIR/fhir-json/templates/" + resource + ".json") as templateFile:

      template = templateFile.read();

      for key, value in data.items():
        template = template.replace("[" + key + "]", value);

      URL = FHIR_HOST + config['FHIR_SERVER']['ENDPOINT'] + resource + "/" + data["id"] + "?_format=json";

      return Utilities.callFHIRServer(URL, "PUT", template, FHIR_USERNAME, FHIR_PASSWORD);
