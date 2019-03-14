import os
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.endpoints import HTTPEndpoint

from FHIR.utilities import Utilities

create = Starlette()

"""
@api {post} /create/organization Populate a FHIR Organization template with the supplied values
@apiName CreateOrganization
@apiGroup Create

@apiParam {String} id Unique ID of this organization.
"""
@create.route("/organization")
class Organization(HTTPEndpoint):
    async def post(self, request):
        return Response("", Utilities.createFHIRResource("Organization", await request.body()), {}, "");

"""
@api {post} /create/practitioner Populate a FHIR Practitioner template with the supplied values
@apiName CreatePractitioner
@apiGroup Create

@apiParam {String} id Unique ID of this practitioner.
@apiParam {String} familyName  Practitioner family name.
@apiParam {String} givenName Practitioner given name.
"""
@create.route("/practitioner")
class Practitioner(HTTPEndpoint):
    async def post(self, request):
        return Response("", Utilities.createFHIRResource("Practitioner", await request.body()), {}, "");

"""
@api {post} /create/patient Populate a FHIR Patient template with the supplied values
@apiName CreatePatient
@apiGroup Create

@apiParam {String} id Unique ID of this patient.
@apiParam {String} title Patient title.
@apiParam {String} familyName Patient family name.
@apiParam {String} givenName Patient given name.
@apiParam {String} birthDate Patient date of birth.
@apiParam {String} organizationReference ID of Organization with which the patient is registered.
@apiParam {String} ethnicityCode Code used for patient ethnicity.
@apiParam {String} ethnicityDisplay Text associated with patient ethnicity.
"""
@create.route("/patient")
class Patient(HTTPEndpoint):
    async def post(self, request):
        return Response("", Utilities.createFHIRResource("Patient", await request.body()), {}, "");

"""
@api {post} /create/condition Populate a FHIR Condition template with the supplied values
@apiName CreateCondition
@apiGroup Create

@apiParam {String} id Unique ID of this condition.
@apiParam {String} codeSystem  Code system used for this condition.
@apiParam {String} code  Code used for this condition.
@apiParam {String} display  Text associated with this condition.
@apiParam {String} subjectReference  The ID of the patient to whom this condition pertains.
@apiParam {String} practitionerReference  The ID of the practitioner who diagnosed this condition.
"""
@create.route("/condition")
class Condition(HTTPEndpoint):
    async def post(self, request):
        return Response("", Utilities.createFHIRResource("Condition", await request.body()), {}, "");

"""
@api {post} /create/medication Populate a FHIR Medication template with the supplied values
@apiName CreateMedication
@apiGroup Create

@apiParam {String} id Unique ID of this medication.
@apiParam {String} codeSystem  Code system used for this medication.
@apiParam {String} code  Code used for this medication.
@apiParam {String} display  Text associated with this medication.
"""
@create.route("/medication")
class Medication(HTTPEndpoint):
    async def post(self, request):
        return Response("", Utilities.createFHIRResource("Medication", await request.body()), {}, "");

"""
@api {post} /create/dispense Populate a FHIR MedicationDispense template with the supplied values
@apiName CreateDispense
@apiGroup Create

@apiParam {String} id Unique ID of this dispense of medication.
@apiParam {String} medicationReference The ID of the medication involved in this dispense.
@apiParam {String} subjectReference The ID of the patient that is taking this medication.
@apiParam {String} practitionerReference The ID of the practitioner that prescribed this medication.
@apiParam {String} organizationReference The ID of the organization the practitioner is associated with.
"""
@create.route("/dispense")
class Dispense(HTTPEndpoint):
    async def post(self, request):
        print(os.getcwd());
        return Response("", Utilities.createFHIRResource("MedicationDispense", await request.body()), {}, "");

@create.route("/subscription")
class Subscription(HTTPEndpoint):
    async def post(self, request):
        print(os.getcwd());
        return Response("", Utilities.createFHIRResource("Subscription", await request.body()), {}, "");
