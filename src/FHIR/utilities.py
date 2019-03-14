from __future__ import print_function
from builtins import str
from past.builtins import basestring
from builtins import object
import json, requests

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
      #rejectUnauthorized: false,
      #requestCert: true,
      data=body
    );

    if (request.status_code == 201):
      return 200;
    else:
      return 400;


  @staticmethod
  def createFHIRResource(resource, data):

    data = json.loads(data);

    with open("FHIR/fhir-json/templates/" + resource + ".json") as templateFile:

      template = templateFile.read();

      for key, value in data.items():
        template = template.replace("[" + key + "]", value);

      return Utilities.callFHIRServer("http://localhost:8080/fhir/" + resource + "/" + data["id"] + "?_format=json", "PUT", template);
