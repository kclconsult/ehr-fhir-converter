from __future__ import print_function
from builtins import str
from past.builtins import basestring
from builtins import object
import json, requests, configparser, os

class Utilities(object):

  @staticmethod
  def callFHIRServer(url, method, body):

    request = requests.request(
      method,
      headers = {
       #"Authorization": "Basic " + new Buffer(config.FHIR_USERNAME + ":" + config.FHIR_PASSWORD).toString("base64"),
       "Content-Type": "application/fhir+json; charset=UTF-8"
      },
      url=url,
      data=body
    );

    if (request.status_code == 201):
      return 200;
    else:
      return 400;


  @staticmethod
  def createFHIRResource(resource, data):

    config = configparser.ConfigParser();

    if 'FHIR_SERVER_ADDRESS' in os.environ:

      config.read('config/config.prod.ini');
      FHIR_HOST = config.get('FHIR_SERVER', 'URL', vars=os.environ);

    else:

      config.read('config/config.dev.ini');
      FHIR_HOST = config.get('FHIR_SERVER', 'URL');

    data = json.loads(data);

    with open("FHIR/fhir-json/templates/" + resource + ".json") as templateFile:

      template = templateFile.read();

      for key, value in data.items():
        template = template.replace("[" + key + "]", value);

      URL = FHIR_HOST + config['FHIR_SERVER']['ENDPOINT'] + resource + "/" + data["id"] + "?_format=json";

      return Utilities.callFHIRServer(URL, "PUT", template);
