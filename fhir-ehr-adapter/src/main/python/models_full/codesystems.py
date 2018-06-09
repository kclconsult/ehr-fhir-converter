#
#  CodeSystems.py
#  client-py
#
#  Generated from FHIR 1.8.0.10521 on 2018-01-16.
#  2018, SMART Health IT.
#
#  THIS HAS BEEN ADAPTED FROM Swift Enums WITHOUT EVER BEING IMPLEMENTED IN
#  Python, FOR DEMONSTRATION PURPOSES ONLY.
#


class AbstractType(object):
	""" A type defined by FHIR that is an abstract type

	URL: http://hl7.org/fhir/abstract-types
	ValueSet: http://hl7.org/fhir/ValueSet/abstract-types
	"""
	
	type = "Type"
	""" A place holder that means any kind of data type
	"""
	
	any = "Any"
	""" A place holder that means any kind of resource
	"""



class AccountStatus(object):
	""" Indicates whether the account is available to be used.

	URL: http://hl7.org/fhir/account-status
	ValueSet: http://hl7.org/fhir/ValueSet/account-status
	"""
	
	active = "active"
	""" This account is active and may be used.
	"""
	
	inactive = "inactive"
	""" This account is inactive and should not be used to track financial information.
	"""
	
	enteredInError = "entered-in-error"
	""" This instance should not have been part of this patient's medical record.
	"""



class ActionList(object):
	""" List of allowable action which this resource can request.

	URL: http://hl7.org/fhir/actionlist
	ValueSet: http://hl7.org/fhir/ValueSet/actionlist
	"""
	
	cancel = "cancel"
	""" Cancel, reverse or nullify the target resource.
	"""
	
	poll = "poll"
	""" Check for previously un-read/ not-retrieved resources.
	"""
	
	reprocess = "reprocess"
	""" Re-process the target resource.
	"""
	
	status = "status"
	""" Retrieve the processing status of the target resource.
	"""



class ActivityDefinitionCategory(object):
	""" High-level categorization of the type of activity in a protocol.

	URL: http://hl7.org/fhir/activity-definition-category
	ValueSet: http://hl7.org/fhir/ValueSet/activity-definition-category
	"""
	
	communication = "communication"
	""" To communicate with a participant in some way
	"""
	
	device = "device"
	""" To use a specific device
	"""
	
	diagnostic = "diagnostic"
	""" To perform a particular diagnostic
	"""
	
	diet = "diet"
	""" To consume food of a specified nature
	"""
	
	drug = "drug"
	""" To consume/receive a drug or other product
	"""
	
	encounter = "encounter"
	""" To meet with the patient (in-patient, out-patient, etc.)
	"""
	
	immunization = "immunization"
	""" To administer a particular immunization
	"""
	
	observation = "observation"
	""" To capture information about a patient (vitals, labs, etc.)
	"""
	
	procedure = "procedure"
	""" To modify the patient in some way (surgery, physiotherapy, education, counseling, etc.)
	"""
	
	referral = "referral"
	""" To refer the patient to receive some service
	"""
	
	supply = "supply"
	""" To provide something to the patient (medication, medical supply, etc.)
	"""
	
	vision = "vision"
	""" To receive a particular vision correction device
	"""
	
	other = "other"
	""" Some other form of action
	"""



class AddressType(object):
	""" The type of an address (physical / postal)

	URL: http://hl7.org/fhir/address-type
	ValueSet: http://hl7.org/fhir/ValueSet/address-type
	"""
	
	postal = "postal"
	""" Mailing addresses - PO Boxes and care-of addresses.
	"""
	
	physical = "physical"
	""" A physical address that can be visited.
	"""
	
	both = "both"
	""" An address that is both physical and postal.
	"""



class AddressUse(object):
	""" The use of an address

	URL: http://hl7.org/fhir/address-use
	ValueSet: http://hl7.org/fhir/ValueSet/address-use
	"""
	
	home = "home"
	""" A communication address at a home.
	"""
	
	work = "work"
	""" An office address. First choice for business related contacts during business hours.
	"""
	
	temp = "temp"
	""" A temporary address. The period can provide more detailed information.
	"""
	
	old = "old"
	""" This address is no longer in use (or was never correct, but retained for records).
	"""



class AdministrativeGender(object):
	""" The gender of a person used for administrative purposes.

	URL: http://hl7.org/fhir/administrative-gender
	ValueSet: http://hl7.org/fhir/ValueSet/administrative-gender
	"""
	
	male = "male"
	""" Male
	"""
	
	female = "female"
	""" Female
	"""
	
	other = "other"
	""" Other
	"""
	
	unknown = "unknown"
	""" Unknown
	"""



class AggregationMode(object):
	""" How resource references can be aggregated.

	URL: http://hl7.org/fhir/resource-aggregation-mode
	ValueSet: http://hl7.org/fhir/ValueSet/resource-aggregation-mode
	"""
	
	contained = "contained"
	""" The reference is a local reference to a contained resource.
	"""
	
	referenced = "referenced"
	""" The reference to a resource that has to be resolved externally to the resource that includes the reference.
	"""
	
	bundled = "bundled"
	""" The resource the reference points to will be found in the same bundle as the resource that includes the
	/// reference.
	"""



class AllergyIntoleranceCategory(object):
	""" Category of an identified substance.

	URL: http://hl7.org/fhir/allergy-intolerance-category
	ValueSet: http://hl7.org/fhir/ValueSet/allergy-intolerance-category
	"""
	
	food = "food"
	""" Any substance consumed to provide nutritional support for the body.
	"""
	
	medication = "medication"
	""" Substances administered to achieve a physiological effect.
	"""
	
	biologic = "biologic"
	""" A preparation that is synthesized from living organisms or their products, especially a human or animal protein,
	/// such as a hormone or antitoxin, that is used as a diagnostic, preventive, or therapeutic agent. Also called
	/// biological drug. Examples of biologic medications include: vaccines; allergenic extracts, which are used for
	/// both diagnosis and treatment (for example, allergy shots); gene therapies; cellular therapies.  There are other
	/// biologic products, such as tissues, that are not typically associated with allergies.
	"""
	
	environment = "environment"
	""" Any substances that are encountered in the environment, including any substance not already classified as food,
	/// medication, or biologic.
	"""



class AllergyIntoleranceCertainty(object):
	""" Statement about the degree of clinical certainty that a specific substance was the cause of the manifestation in an
reaction event.

	URL: http://hl7.org/fhir/reaction-event-certainty
	ValueSet: http://hl7.org/fhir/ValueSet/reaction-event-certainty
	"""
	
	unlikely = "unlikely"
	""" There is a low level of clinical certainty that the reaction was caused by the identified substance.
	"""
	
	likely = "likely"
	""" There is a high level of clinical certainty that the reaction was caused by the identified substance.
	"""
	
	confirmed = "confirmed"
	""" There is a very high level of clinical certainty that the reaction was due to the identified substance, which
	/// may include clinical evidence by testing or rechallenge.
	"""
	
	unknown = "unknown"
	""" The clinical certainty that the reaction was caused by the identified substance is unknown.  It is an explicit
	/// assertion that certainty is not known.
	"""



class AllergyIntoleranceClinicalStatus(object):
	""" The clinical status of the allergy or intolerance.

	URL: http://hl7.org/fhir/allergy-clinical-status
	ValueSet: http://hl7.org/fhir/ValueSet/allergy-clinical-status
	"""
	
	active = "active"
	""" An active record of a risk of a reaction to the identified substance.
	"""
	
	inactive = "inactive"
	""" An inactivated record of a risk of a reaction to the identified substance.
	"""
	
	resolved = "resolved"
	""" A reaction to the identified substance has been clinically reassessed by testing or re-exposure and considered
	/// to be resolved.
	"""



class AllergyIntoleranceCriticality(object):
	""" Estimate of the potential clinical harm, or seriousness, of a reaction to an identified substance.

	URL: http://hl7.org/fhir/allergy-intolerance-criticality
	ValueSet: http://hl7.org/fhir/ValueSet/allergy-intolerance-criticality
	"""
	
	low = "low"
	""" Worst case result of a future exposure is not assessed to be life-threatening or having high potential for organ
	/// system failure.
	"""
	
	high = "high"
	""" Worst case result of a future exposure is assessed to be life-threatening or having high potential for organ
	/// system failure.
	"""
	
	unableToAssess = "unable-to-assess"
	""" Unable to assess the worst case result of a future exposure.
	"""



class AllergyIntoleranceSeverity(object):
	""" Clinical assessment of the severity of a reaction event as a whole, potentially considering multiple different
manifestations.

	URL: http://hl7.org/fhir/reaction-event-severity
	ValueSet: http://hl7.org/fhir/ValueSet/reaction-event-severity
	"""
	
	mild = "mild"
	""" Causes mild physiological effects.
	"""
	
	moderate = "moderate"
	""" Causes moderate physiological effects.
	"""
	
	severe = "severe"
	""" Causes severe physiological effects.
	"""



class AllergyIntoleranceSubstanceExposureRisk(object):
	""" The risk of an adverse reaction (allergy or intolerance) for this patient upon xposure to the substance (including
pharmaceutical products).

	URL: http://hl7.org/fhir/allerg-intol-substance-exp-risk
	ValueSet: http://hl7.org/fhir/ValueSet/allerg-intol-substance-exp-risk
	"""
	
	knownReactionRisk = "known-reaction-risk"
	""" Known risk of allergy or intolerance reaction upon exposure to the specified substance.
	"""
	
	noKnownReactionRisk = "no-known-reaction-risk"
	""" No known risk of allergy or intolerance reaction upon exposure to the specified substance.
	"""



class AllergyIntoleranceType(object):
	""" Identification of the underlying physiological mechanism for a Reaction Risk.

	URL: http://hl7.org/fhir/allergy-intolerance-type
	ValueSet: http://hl7.org/fhir/ValueSet/allergy-intolerance-type
	"""
	
	allergy = "allergy"
	""" A propensity for hypersensitivity reaction(s) to a substance.  These reactions are most typically type I
	/// hypersensitivity, plus other "allergy-like" reactions, including pseudoallergy.
	"""
	
	intolerance = "intolerance"
	""" A propensity for adverse reactions to a substance that is not judged to be allergic or "allergy-like".  These
	/// reactions are typically (but not necessarily) non-immune.  They are to some degree idiosyncratic and/or
	/// individually specific (i.e. are not a reaction that is expected to occur with most or all patients given similar
	/// circumstances).
	"""



class AllergyIntoleranceVerificationStatus(object):
	""" Assertion about certainty associated with a propensity, or potential risk, of a reaction to the identified substance.

	URL: http://hl7.org/fhir/allergy-verification-status
	ValueSet: http://hl7.org/fhir/ValueSet/allergy-verification-status
	"""
	
	unconfirmed = "unconfirmed"
	""" A low level of certainty about the propensity for a reaction to the identified substance.
	"""
	
	confirmed = "confirmed"
	""" A high level of certainty about the propensity for a reaction to the identified substance, which may include
	/// clinical evidence by testing or rechallenge.
	"""
	
	refuted = "refuted"
	""" A propensity for a reaction to the identified substance has been disproven with a high level of clinical
	/// certainty, which may include testing or rechallenge, and is refuted.
	"""
	
	enteredInError = "entered-in-error"
	""" The statement was entered in error and is not valid.
	"""



class AppointmentStatus(object):
	""" The free/busy status of an appointment.

	URL: http://hl7.org/fhir/appointmentstatus
	ValueSet: http://hl7.org/fhir/ValueSet/appointmentstatus
	"""
	
	proposed = "proposed"
	""" None of the participant(s) have finalized their acceptance of the appointment request, and the start/end time
	/// may not be set yet.
	"""
	
	pending = "pending"
	""" Some or all of the participant(s) have not finalized their acceptance of the appointment request.
	"""
	
	booked = "booked"
	""" All participant(s) have been considered and the appointment is confirmed to go ahead at the date/times
	/// specified.
	"""
	
	arrived = "arrived"
	""" Some of the patients have arrived.
	"""
	
	fulfilled = "fulfilled"
	""" This appointment has completed and may have resulted in an encounter.
	"""
	
	cancelled = "cancelled"
	""" The appointment has been cancelled.
	"""
	
	noshow = "noshow"
	""" Some or all of the participant(s) have not/did not appear for the appointment (usually the patient).
	"""
	
	enteredInError = "entered-in-error"
	""" This instance should not have been part of this patient's medical record.
	"""



class AssertionDirectionType(object):
	""" The type of direction to use for assertion.

	URL: http://hl7.org/fhir/assert-direction-codes
	ValueSet: http://hl7.org/fhir/ValueSet/assert-direction-codes
	"""
	
	response = "response"
	""" The assertion is evaluated on the response. This is the default value.
	"""
	
	request = "request"
	""" The assertion is evaluated on the request.
	"""



class AssertionOperatorType(object):
	""" The type of operator to use for assertion.

	URL: http://hl7.org/fhir/assert-operator-codes
	ValueSet: http://hl7.org/fhir/ValueSet/assert-operator-codes
	"""
	
	equals = "equals"
	""" Default value. Equals comparison.
	"""
	
	notEquals = "notEquals"
	""" Not equals comparison.
	"""
	
	# in = "in"
	""" Compare value within a known set of values.
	"""
	
	notIn = "notIn"
	""" Compare value not within a known set of values.
	"""
	
	greaterThan = "greaterThan"
	""" Compare value to be greater than a known value.
	"""
	
	lessThan = "lessThan"
	""" Compare value to be less than a known value.
	"""
	
	empty = "empty"
	""" Compare value is empty.
	"""
	
	notEmpty = "notEmpty"
	""" Compare value is not empty.
	"""
	
	contains = "contains"
	""" Compare value string contains a known value.
	"""
	
	notContains = "notContains"
	""" Compare value string does not contain a known value.
	"""
	
	eval = "eval"
	""" Evaluate the fhirpath expression as a boolean condition.
	"""



class AssertionResponseTypes(object):
	""" The type of response code to use for assertion.

	URL: http://hl7.org/fhir/assert-response-code-types
	ValueSet: http://hl7.org/fhir/ValueSet/assert-response-code-types
	"""
	
	okay = "okay"
	""" Response code is 200.
	"""
	
	created = "created"
	""" Response code is 201.
	"""
	
	noContent = "noContent"
	""" Response code is 204.
	"""
	
	notModified = "notModified"
	""" Response code is 304.
	"""
	
	bad = "bad"
	""" Response code is 400.
	"""
	
	forbidden = "forbidden"
	""" Response code is 403.
	"""
	
	notFound = "notFound"
	""" Response code is 404.
	"""
	
	methodNotAllowed = "methodNotAllowed"
	""" Response code is 405.
	"""
	
	conflict = "conflict"
	""" Response code is 409.
	"""
	
	gone = "gone"
	""" Response code is 410.
	"""
	
	preconditionFailed = "preconditionFailed"
	""" Response code is 412.
	"""
	
	unprocessable = "unprocessable"
	""" Response code is 422.
	"""



class AuditEventAction(object):
	""" Indicator for type of action performed during the event that generated the audit.

	URL: http://hl7.org/fhir/audit-event-action
	ValueSet: http://hl7.org/fhir/ValueSet/audit-event-action
	"""
	
	C = "C"
	""" Create a new database object, such as placing an order.
	"""
	
	R = "R"
	""" Display or print data, such as a doctor census.
	"""
	
	U = "U"
	""" Update data, such as revise patient information.
	"""
	
	D = "D"
	""" Delete items, such as a doctor master file record.
	"""
	
	E = "E"
	""" Perform a system or application function such as log-on, program execution or use of an object's method, or
	/// perform a query/search operation.
	"""



class BindingStrength(object):
	""" Indication of the degree of conformance expectations associated with a binding.

	URL: http://hl7.org/fhir/binding-strength
	ValueSet: http://hl7.org/fhir/ValueSet/binding-strength
	"""
	
	required = "required"
	""" To be conformant, instances of this element SHALL include a code from the specified value set.
	"""
	
	extensible = "extensible"
	""" To be conformant, instances of this element SHALL include a code from the specified value set if any of the
	/// codes within the value set can apply to the concept being communicated.  If the value set does not cover the
	/// concept (based on human review), alternate codings (or, data type allowing, text) may be included instead.
	"""
	
	preferred = "preferred"
	""" Instances are encouraged to draw from the specified codes for interoperability purposes but are not required to
	/// do so to be considered conformant.
	"""
	
	example = "example"
	""" Instances are not expected or even encouraged to draw from the specified value set.  The value set merely
	/// provides examples of the types of concepts intended to be included.
	"""



class BundleType(object):
	""" Indicates the purpose of a bundle - how it was intended to be used.

	URL: http://hl7.org/fhir/bundle-type
	ValueSet: http://hl7.org/fhir/ValueSet/bundle-type
	"""
	
	document = "document"
	""" The bundle is a document. The first resource is a Composition.
	"""
	
	message = "message"
	""" The bundle is a message. The first resource is a MessageHeader.
	"""
	
	transaction = "transaction"
	""" The bundle is a transaction - intended to be processed by a server as an atomic commit.
	"""
	
	transactionResponse = "transaction-response"
	""" The bundle is a transaction response. Because the response is a transaction response, the transaction has
	/// succeeded, and all responses are error free.
	"""
	
	batch = "batch"
	""" The bundle is a transaction - intended to be processed by a server as a group of actions.
	"""
	
	batchResponse = "batch-response"
	""" The bundle is a batch response. Note that as a batch, some responses may indicate failure and others success.
	"""
	
	history = "history"
	""" The bundle is a list of resources from a history interaction on a server.
	"""
	
	searchset = "searchset"
	""" The bundle is a list of resources returned as a result of a search/query interaction, operation, or message.
	"""
	
	collection = "collection"
	""" The bundle is a set of resources collected into a single package for ease of distribution.
	"""



class CapabilityStatementKind(object):
	""" How a capability statement is intended to be used.

	URL: http://hl7.org/fhir/capability-statement-kind
	ValueSet: http://hl7.org/fhir/ValueSet/capability-statement-kind
	"""
	
	instance = "instance"
	""" The CapabilityStatement instance represents the present capabilities of a specific system instance.  This is the
	/// kind returned by OPTIONS for a FHIR server end-point.
	"""
	
	capability = "capability"
	""" The CapabilityStatement instance represents the capabilities of a system or piece of software, independent of a
	/// particular installation.
	"""
	
	requirements = "requirements"
	""" The CapabilityStatement instance represents a set of requirements for other systems to meet; e.g. as part of an
	/// implementation guide or 'request for proposal'.
	"""



class CarePlanActivityStatus(object):
	""" Indicates where the activity is at in its overall life cycle.

	URL: http://hl7.org/fhir/care-plan-activity-status
	ValueSet: http://hl7.org/fhir/ValueSet/care-plan-activity-status
	"""
	
	notStarted = "not-started"
	""" Activity is planned but no action has yet been taken.
	"""
	
	scheduled = "scheduled"
	""" Appointment or other booking has occurred but activity has not yet begun.
	"""
	
	inProgress = "in-progress"
	""" Activity has been started but is not yet complete.
	"""
	
	onHold = "on-hold"
	""" Activity was started but has temporarily ceased with an expectation of resumption at a future time.
	"""
	
	completed = "completed"
	""" The activities have been completed (more or less) as planned.
	"""
	
	cancelled = "cancelled"
	""" The activities have been ended prior to completion (perhaps even before they were started).
	"""
	
	unknown = "unknown"
	""" The authoring system doesn't know the current state of the activity.
	"""



class CarePlanRelationship(object):
	""" Codes identifying the types of relationships between two plans.

	URL: http://hl7.org/fhir/care-plan-relationship
	ValueSet: http://hl7.org/fhir/ValueSet/care-plan-relationship
	"""
	
	includes = "includes"
	""" The referenced plan is considered to be part of this plan.
	"""
	
	replaces = "replaces"
	""" This plan takes the places of the referenced plan.
	"""
	
	fulfills = "fulfills"
	""" This plan provides details about how to perform activities defined at a higher level by the referenced plan.
	"""



class CarePlanStatus(object):
	""" Indicates whether the plan is currently being acted upon, represents future intentions or is now a historical record.

	URL: http://hl7.org/fhir/care-plan-status
	ValueSet: http://hl7.org/fhir/ValueSet/care-plan-status
	"""
	
	proposed = "proposed"
	""" The plan has been suggested but no commitment to it has yet been made.
	"""
	
	draft = "draft"
	""" The plan is in development or awaiting use but is not yet intended to be acted upon.
	"""
	
	active = "active"
	""" The plan is intended to be followed and used as part of patient care.
	"""
	
	suspended = "suspended"
	""" The plan has been temporarily stopped but is expected to resume in the future.
	"""
	
	completed = "completed"
	""" The plan is no longer in use and is not expected to be followed or used in patient care.
	"""
	
	enteredInError = "entered-in-error"
	""" The plan was entered in error and voided.
	"""
	
	cancelled = "cancelled"
	""" The plan has been terminated prior to reaching completion (though it may have been replaced by a new plan).
	"""
	
	unknown = "unknown"
	""" The authoring system doesn't know the current state of the care plan.
	"""



class ChoiceListOrientation(object):
	""" Direction in which lists of question options should be displayed

	URL: http://hl7.org/fhir/choice-list-orientation
	ValueSet: http://hl7.org/fhir/ValueSet/choice-list-orientation
	"""
	
	horizontal = "horizontal"
	""" List choices along the horizontal axis
	"""
	
	vertical = "vertical"
	""" List choices down the vertical axis
	"""



class ClassificationOrContext(object):
	""" Identifies whether a useContext represents a context or classification for the element

	URL: http://hl7.org/fhir/classification-or-context
	ValueSet: http://hl7.org/fhir/ValueSet/classification-or-context
	"""
	
	classification = "classification"
	""" Indicates the useContext is a classification - e.g. Administrative, financial, etc.
	"""
	
	context = "context"
	""" Indicates the useContext is a context - a domain of use - e.g. Particular country, organization or system
	"""



class ClinicalImpressionStatus(object):
	""" The workflow state of a clinical impression.

	URL: http://hl7.org/fhir/clinical-impression-status
	ValueSet: http://hl7.org/fhir/ValueSet/clinical-impression-status
	"""
	
	draft = "draft"
	""" The assessment is still on-going and results are not yet final.
	"""
	
	completed = "completed"
	""" The assessment is done and the results are final.
	"""
	
	enteredInError = "entered-in-error"
	""" This assessment was never actually done and the record is erroneous (e.g. Wrong patient).
	"""



class CodeSystemContentMode(object):
	""" How much of the content of the code system - the concepts and codes it defines - are represented in a code system
resource

	URL: http://hl7.org/fhir/codesystem-content-mode
	ValueSet: http://hl7.org/fhir/ValueSet/codesystem-content-mode
	"""
	
	notPresent = "not-present"
	""" None of the concepts defined by the code system are included in the code system resource
	"""
	
	examplar = "examplar"
	""" A few representative concepts are included in the code system resource
	"""
	
	fragment = "fragment"
	""" A subset of the code system concepts are included in the code system resource
	"""
	
	complete = "complete"
	""" All the concepts defined by the code system are included in the code system resource
	"""



class CodeSystemHierarchyMeaning(object):
	""" The meaning of the hierarchy of concepts in a code system

	URL: http://hl7.org/fhir/codesystem-hierarchy-meaning
	ValueSet: http://hl7.org/fhir/ValueSet/codesystem-hierarchy-meaning
	"""
	
	groupedBy = "grouped-by"
	""" No particular relationship between the concepts can be assumed, except what can be determined by inspection of
	/// the definitions of the elements (possible reasons to use this: importing from a source where this is not
	/// defined, or where various parts of the heirarchy have different meanings)
	"""
	
	isA = "is-a"
	""" A hierarchy where the child concepts have an IS-A relationship with the parents - that is, all the properties of
	/// the parent are also true for it's child concepts
	"""
	
	partOf = "part-of"
	""" Child elements list the individual parts of a composite whole (e.g. bodysite)
	"""
	
	classifiedWith = "classified-with"
	""" Child concepts in the hierarchy may have only one parent and there is a presumption that the code system is a
	/// "closed world" meaning all things must be in the hierarchy. This results in concepts such as "not otherwise
	/// clasified."
	"""



class CommunicationRequestStatus(object):
	""" The status of the communication.

	URL: http://hl7.org/fhir/communication-request-status
	ValueSet: http://hl7.org/fhir/ValueSet/communication-request-status
	"""
	
	proposed = "proposed"
	""" The request has been proposed.
	"""
	
	planned = "planned"
	""" The request has been planned.
	"""
	
	requested = "requested"
	""" The request has been placed.
	"""
	
	received = "received"
	""" The receiving system has received the request but not yet decided whether it will be performed.
	"""
	
	accepted = "accepted"
	""" The receiving system has accepted the order, but work has not yet commenced.
	"""
	
	inProgress = "in-progress"
	""" The work to fulfill the order is happening.
	"""
	
	completed = "completed"
	""" The work has been complete, the report(s) released, and no further work is planned.
	"""
	
	suspended = "suspended"
	""" The request has been held by originating system/user request.
	"""
	
	rejected = "rejected"
	""" The receiving system has declined to fulfill the request
	"""
	
	failed = "failed"
	""" The communication was attempted, but due to some procedural error, it could not be completed.
	"""



class CommunicationStatus(object):
	""" The status of the communication.

	URL: http://hl7.org/fhir/communication-status
	ValueSet: http://hl7.org/fhir/ValueSet/communication-status
	"""
	
	inProgress = "in-progress"
	""" The communication transmission is ongoing.
	"""
	
	completed = "completed"
	""" The message transmission is complete, i.e., delivered to the recipient's destination.
	"""
	
	suspended = "suspended"
	""" The communication transmission has been held by originating system/user request.
	"""
	
	rejected = "rejected"
	""" The receiving system has declined to accept the message.
	"""
	
	failed = "failed"
	""" There was a failure in transmitting the message out.
	"""



class CompartmentType(object):
	""" Which compartment a compartmnet definition describes

	URL: http://hl7.org/fhir/compartment-type
	ValueSet: http://hl7.org/fhir/ValueSet/compartment-type
	"""
	
	patient = "Patient"
	""" The compartment definition is for the patient compartment
	"""
	
	encounter = "Encounter"
	""" The compartment definition is for the encounter compartment
	"""
	
	relatedPerson = "RelatedPerson"
	""" The compartment definition is for the related-person compartment
	"""
	
	practitioner = "Practitioner"
	""" The compartment definition is for the practitioner compartment
	"""
	
	device = "Device"
	""" The compartment definition is for the device compartment
	"""



class CompositeMeasureScoring(object):
	""" The composite scoring method of the measure

	URL: http://hl7.org/fhir/composite-measure-scoring
	ValueSet: http://hl7.org/fhir/ValueSet/composite-measure-scoring
	"""
	
	opportunity = "opportunity"
	""" Opportunity scoring combines the scores from component measures by combining the numerators and denominators for
	/// each component
	"""
	
	allOrNothing = "all-or-nothing"
	""" All-or-nothing scoring includes an individual in the numerator of the composite measure if they are in the
	/// numerators of all of the component measures in which they are in the denominator
	"""
	
	linear = "linear"
	""" Linear scoring gives an individual a score based on the number of numerators in which they appear
	"""
	
	weighted = "weighted"
	""" Weighted scoring gives an individual a score based on a weigthed factor for each component numerator in which
	/// they appear
	"""



class CompositionAttestationMode(object):
	""" The way in which a person authenticated a composition.

	URL: http://hl7.org/fhir/composition-attestation-mode
	ValueSet: http://hl7.org/fhir/ValueSet/composition-attestation-mode
	"""
	
	personal = "personal"
	""" The person authenticated the content in their personal capacity.
	"""
	
	professional = "professional"
	""" The person authenticated the content in their professional capacity.
	"""
	
	legal = "legal"
	""" The person authenticated the content and accepted legal responsibility for its content.
	"""
	
	official = "official"
	""" The organization authenticated the content as consistent with their policies and procedures.
	"""



class CompositionStatus(object):
	""" The workflow/clinical status of the composition.

	URL: http://hl7.org/fhir/composition-status
	ValueSet: http://hl7.org/fhir/ValueSet/composition-status
	"""
	
	preliminary = "preliminary"
	""" This is a preliminary composition or document (also known as initial or interim). The content may be incomplete
	/// or unverified.
	"""
	
	final = "final"
	""" This version of the composition is complete and verified by an appropriate person and no further work is
	/// planned. Any subsequent updates would be on a new version of the composition.
	"""
	
	amended = "amended"
	""" The composition content or the referenced resources have been modified (edited or added to) subsequent to being
	/// released as "final" and the composition is complete and verified by an authorized person.
	"""
	
	enteredInError = "entered-in-error"
	""" The composition or document was originally created/issued in error, and this is an amendment that marks that the
	/// entire series should not be considered as valid.
	"""



class ConceptMapEquivalence(object):
	""" The degree of equivalence between concepts.

	URL: http://hl7.org/fhir/concept-map-equivalence
	ValueSet: http://hl7.org/fhir/ValueSet/concept-map-equivalence
	"""
	
	relatedto = "relatedto"
	""" The concepts are related to each other, and have at least some overlap in meaning, but the exact relationship is
	/// not known
	"""
	
	equivalent = "equivalent"
	""" The definitions of the concepts mean the same thing (including when structural implications of meaning are
	/// considered) (i.e. extensionally identical).
	"""
	
	equal = "equal"
	""" The definitions of the concepts are exactly the same (i.e. only grammatical differences) and structural
	/// implications of meaning are identical or irrelevant (i.e. intentionally identical).
	"""
	
	wider = "wider"
	""" The target mapping is wider in meaning than the source concept.
	"""
	
	subsumes = "subsumes"
	""" The target mapping subsumes the meaning of the source concept (e.g. the source is-a target).
	"""
	
	narrower = "narrower"
	""" The target mapping is narrower in meaning than the source concept. The sense in which the mapping is narrower
	/// SHALL be described in the comments in this case, and applications should be careful when attempting to use these
	/// mappings operationally.
	"""
	
	specializes = "specializes"
	""" The target mapping specializes the meaning of the source concept (e.g. the target is-a source).
	"""
	
	inexact = "inexact"
	""" The target mapping overlaps with the source concept, but both source and target cover additional meaning, or the
	/// definitions are imprecise and it is uncertain whether they have the same boundaries to their meaning. The sense
	/// in which the mapping is narrower SHALL be described in the comments in this case, and applications should be
	/// careful when attempting to use these mappings operationally.
	"""
	
	unmatched = "unmatched"
	""" There is no match for this concept in the destination concept system.
	"""
	
	disjoint = "disjoint"
	""" This is an explicit assertion that there is no mapping between the source and target concept.
	"""



class ConditionState(object):
	""" Enumeration indicating whether the condition is currently active, inactive, or has been resolved.

	URL: http://hl7.org/fhir/condition-state
	ValueSet: http://hl7.org/fhir/ValueSet/condition-state
	"""
	
	active = "active"
	""" The condition is active.
	"""
	
	inactive = "inactive"
	""" The condition inactive but not resolved.
	"""
	
	resolved = "resolved"
	""" The condition is resolved.
	"""



class ConditionVerificationStatus(object):
	""" The verification status to support or decline the clinical status of the condition or diagnosis.

	URL: http://hl7.org/fhir/condition-ver-status
	ValueSet: http://hl7.org/fhir/ValueSet/condition-ver-status
	"""
	
	provisional = "provisional"
	""" This is a tentative diagnosis - still a candidate that is under consideration.
	"""
	
	differential = "differential"
	""" One of a set of potential (and typically mutually exclusive) diagnosis asserted to further guide the diagnostic
	/// process and preliminary treatment.
	"""
	
	confirmed = "confirmed"
	""" There is sufficient diagnostic and/or clinical evidence to treat this as a confirmed condition.
	"""
	
	refuted = "refuted"
	""" This condition has been ruled out by diagnostic and clinical evidence.
	"""
	
	enteredInError = "entered-in-error"
	""" The statement was entered in error and is not valid.
	"""
	
	unknown = "unknown"
	""" The condition status is unknown.  Note that "unknown" is a value of last resort and every attempt should be made
	/// to provide a meaningful value other than "unknown".
	"""



class ConditionalDeleteStatus(object):
	""" A code that indicates how the server supports conditional delete.

	URL: http://hl7.org/fhir/conditional-delete-status
	ValueSet: http://hl7.org/fhir/ValueSet/conditional-delete-status
	"""
	
	notSupported = "not-supported"
	""" No support for conditional deletes.
	"""
	
	single = "single"
	""" Conditional deletes are supported, but only single resources at a time.
	"""
	
	multiple = "multiple"
	""" Conditional deletes are supported, and multiple resources can be deleted in a single interaction.
	"""



class ConditionalReadStatus(object):
	""" A code that indicates how the server supports conditional read.

	URL: http://hl7.org/fhir/conditional-read-status
	ValueSet: http://hl7.org/fhir/ValueSet/conditional-read-status
	"""
	
	notSupported = "not-supported"
	""" No support for conditional deletes.
	"""
	
	modifiedSince = "modified-since"
	""" Conditional reads are supported, but only with the If-Modified-Since HTTP Header.
	"""
	
	notMatch = "not-match"
	""" Conditional reads are supported, but only with the If-None-Match HTTP Header.
	"""
	
	fullSupport = "full-support"
	""" Conditional reads are supported, with both If-Modified-Since and If-None-Match HTTP Headers.
	"""



class ConformanceExpectation(object):
	""" Indicates the degree of adherence to a specified behavior or capability expected in order for a system to be deemed
conformant with a specification.

	URL: http://hl7.org/fhir/conformance-expectation
	ValueSet: http://hl7.org/fhir/ValueSet/conformance-expectation
	"""
	
	SHALL = "SHALL"
	""" Support for the specified capability is required to be considered conformant.
	"""
	
	SHOULD = "SHOULD"
	""" Support for the specified capability is strongly encouraged and failure to support it should only occur after
	/// careful consideration.
	"""
	
	MAY = "MAY"
	""" Support for the specified capability is not necessary to be considered conformant and the requirement should be
	/// considered strictly optional.
	"""
	
	SHOULDNOT = "SHOULD-NOT"
	""" Support for the specified capability is strongly discouraged and should occur only after careful consideration.
	"""



class ConsentDataMeaning(object):
	""" How a resource reference is interpreted when testing consent restrictions

	URL: http://hl7.org/fhir/consent-data-meaning
	ValueSet: http://hl7.org/fhir/ValueSet/consent-data-meaning
	"""
	
	instance = "instance"
	""" The consent applies directly to the instance of the resource
	"""
	
	related = "related"
	""" The consent applies directly to the instance of the resource, and instances it refers to
	"""
	
	dependents = "dependents"
	""" The consent applies directly to the instance of the resource, and instances that refer to it
	"""



class ConsentExceptType(object):
	""" How an exception is statement is applied, as adding additional consent, or removing consent

	URL: http://hl7.org/fhir/consent-except-type
	ValueSet: http://hl7.org/fhir/ValueSet/consent-except-type
	"""
	
	deny = "deny"
	""" Consent is denied for actions meeting these rules
	"""
	
	permit = "permit"
	""" Consent is provided for actions meeting these rules
	"""



class ConsentStatus(object):
	""" Indicates the status of the consent

	URL: http://hl7.org/fhir/consent-status
	ValueSet: http://hl7.org/fhir/ValueSet/consent-status
	"""
	
	draft = "draft"
	""" The consent is in development or awaiting use but is not yet intended to be acted upon.
	"""
	
	proposed = "proposed"
	""" The consent has be proposed but not yet agreed to by all parties. The negotiation stage.
	"""
	
	active = "active"
	""" The consent is to be followed and enforced.
	"""
	
	rejected = "rejected"
	""" The consent has been rejected by one or more of the parties.
	"""
	
	inactive = "inactive"
	""" The consent is terminated or replaced.
	"""
	
	enteredInError = "entered-in-error"
	""" The consent was created wrongly (e.g. wrong patient) and should be ignored
	"""



class ConstraintSeverity(object):
	""" SHALL applications comply with this constraint?

	URL: http://hl7.org/fhir/constraint-severity
	ValueSet: http://hl7.org/fhir/ValueSet/constraint-severity
	"""
	
	error = "error"
	""" If the constraint is violated, the resource is not conformant.
	"""
	
	warning = "warning"
	""" If the constraint is violated, the resource is conformant, but it is not necessarily following best practice.
	"""



class ContactPointSystem(object):
	""" Telecommunications form for contact point

	URL: http://hl7.org/fhir/contact-point-system
	ValueSet: http://hl7.org/fhir/ValueSet/contact-point-system
	"""
	
	phone = "phone"
	""" The value is a telephone number used for voice calls. Use of full international numbers starting with + is
	/// recommended to enable automatic dialing support but not required.
	"""
	
	fax = "fax"
	""" The value is a fax machine. Use of full international numbers starting with + is recommended to enable automatic
	/// dialing support but not required.
	"""
	
	email = "email"
	""" The value is an email address.
	"""
	
	pager = "pager"
	""" The value is a pager number. These may be local pager numbers that are only usable on a particular pager system.
	"""
	
	url = "url"
	""" A contact that is not a phone, fax, pager or email address and is expressed as a URL.  This is intended for
	/// various personal contacts including blogs, Skype, Twitter, Facebook, etc. Do not use for email addresses.
	"""
	
	other = "other"
	""" A contact that is not a phone, fax, page or email address and is not expressible as a URL.  E.g. Internal mail
	/// address.  This SHOULD NOT be used for contacts that are expressible as a URL (e.g. Skype, Twitter, Facebook,
	/// etc.)  Extensions may be used to distinguish "other" contact types.
	"""



class ContactPointUse(object):
	""" Use of contact point

	URL: http://hl7.org/fhir/contact-point-use
	ValueSet: http://hl7.org/fhir/ValueSet/contact-point-use
	"""
	
	home = "home"
	""" A communication contact point at a home; attempted contacts for business purposes might intrude privacy and
	/// chances are one will contact family or other household members instead of the person one wishes to call.
	/// Typically used with urgent cases, or if no other contacts are available.
	"""
	
	work = "work"
	""" An office contact point. First choice for business related contacts during business hours.
	"""
	
	temp = "temp"
	""" A temporary contact point. The period can provide more detailed information.
	"""
	
	old = "old"
	""" This contact point is no longer in use (or was never correct, but retained for records).
	"""
	
	mobile = "mobile"
	""" A telecommunication device that moves and stays with its owner. May have characteristics of all other use codes,
	/// suitable for urgent matters, not the first choice for routine business.
	"""



class ContentType(object):
	""" The content or mime type.

	URL: http://hl7.org/fhir/content-type
	ValueSet: http://hl7.org/fhir/ValueSet/content-type
	"""
	
	xml = "xml"
	""" XML content-type corresponding to the application/fhir+xml mime-type.
	"""
	
	json = "json"
	""" JSON content-type corresponding to the application/fhir+json mime-type.
	"""
	
	ttl = "ttl"
	""" RDF content-type corresponding to the text/turtle mime-type.
	"""
	
	none = "none"
	""" Prevent the use of the corresponding http header.
	"""



class ContributorType(object):
	""" The type of contributor

	URL: http://hl7.org/fhir/contributor-type
	ValueSet: http://hl7.org/fhir/ValueSet/contributor-type
	"""
	
	author = "author"
	""" An author of the content of the module
	"""
	
	editor = "editor"
	""" An editor of the content of the module
	"""
	
	reviewer = "reviewer"
	""" A reviewer of the content of the module
	"""
	
	endorser = "endorser"
	""" An endorser of the content of the module
	"""



class CopyNumberEvent(object):
	""" Copy Number Event

	URL: http://hl7.org/fhir/copy-number-event
	ValueSet: http://hl7.org/fhir/ValueSet/copy-number-event
	"""
	
	amp = "amp"
	""" amplificaiton
	"""
	
	# del = "del"
	""" deletion
	"""
	
	lof = "lof"
	""" loss of function
	"""



class DWebType(object):
	""" The type of the service endpoint

	URL: http://hl7.org/fhir/dWebType
	ValueSet: http://hl7.org/fhir/ValueSet/dWebType
	"""
	
	WADORS = "WADO-RS"
	""" Web Access to DICOM Persistent Objects - RESTful Services
	"""
	
	WADOURI = "WADO-URI"
	""" Web Access to DICOM Persistent Objects - URI
	"""
	
	IID = "IID"
	""" IHE - Invoke Image Display Profile
	"""



class DataAbsentReason(object):
	""" Used to specify why the normally expected content of the data element is missing.

	URL: http://hl7.org/fhir/data-absent-reason
	ValueSet: http://hl7.org/fhir/ValueSet/data-absent-reason
	"""
	
	unknown = "unknown"
	""" The value is not known.
	"""
	
	asked = "asked"
	""" The source human does not know the value.
	"""
	
	temp = "temp"
	""" There is reason to expect (from the workflow) that the value may become known.
	"""
	
	notAsked = "not-asked"
	""" The workflow didn't lead to this value being known.
	"""
	
	masked = "masked"
	""" The information is not available due to security, privacy or related reasons.
	"""
	
	unsupported = "unsupported"
	""" The source system wasn't capable of supporting this element.
	"""
	
	astext = "astext"
	""" The content of the data is represented in the resource narrative.
	"""
	
	error = "error"
	""" Some system or workflow process error means that the information is not available.
	"""
	
	naN = "NaN"
	""" NaN, standing for not a number, is a numeric data type value representing an undefined or unrepresentable value.
	"""
	
	notPerformed = "not-performed"
	""" The value is not available because the observation procedure (test, etc.) was not performed.
	"""



class DataElementStringency(object):
	""" Indicates the degree of precision of the data element definition.

	URL: http://hl7.org/fhir/dataelement-stringency
	ValueSet: http://hl7.org/fhir/ValueSet/dataelement-stringency
	"""
	
	comparable = "comparable"
	""" The data element is sufficiently well-constrained that multiple pieces of data captured according to the
	/// constraints of the data element will be comparable (though in some cases, a degree of automated
	/// conversion/normalization may be required).
	"""
	
	fullySpecified = "fully-specified"
	""" The data element is fully specified down to a single value set, single unit of measure, single data type, etc.
	/// Multiple pieces of data associated with this data element are fully comparable.
	"""
	
	equivalent = "equivalent"
	""" The data element allows multiple units of measure having equivalent meaning; e.g. "cc" (cubic centimeter) and
	/// "mL" (milliliter).
	"""
	
	convertable = "convertable"
	""" The data element allows multiple units of measure that are convertable between each other (e.g. inches and
	/// centimeters) and/or allows data to be captured in multiple value sets for which a known mapping exists allowing
	/// conversion of meaning.
	"""
	
	scaleable = "scaleable"
	""" A convertable data element where unit conversions are different only by a power of 10; e.g. g, mg, kg.
	"""
	
	flexible = "flexible"
	""" The data element is unconstrained in units, choice of data types and/or choice of vocabulary such that automated
	/// comparison of data captured using the data element is not possible.
	"""



class DataType(object):
	""" The type of an element - one of the FHIR data types.

	URL: http://hl7.org/fhir/data-types
	ValueSet: http://hl7.org/fhir/ValueSet/data-types
	"""
	
	address = "Address"
	""" An address expressed using postal conventions (as opposed to GPS or other location definition formats).  This
	/// data type may be used to convey addresses for use in delivering mail as well as for visiting locations and which
	/// might not be valid for mail delivery.  There are a variety of postal address formats defined around the world.
	"""
	
	age = "Age"
	""" A duration of time during which an organism (or a process) has existed.
	"""
	
	annotation = "Annotation"
	""" A  text note which also  contains information about who made the statement and when.
	"""
	
	attachment = "Attachment"
	""" For referring to data content defined in other formats.
	"""
	
	backboneElement = "BackboneElement"
	""" Base definition for all elements that are defined inside a resource - but not those in a data type.
	"""
	
	codeableConcept = "CodeableConcept"
	""" A concept that may be defined by a formal reference to a terminology or ontology or may be provided by text.
	"""
	
	coding = "Coding"
	""" A reference to a code defined by a terminology system.
	"""
	
	contactDetail = "ContactDetail"
	""" Specifies contact information for a person or organization.
	"""
	
	contactPoint = "ContactPoint"
	""" Details for all kinds of technology mediated contact points for a person or organization, including telephone,
	/// email, etc.
	"""
	
	contributor = "Contributor"
	""" A contributor to the content of a knowledge asset, including authors, editors, reviewers, and endorsers.
	"""
	
	count = "Count"
	""" A measured amount (or an amount that can potentially be measured). Note that measured amounts include amounts
	/// that are not precisely quantified, including amounts involving arbitrary units and floating currencies.
	"""
	
	dataRequirement = "DataRequirement"
	""" Describes a required data item for evaluation in terms of the type of data, and optional code- or date-based
	/// filters of the data.
	"""
	
	distance = "Distance"
	""" A length - a value with a unit that is a physical distance.
	"""
	
	dosageInstruction = "DosageInstruction"
	""" Indicates how the medication is to be used by the patient.
	"""
	
	duration = "Duration"
	""" A length of time.
	"""
	
	element = "Element"
	""" Base definition for all elements in a resource.
	"""
	
	elementDefinition = "ElementDefinition"
	""" Captures constraints on each element within the resource, profile, or extension.
	"""
	
	extension = "Extension"
	""" Optional Extensions Element - found in all resources.
	"""
	
	humanName = "HumanName"
	""" A human's name with the ability to identify parts and usage.
	"""
	
	identifier = "Identifier"
	""" A technical identifier - identifies some entity uniquely and unambiguously.
	"""
	
	meta = "Meta"
	""" The metadata about a resource. This is content in the resource that is maintained by the infrastructure. Changes
	/// to the content may not always be associated with version changes to the resource.
	"""
	
	money = "Money"
	""" An amount of economic utility in some recognised currency.
	"""
	
	narrative = "Narrative"
	""" A human-readable formatted text, including images.
	"""
	
	parameterDefinition = "ParameterDefinition"
	""" The parameters to the module. This collection specifies both the input and output parameters. Input parameters
	/// are provided by the caller as part of the $evaluate operation. Output parameters are included in the
	/// GuidanceResponse.
	"""
	
	period = "Period"
	""" A time period defined by a start and end date and optionally time.
	"""
	
	quantity = "Quantity"
	""" A measured amount (or an amount that can potentially be measured). Note that measured amounts include amounts
	/// that are not precisely quantified, including amounts involving arbitrary units and floating currencies.
	"""
	
	range = "Range"
	""" A set of ordered Quantities defined by a low and high limit.
	"""
	
	ratio = "Ratio"
	""" A relationship of two Quantity values - expressed as a numerator and a denominator.
	"""
	
	reference = "Reference"
	""" A reference from one resource to another.
	"""
	
	relatedArtifact = "RelatedArtifact"
	""" Related artifacts such as additional documentation, justification, or bibliographic references.
	"""
	
	sampledData = "SampledData"
	""" A series of measurements taken by a device, with upper and lower limits. There may be more than one dimension in
	/// the data.
	"""
	
	signature = "Signature"
	""" A digital signature along with supporting context. The signature may be electronic/cryptographic in nature, or a
	/// graphical image representing a hand-written signature, or a signature process. Different Signature approaches
	/// have different utilities.
	"""
	
	simpleQuantity = "SimpleQuantity"
	""" simpleQuantity
	"""
	
	timing = "Timing"
	""" Specifies an event that may occur multiple times. Timing schedules are used to record when things are expected
	/// or requested to occur. The most common usage is in dosage instructions for medications. They are also used when
	/// planning care of various kinds.
	"""
	
	triggerDefinition = "TriggerDefinition"
	""" A description of a triggering event.
	"""
	
	usageContext = "UsageContext"
	""" Specifies clinical/business/etc metadata that can be used to retrieve, index and/or categorize an artifact. This
	/// metadata can either be specific to the applicable population (e.g., age category, DRG) or the specific context
	/// of care (e.g., venue, care setting, provider of care).
	"""
	
	base64Binary = "base64Binary"
	""" A stream of bytes
	"""
	
	boolean = "boolean"
	""" Value of "true" or "false"
	"""
	
	code = "code"
	""" A string which has at least one character and no leading or trailing whitespace and where there is no whitespace
	/// other than single spaces in the contents
	"""
	
	date = "date"
	""" A date or partial date (e.g. just year or year + month). There is no time zone. The format is a union of the
	/// schema types gYear, gYearMonth and date.  Dates SHALL be valid dates.
	"""
	
	dateTime = "dateTime"
	""" A date, date-time or partial date (e.g. just year or year + month).  If hours and minutes are specified, a time
	/// zone SHALL be populated. The format is a union of the schema types gYear, gYearMonth, date and dateTime. Seconds
	/// must be provided due to schema type constraints but may be zero-filled and may be ignored.                 Dates
	/// SHALL be valid dates.
	"""
	
	decimal = "decimal"
	""" A rational number with implicit precision
	"""
	
	id = "id"
	""" Any combination of letters, numerals, "-" and ".", with a length limit of 64 characters.  (This might be an
	/// integer, an unprefixed OID, UUID or any other identifier pattern that meets these constraints.)  Ids are case-
	/// insensitive.
	"""
	
	instant = "instant"
	""" An instant in time - known at least to the second
	"""
	
	integer = "integer"
	""" A whole number
	"""
	
	markdown = "markdown"
	""" A string that may contain markdown syntax for optional processing by a mark down presentation engine
	"""
	
	oid = "oid"
	""" An oid represented as a URI
	"""
	
	positiveInt = "positiveInt"
	""" An integer with a value that is positive (e.g. >0)
	"""
	
	string = "string"
	""" A sequence of Unicode characters
	"""
	
	time = "time"
	""" A time during the day, with no date specified
	"""
	
	unsignedInt = "unsignedInt"
	""" An integer with a value that is not negative (e.g. >= 0)
	"""
	
	uri = "uri"
	""" String of characters used to identify a name or a resource
	"""
	
	uuid = "uuid"
	""" A UUID, represented as a URI
	"""
	
	xhtml = "xhtml"
	""" XHTML format, as defined by W3C, but restricted usage (mainly, no active content)
	"""



class DaysOfWeek(object):
	""" The days of the week.

	URL: http://hl7.org/fhir/days-of-week
	ValueSet: http://hl7.org/fhir/ValueSet/days-of-week
	"""
	
	mon = "mon"
	""" Monday
	"""
	
	tue = "tue"
	""" Tuesday
	"""
	
	wed = "wed"
	""" Wednesday
	"""
	
	thu = "thu"
	""" Thursday
	"""
	
	fri = "fri"
	""" Friday
	"""
	
	sat = "sat"
	""" Saturday
	"""
	
	sun = "sun"
	""" Sunday
	"""



class DefinitionStatus(object):
	""" Codes identifying the stage lifecycle stage of a definition

	URL: http://hl7.org/fhir/definition-status
	ValueSet: http://hl7.org/fhir/ValueSet/definition-status
	"""
	
	draft = "draft"
	""" The definition is in the design stage and is not yet considered to be "ready for use"
	"""
	
	active = "active"
	""" The definition is considered ready for use
	"""
	
	withdrawn = "withdrawn"
	""" The definition should no longer be used
	"""
	
	unknown = "unknown"
	""" The authoring system does not know which of the status values currently applies for this definition.
	"""



class DetectedIssueSeverity(object):
	""" Indicates the potential degree of impact of the identified issue on the patient.

	URL: http://hl7.org/fhir/detectedissue-severity
	ValueSet: http://hl7.org/fhir/ValueSet/detectedissue-severity
	"""
	
	high = "high"
	""" Indicates the issue may be life-threatening or has the potential to cause permanent injury.
	"""
	
	moderate = "moderate"
	""" Indicates the issue may result in noticeable adverse consequences but is unlikely to be life-threatening or
	/// cause permanent injury.
	"""
	
	low = "low"
	""" Indicates the issue may result in some adverse consequences but is unlikely to substantially affect the
	/// situation of the subject.
	"""



class DeviceMetricCalibrationState(object):
	""" Describes the state of a metric calibration.

	URL: http://hl7.org/fhir/metric-calibration-state
	ValueSet: http://hl7.org/fhir/ValueSet/metric-calibration-state
	"""
	
	notCalibrated = "not-calibrated"
	""" The metric has not been calibrated.
	"""
	
	calibrationRequired = "calibration-required"
	""" The metric needs to be calibrated.
	"""
	
	calibrated = "calibrated"
	""" The metric has been calibrated.
	"""
	
	unspecified = "unspecified"
	""" The state of calibration of this metric is unspecified.
	"""



class DeviceMetricCalibrationType(object):
	""" Describes the type of a metric calibration.

	URL: http://hl7.org/fhir/metric-calibration-type
	ValueSet: http://hl7.org/fhir/ValueSet/metric-calibration-type
	"""
	
	unspecified = "unspecified"
	""" TODO
	"""
	
	offset = "offset"
	""" TODO
	"""
	
	gain = "gain"
	""" TODO
	"""
	
	twoPoint = "two-point"
	""" TODO
	"""



class DeviceMetricCategory(object):
	""" Describes the category of the metric.

	URL: http://hl7.org/fhir/metric-category
	ValueSet: http://hl7.org/fhir/ValueSet/metric-category
	"""
	
	measurement = "measurement"
	""" DeviceObservations generated for this DeviceMetric are measured.
	"""
	
	setting = "setting"
	""" DeviceObservations generated for this DeviceMetric is a setting that will influence the behavior of the Device.
	"""
	
	calculation = "calculation"
	""" DeviceObservations generated for this DeviceMetric are calculated.
	"""
	
	unspecified = "unspecified"
	""" The category of this DeviceMetric is unspecified.
	"""



class DeviceMetricColor(object):
	""" Describes the typical color of representation.

	URL: http://hl7.org/fhir/metric-color
	ValueSet: http://hl7.org/fhir/ValueSet/metric-color
	"""
	
	black = "black"
	""" Color for representation - black.
	"""
	
	red = "red"
	""" Color for representation - red.
	"""
	
	green = "green"
	""" Color for representation - green.
	"""
	
	yellow = "yellow"
	""" Color for representation - yellow.
	"""
	
	blue = "blue"
	""" Color for representation - blue.
	"""
	
	magenta = "magenta"
	""" Color for representation - magenta.
	"""
	
	cyan = "cyan"
	""" Color for representation - cyan.
	"""
	
	white = "white"
	""" Color for representation - white.
	"""



class DeviceMetricOperationalStatus(object):
	""" Describes the operational status of the DeviceMetric.

	URL: http://hl7.org/fhir/metric-operational-status
	ValueSet: http://hl7.org/fhir/ValueSet/metric-operational-status
	"""
	
	on = "on"
	""" The DeviceMetric is operating and will generate DeviceObservations.
	"""
	
	off = "off"
	""" The DeviceMetric is not operating.
	"""
	
	standby = "standby"
	""" The DeviceMetric is operating, but will not generate any DeviceObservations.
	"""



class DeviceStatus(object):
	""" The availability status of the device.

	URL: http://hl7.org/fhir/devicestatus
	ValueSet: http://hl7.org/fhir/ValueSet/devicestatus
	"""
	
	available = "available"
	""" The Device is available for use.
	"""
	
	notAvailable = "not-available"
	""" The Device is no longer available for use (e.g. lost, expired, damaged).
	"""
	
	enteredInError = "entered-in-error"
	""" The Device was entered in error and voided.
	"""



class DiagnosticReportStatus(object):
	""" The status of the diagnostic report as a whole.

	URL: http://hl7.org/fhir/diagnostic-report-status
	ValueSet: http://hl7.org/fhir/ValueSet/diagnostic-report-status
	"""
	
	registered = "registered"
	""" The existence of the report is registered, but there is nothing yet available.
	"""
	
	partial = "partial"
	""" This is a partial (e.g. initial, interim or preliminary) report: data in the report may be incomplete or
	/// unverified.
	"""
	
	final = "final"
	""" The report is complete and verified by an authorized person.
	"""
	
	corrected = "corrected"
	""" The report has been modified subsequent to being Final, and is complete and verified by an authorized person
	"""
	
	appended = "appended"
	""" The report has been modified subsequent to being Final, and is complete and verified by an authorized person.
	/// New content has been added, but existing content hasn't changed.
	"""
	
	cancelled = "cancelled"
	""" The report is unavailable because the measurement was not started or not completed (also sometimes called
	/// "aborted").
	"""
	
	enteredInError = "entered-in-error"
	""" The report has been withdrawn following a previous final release.
	"""



class DigitalMediaType(object):
	""" Whether the Media is a photo, video, or audio

	URL: http://hl7.org/fhir/digital-media-type
	ValueSet: http://hl7.org/fhir/ValueSet/digital-media-type
	"""
	
	photo = "photo"
	""" The media consists of one or more unmoving images, including photographs, computer-generated graphs and charts,
	/// and scanned documents
	"""
	
	video = "video"
	""" The media consists of a series of frames that capture a moving image
	"""
	
	audio = "audio"
	""" The media consists of a sound recording
	"""



class DocumentMode(object):
	""" Whether the application produces or consumes documents.

	URL: http://hl7.org/fhir/document-mode
	ValueSet: http://hl7.org/fhir/ValueSet/document-mode
	"""
	
	producer = "producer"
	""" The application produces documents of the specified type.
	"""
	
	consumer = "consumer"
	""" The application consumes documents of the specified type.
	"""



class DocumentReferenceStatus(object):
	""" The status of the document reference.

	URL: http://hl7.org/fhir/document-reference-status
	ValueSet: http://hl7.org/fhir/ValueSet/document-reference-status
	"""
	
	current = "current"
	""" This is the current reference for this document.
	"""
	
	superseded = "superseded"
	""" This reference has been superseded by another reference.
	"""
	
	enteredInError = "entered-in-error"
	""" This reference was created in error.
	"""



class DocumentRelationshipType(object):
	""" The type of relationship between documents.

	URL: http://hl7.org/fhir/document-relationship-type
	ValueSet: http://hl7.org/fhir/ValueSet/document-relationship-type
	"""
	
	replaces = "replaces"
	""" This document logically replaces or supersedes the target document.
	"""
	
	transforms = "transforms"
	""" This document was generated by transforming the target document (e.g. format or language conversion).
	"""
	
	signs = "signs"
	""" This document is a signature of the target document.
	"""
	
	appends = "appends"
	""" This document adds additional information to the target document.
	"""



class EncounterLocationStatus(object):
	""" The status of the location.

	URL: http://hl7.org/fhir/encounter-location-status
	ValueSet: http://hl7.org/fhir/ValueSet/encounter-location-status
	"""
	
	planned = "planned"
	""" The patient is planned to be moved to this location at some point in the future.
	"""
	
	active = "active"
	""" The patient is currently at this location, or was between the period specified.
	/// 
	/// A system may update these records when the patient leaves the location to either reserved, or completed
	"""
	
	reserved = "reserved"
	""" This location is held empty for this patient.
	"""
	
	completed = "completed"
	""" The patient was at this location during the period specified.
	/// 
	/// Not to be used when the patient is currently at the location
	"""



class EncounterStatus(object):
	""" Current state of the encounter

	URL: http://hl7.org/fhir/encounter-status
	ValueSet: http://hl7.org/fhir/ValueSet/encounter-status
	"""
	
	planned = "planned"
	""" The Encounter has not yet started.
	"""
	
	arrived = "arrived"
	""" The Patient is present for the encounter, however is not currently meeting with a practitioner.
	"""
	
	inProgress = "in-progress"
	""" The Encounter has begun and the patient is present / the practitioner and the patient are meeting.
	"""
	
	onleave = "onleave"
	""" The Encounter has begun, but the patient is temporarily on leave.
	"""
	
	finished = "finished"
	""" The Encounter has ended.
	"""
	
	cancelled = "cancelled"
	""" The Encounter has ended before it has begun.
	"""
	
	enteredInError = "entered-in-error"
	""" This instance should not have been part of this patient's medical record.
	"""



class EndpointStatus(object):
	""" The status of the endpoint

	URL: http://hl7.org/fhir/endpoint-status
	ValueSet: http://hl7.org/fhir/ValueSet/endpoint-status
	"""
	
	active = "active"
	""" This endpoint is expected to be active and can be used
	"""
	
	suspended = "suspended"
	""" This endpoint is temporarily unavailable
	"""
	
	error = "error"
	""" This endpoint has exceeded connectivity thresholds and is considered in an error state and should no longer be
	/// attempted to connect to until corrective action is taken
	"""
	
	off = "off"
	""" This endpoint is no longer to be used
	"""
	
	enteredInError = "entered-in-error"
	""" This instance should not have been part of this patient's medical record.
	"""
	
	test = "test"
	""" This endpoint is not intended for production usage.
	"""



class EpisodeOfCareStatus(object):
	""" The status of the episode of care.

	URL: http://hl7.org/fhir/episode-of-care-status
	ValueSet: http://hl7.org/fhir/ValueSet/episode-of-care-status
	"""
	
	planned = "planned"
	""" This episode of care is planned to start at the date specified in the period.start. During this status an
	/// organization may perform assessments to determine if they are eligible to receive services, or be organizing to
	/// make resources available to provide care services.
	"""
	
	waitlist = "waitlist"
	""" This episode has been placed on a waitlist, pending the episode being made active (or cancelled).
	"""
	
	active = "active"
	""" This episode of care is current.
	"""
	
	onhold = "onhold"
	""" This episode of care is on hold, the organization has limited responsibility for the patient (such as while on
	/// respite).
	"""
	
	finished = "finished"
	""" This episode of care is finished at the organization is not expecting to be providing care to the patient. Can
	/// also be known as "closed", "completed" or other similar terms.
	"""
	
	cancelled = "cancelled"
	""" The episode of care was cancelled, or withdrawn from service, often selected during the planned stage as the
	/// patient may have gone elsewhere, or the circumstances have changed and the organization is unable to provide the
	/// care. It indicates that services terminated outside the planned/expected workflow.
	"""
	
	enteredInError = "entered-in-error"
	""" This instance should not have been part of this patient's medical record.
	"""



class EventCapabilityMode(object):
	""" The mode of a message capability statement.

	URL: http://hl7.org/fhir/event-capability-mode
	ValueSet: http://hl7.org/fhir/ValueSet/event-capability-mode
	"""
	
	sender = "sender"
	""" The application sends requests and receives responses.
	"""
	
	receiver = "receiver"
	""" The application receives requests and sends responses.
	"""



class EventStatus(object):
	""" Codes identifying the stage lifecycle stage of a event

	URL: http://hl7.org/fhir/event-status
	ValueSet: http://hl7.org/fhir/ValueSet/event-status
	"""
	
	preparation = "preparation"
	""" The core event has not started yet, but some staging activities have begun (e.g. surgical suite preparation).
	/// Preparation stages may be tracked for billing purposes.
	"""
	
	inProgress = "in-progress"
	""" The event is currently occurring
	"""
	
	suspended = "suspended"
	""" The event has been temporarily stopped but is expected to resume in the future
	"""
	
	aborted = "aborted"
	""" The event was  prior to the full completion of the intended actions
	"""
	
	completed = "completed"
	""" The event has now concluded
	"""
	
	enteredInError = "entered-in-error"
	""" This electronic record should never have existed, though it is possible that real-world decisions were based on
	/// it.  (If real-world activity has occurred, the status should be "cancelled" rather than "entered-in-error".)
	"""
	
	unknown = "unknown"
	""" The authoring system does not know which of the status values currently applies for this event
	"""



class EventTiming(object):
	""" Real world event that the relating to the schedule.

	URL: http://hl7.org/fhir/event-timing
	ValueSet: http://hl7.org/fhir/ValueSet/event-timing
	"""
	
	MORN = "MORN"
	""" event occurs during the morning
	"""
	
	AFT = "AFT"
	""" event occurs during the afternoon
	"""
	
	EVE = "EVE"
	""" event occurs during the evening
	"""
	
	NIGHT = "NIGHT"
	""" event occurs during the night
	"""



class ExplanationOfBenefitStatus(object):
	""" A code specifying the state of the resource instance.

	URL: http://hl7.org/fhir/explanationofbenefit-status
	ValueSet: http://hl7.org/fhir/ValueSet/explanationofbenefit-status
	"""
	
	active = "active"
	""" The resource instance is currently in-force.
	"""
	
	cancelled = "cancelled"
	""" The resource instance is withdrawn, rescinded or reversed.
	"""
	
	draft = "draft"
	""" A new resource instance the contents of which is not complete.
	"""
	
	enteredInError = "entered-in-error"
	""" The resource instance was entered in error.
	"""



class ExtensionContext(object):
	""" How an extension context is interpreted.

	URL: http://hl7.org/fhir/extension-context
	ValueSet: http://hl7.org/fhir/ValueSet/extension-context
	"""
	
	resource = "resource"
	""" The context is all elements matching a particular resource element path.
	"""
	
	datatype = "datatype"
	""" The context is all nodes matching a particular data type element path (root or repeating element) or all
	/// elements referencing a particular primitive data type (expressed as the datatype name).
	"""
	
	extension = "extension"
	""" The context is a particular extension from a particular profile, a uri that identifies the extension definition.
	"""



class FHIRDefinedConceptProperties(object):
	""" A set of common concept properties for use on coded systems through out the FHIR eco-system.

	URL: http://hl7.org/fhir/concept-properties
	ValueSet: http://hl7.org/fhir/ValueSet/concept-properties
	"""
	
	inactive = "inactive"
	""" True if the concept is not considered active - e.g. not a valid concept any more. Property type is boolean,
	/// default value is false
	"""
	
	deprecated = "deprecated"
	""" The date at which a concept was deprecated. Concepts that are deprecated but not inactive can still be used, but
	/// their use is discouraged, and they should be expected to be made inactive in a future release. Property type is
	/// dateTime
	"""
	
	notSelectable = "notSelectable"
	""" The concept is not intended to be chosen by the user - only intended to be used as a selector for other
	/// concepts. Note, though, that the interpretation of this is highly contextual; all concepts are selectable in
	/// some context. Property type is boolean, default value is false
	"""
	
	parent = "parent"
	""" The concept identified in this property is a parent of the concept on which it is a property. The property type
	/// will be 'code'. The meaning of 'parent' is defined by the heirarchyMeaning attribute
	"""
	
	child = "child"
	""" The concept identified in this property is a child of the concept on which it is a property. The property type
	/// will be 'code'. The meaning of 'child' is defined by the heirarchyMeaning attribute
	"""



class FHIRRestfulInteractions(object):
	""" The set of interactions defined by the RESTful part of the FHIR specification.

	URL: http://hl7.org/fhir/restful-interaction
	ValueSet: http://hl7.org/fhir/ValueSet/restful-interaction
	"""
	
	read = "read"
	""" Read the current state of the resource.
	"""
	
	vread = "vread"
	""" Read the state of a specific version of the resource.
	"""
	
	update = "update"
	""" Update an existing resource by its id (or create it if it is new).
	"""
	
	patch = "patch"
	""" Update an existing resource by posting a set of changes to it.
	"""
	
	delete = "delete"
	""" Delete a resource.
	"""
	
	history = "history"
	""" Retrieve the change history for a particular resource, type of resource, or the entire system.
	"""
	
	historyInstance = "history-instance"
	""" Retrieve the change history for a particular resource.
	"""
	
	historyType = "history-type"
	""" Retrieve the change history for all resources of a particular type.
	"""
	
	historySystem = "history-system"
	""" Retrieve the change history for all resources on a system.
	"""
	
	create = "create"
	""" Create a new resource with a server assigned id.
	"""
	
	search = "search"
	""" Search a resource type or all resources based on some filter criteria.
	"""
	
	searchType = "search-type"
	""" Search all resources of the specified type based on some filter criteria.
	"""
	
	searchSystem = "search-system"
	""" Search all resources based on some filter criteria.
	"""
	
	capabilities = "capabilities"
	""" Get a Capability Statement for the system.
	"""
	
	transaction = "transaction"
	""" Update, create or delete a set of resources as a single transaction.
	"""
	
	batch = "batch"
	""" perform a set of a separate interactions in a single http operation
	"""
	
	operation = "operation"
	""" Perform an operation as defined by an OperationDefinition.
	"""



class FamilyHistoryStatus(object):
	""" A code that identifies the status of the family history record.

	URL: http://hl7.org/fhir/history-status
	ValueSet: http://hl7.org/fhir/ValueSet/history-status
	"""
	
	partial = "partial"
	""" Some health information is known and captured, but not complete - see notes for details.
	"""
	
	completed = "completed"
	""" All available related health information is captured as of the date (and possibly time) when the family member
	/// history was taken.
	"""
	
	enteredInError = "entered-in-error"
	""" This instance should not have been part of this patient's medical record.
	"""
	
	healthUnknown = "health-unknown"
	""" Health information for this individual is unavailable/unknown.
	"""



class FilterOperator(object):
	""" The kind of operation to perform as a part of a property based filter.

	URL: http://hl7.org/fhir/filter-operator
	ValueSet: http://hl7.org/fhir/ValueSet/filter-operator
	"""
	
	eq = "="
	""" The specified property of the code equals the provided value.
	"""
	
	isA = "is-a"
	""" Includes all concept ids that have a transitive is-a relationship with the concept Id provided as the value,
	/// including the provided concept itself (i.e. include child codes)
	"""
	
	descendentOf = "descendent-of"
	""" Includes all concept ids that have a transitive is-a relationship with the concept Id provided as the value,
	/// excluding the provided concept itself (i.e. include child codes)
	"""
	
	isNotA = "is-not-a"
	""" The specified property of the code does not have an is-a relationship with the provided value.
	"""
	
	regex = "regex"
	""" The specified property of the code  matches the regex specified in the provided value.
	"""
	
	# in = "in"
	""" The specified property of the code is in the set of codes or concepts specified in the provided value (comma
	/// separated list).
	"""
	
	notIn = "not-in"
	""" The specified property of the code is not in the set of codes or concepts specified in the provided value (comma
	/// separated list).
	"""
	
	generalizes = "generalizes"
	""" Includes all concept ids that have a transitive is-a relationship from the concept Id provided as the value,
	/// including the provided concept itself (e.g. include parent codes)
	"""
	
	exists = "exists"
	""" The specified property of the code has at least one value (if the specified value is true; if the specified
	/// value is false, then matches when the specified property of the code has no values)
	"""



class FlagStatus(object):
	""" Indicates whether this flag is active and needs to be displayed to a user, or whether it is no longer needed or entered
in error.

	URL: http://hl7.org/fhir/flag-status
	ValueSet: http://hl7.org/fhir/ValueSet/flag-status
	"""
	
	active = "active"
	""" A current flag that should be displayed to a user. A system may use the category to determine which roles should
	/// view the flag.
	"""
	
	inactive = "inactive"
	""" The flag does not need to be displayed any more.
	"""
	
	enteredInError = "entered-in-error"
	""" The flag was added in error, and should no longer be displayed.
	"""



class GoalAcceptanceStatus(object):
	""" Codes indicating whether the goal has been accepted by a stakeholder

	URL: http://hl7.org/fhir/goal-acceptance-status
	ValueSet: http://hl7.org/fhir/ValueSet/goal-acceptance-status
	"""
	
	agree = "agree"
	""" Stakeholder supports pursuit of the goal
	"""
	
	disagree = "disagree"
	""" Stakeholder is not in support of the pursuit of the goal
	"""
	
	pending = "pending"
	""" Stakeholder has not yet made a decision on whether they support the goal
	"""



class GoalRelationshipType(object):
	""" Types of relationships between two goals

	URL: http://hl7.org/fhir/goal-relationship-type
	ValueSet: http://hl7.org/fhir/ValueSet/goal-relationship-type
	"""
	
	predecessor = "predecessor"
	""" Indicates that the target goal is one which must be met before striving for the current goal
	"""
	
	successor = "successor"
	""" Indicates that the target goal is a desired objective once the current goal is met
	"""
	
	replacement = "replacement"
	""" Indicates that this goal has been replaced by the target goal
	"""
	
	component = "component"
	""" Indicates that the target goal is considered to be a "piece" of attaining this goal.
	"""
	
	other = "other"
	""" Indicates that the relationship is not covered by one of the pre-defined codes.  (An extension may convey more
	/// information about the meaning of the relationship.)
	"""



class GoalStatus(object):
	""" Indicates whether the goal has been met and is still being targeted

	URL: http://hl7.org/fhir/goal-status
	ValueSet: http://hl7.org/fhir/ValueSet/goal-status
	"""
	
	proposed = "proposed"
	""" A goal is proposed for this patient
	"""
	
	planned = "planned"
	""" A goal is planned for this patient
	"""
	
	accepted = "accepted"
	""" A proposed goal was accepted
	"""
	
	rejected = "rejected"
	""" A proposed goal was rejected
	"""
	
	inProgress = "in-progress"
	""" The goal is being sought but has not yet been reached.  (Also applies if goal was reached in the past but there
	/// has been regression and goal is being sought again)
	"""
	
	achieved = "achieved"
	""" The goal has been met and no further action is needed
	"""
	
	sustaining = "sustaining"
	""" The goal has been met, but ongoing activity is needed to sustain the goal objective
	"""
	
	onHold = "on-hold"
	""" The goal remains a long term objective but is no longer being actively pursued for a temporary period of time.
	"""
	
	cancelled = "cancelled"
	""" The goal is no longer being sought
	"""
	
	onTarget = "on-target"
	""" The goal is on scheduled for the planned timelines
	"""
	
	aheadOfTarget = "ahead-of-target"
	""" The goal is ahead of the planned timelines
	"""
	
	behindTarget = "behind-target"
	""" The goal is behind the planned timelines
	"""
	
	enteredInError = "entered-in-error"
	""" The goal was entered in error and voided.
	"""



class GroupType(object):
	""" Types of resources that are part of group

	URL: http://hl7.org/fhir/group-type
	ValueSet: http://hl7.org/fhir/ValueSet/group-type
	"""
	
	person = "person"
	""" Group contains "person" Patient resources
	"""
	
	animal = "animal"
	""" Group contains "animal" Patient resources
	"""
	
	practitioner = "practitioner"
	""" Group contains healthcare practitioner resources
	"""
	
	device = "device"
	""" Group contains Device resources
	"""
	
	medication = "medication"
	""" Group contains Medication resources
	"""
	
	substance = "substance"
	""" Group contains Substance resources
	"""



class GuidanceResponseStatus(object):
	""" The status of a guidance response

	URL: http://hl7.org/fhir/guidance-response-status
	ValueSet: http://hl7.org/fhir/ValueSet/guidance-response-status
	"""
	
	success = "success"
	""" The request was processed successfully
	"""
	
	dataRequested = "data-requested"
	""" The request was processed successfully, but more data may result in a more complete evaluation
	"""
	
	dataRequired = "data-required"
	""" The request was processed, but more data is required to complete the evaluation
	"""
	
	inProgress = "in-progress"
	""" The request is currently being processed
	"""
	
	failure = "failure"
	""" The request was not processed successfully
	"""



class GuideDependencyType(object):
	""" How a dependency is represented when the guide is published.

	URL: http://hl7.org/fhir/guide-dependency-type
	ValueSet: http://hl7.org/fhir/ValueSet/guide-dependency-type
	"""
	
	reference = "reference"
	""" The guide is referred to by URL.
	"""
	
	inclusion = "inclusion"
	""" The guide is embedded in this guide when published.
	"""



class GuidePageKind(object):
	""" The kind of an included page.

	URL: http://hl7.org/fhir/guide-page-kind
	ValueSet: http://hl7.org/fhir/ValueSet/guide-page-kind
	"""
	
	page = "page"
	""" This is a page of content that is included in the implementation guide. It has no particular function.
	"""
	
	example = "example"
	""" This is a page that represents a human readable rendering of an example.
	"""
	
	list = "list"
	""" This is a page that represents a list of resources of one or more types.
	"""
	
	include = "include"
	""" This is a page showing where an included guide is injected.
	"""
	
	directory = "directory"
	""" This is a page that lists the resources of a given type, and also creates pages for all the listed types as
	/// other pages in the section.
	"""
	
	dictionary = "dictionary"
	""" This is a page that creates the listed resources as a dictionary.
	"""
	
	toc = "toc"
	""" This is a generated page that contains the table of contents.
	"""
	
	resource = "resource"
	""" This is a page that represents a presented resource. This is typically used for generated conformance resource
	/// presentations.
	"""



class HL7Workgroup(object):
	""" An HL7 administrative unit that owns artifacts in the FHIR specification

	URL: http://hl7.org/fhir/hl7-work-group
	ValueSet: http://hl7.org/fhir/ValueSet/hl7-work-group
	"""
	
	cbcc = "cbcc"
	""" Community Based Collaborative Care (http://www.hl7.org/Special/committees/cbcc/index.cfm)
	"""
	
	cds = "cds"
	""" Clinical Decision Support (http://www.hl7.org/Special/committees/dss/index.cfm)
	"""
	
	cqi = "cqi"
	""" Clinical Quality Information (http://www.hl7.org/Special/committees/cqi/index.cfm)
	"""
	
	cg = "cg"
	""" Clinical Genomics (http://www.hl7.org/Special/committees/clingenomics/index.cfm)
	"""
	
	dev = "dev"
	""" Health Care Devices (http://www.hl7.org/Special/committees/healthcaredevices/index.cfm)
	"""
	
	ehr = "ehr"
	""" Electronic Health Records (http://www.hl7.org/special/committees/ehr/index.cfm)
	"""
	
	fhir = "fhir"
	""" FHIR Infrastructure (http://www.hl7.org/Special/committees/fiwg/index.cfm)
	"""
	
	fm = "fm"
	""" Financial Management (http://www.hl7.org/Special/committees/fm/index.cfm)
	"""
	
	hsi = "hsi"
	""" Health Standards Integration (http://www.hl7.org/Special/committees/hsi/index.cfm)
	"""
	
	ii = "ii"
	""" Imaging Integration (http://www.hl7.org/Special/committees/imagemgt/index.cfm)
	"""
	
	inm = "inm"
	""" Infrastructure And Messaging (http://www.hl7.org/special/committees/inm/index.cfm)
	"""
	
	its = "its"
	""" Implementable Technology Specifications (http://www.hl7.org/special/committees/xml/index.cfm)
	"""
	
	oo = "oo"
	""" Orders and Observations (http://www.hl7.org/Special/committees/orders/index.cfm)
	"""
	
	pa = "pa"
	""" Patient Administration (http://www.hl7.org/Special/committees/pafm/index.cfm)
	"""
	
	pc = "pc"
	""" Patient Care (http://www.hl7.org/Special/committees/patientcare/index.cfm)
	"""
	
	pher = "pher"
	""" Public Health and Emergency Response (http://www.hl7.org/Special/committees/pher/index.cfm)
	"""
	
	phx = "phx"
	""" Pharmacy (http://www.hl7.org/Special/committees/medication/index.cfm)
	"""
	
	rcrim = "rcrim"
	""" Regulated Clinical Research Information Management (http://www.hl7.org/Special/committees/rcrim/index.cfm)
	"""
	
	sd = "sd"
	""" Structured Documents (http://www.hl7.org/Special/committees/structure/index.cfm)
	"""
	
	sec = "sec"
	""" Security (http://www.hl7.org/Special/committees/secure/index.cfm)
	"""
	
	us = "us"
	""" US Realm Taskforce (http://wiki.hl7.org/index.php?title=US_Realm_Task_Force)
	"""
	
	vocab = "vocab"
	""" Vocabulary (http://www.hl7.org/Special/committees/Vocab/index.cfm)
	"""
	
	aid = "aid"
	""" Application Implementation and Design (http://www.hl7.org/Special/committees/java/index.cfm)
	"""



class HTTPVerb(object):
	""" HTTP verbs (in the HTTP command line).

	URL: http://hl7.org/fhir/http-verb
	ValueSet: http://hl7.org/fhir/ValueSet/http-verb
	"""
	
	GET = "GET"
	""" HTTP GET
	"""
	
	POST = "POST"
	""" HTTP POST
	"""
	
	PUT = "PUT"
	""" HTTP PUT
	"""
	
	DELETE = "DELETE"
	""" HTTP DELETE
	"""



class HumanNameAssemblyOrder(object):
	""" A code that represents the preferred display order of the components of a human name

	URL: http://hl7.org/fhir/name-assembly-order
	ValueSet: http://hl7.org/fhir/ValueSet/name-assembly-order
	"""
	
	NL1 = "NL1"
	""" NL1
	"""
	
	NL2 = "NL2"
	""" NL2
	"""
	
	NL3 = "NL3"
	""" NL3
	"""
	
	NL4 = "NL4"
	""" NL4
	"""



class IdentifierUse(object):
	""" Identifies the purpose for this identifier, if known .

	URL: http://hl7.org/fhir/identifier-use
	ValueSet: http://hl7.org/fhir/ValueSet/identifier-use
	"""
	
	usual = "usual"
	""" The identifier recommended for display and use in real-world interactions.
	"""
	
	official = "official"
	""" The identifier considered to be most trusted for the identification of this item.
	"""
	
	temp = "temp"
	""" A temporary identifier.
	"""
	
	secondary = "secondary"
	""" An identifier that was assigned in secondary use - it serves to identify the object in a relative context, but
	/// cannot be consistently assigned to the same object again in a different context.
	"""



class IdentityAssuranceLevel(object):
	""" The level of confidence that this link represents the same actual person, based on NIST Authentication Levels.

	URL: http://hl7.org/fhir/identity-assuranceLevel
	ValueSet: http://hl7.org/fhir/ValueSet/identity-assuranceLevel
	"""
	
	level1 = "level1"
	""" Little or no confidence in the asserted identity's accuracy.
	"""
	
	level2 = "level2"
	""" Some confidence in the asserted identity's accuracy.
	"""
	
	level3 = "level3"
	""" High confidence in the asserted identity's accuracy.
	"""
	
	level4 = "level4"
	""" Very high confidence in the asserted identity's accuracy.
	"""



class IssueSeverity(object):
	""" How the issue affects the success of the action.

	URL: http://hl7.org/fhir/issue-severity
	ValueSet: http://hl7.org/fhir/ValueSet/issue-severity
	"""
	
	fatal = "fatal"
	""" The issue caused the action to fail, and no further checking could be performed.
	"""
	
	error = "error"
	""" The issue is sufficiently important to cause the action to fail.
	"""
	
	warning = "warning"
	""" The issue is not important enough to cause the action to fail, but may cause it to be performed suboptimally or
	/// in a way that is not as desired.
	"""
	
	information = "information"
	""" The issue has no relation to the degree of success of the action.
	"""



class IssueType(object):
	""" A code that describes the type of issue.

	URL: http://hl7.org/fhir/issue-type
	ValueSet: http://hl7.org/fhir/ValueSet/issue-type
	"""
	
	invalid = "invalid"
	""" Content invalid against the specification or a profile.
	"""
	
	structure = "structure"
	""" A structural issue in the content such as wrong namespace, or unable to parse the content completely, or invalid
	/// json syntax.
	"""
	
	required = "required"
	""" A required element is missing.
	"""
	
	value = "value"
	""" An element value is invalid.
	"""
	
	invariant = "invariant"
	""" A content validation rule failed - e.g. a schematron rule.
	"""
	
	security = "security"
	""" An authentication/authorization/permissions issue of some kind.
	"""
	
	login = "login"
	""" The client needs to initiate an authentication process.
	"""
	
	unknown = "unknown"
	""" The user or system was not able to be authenticated (either there is no process, or the proferred token is
	/// unacceptable).
	"""
	
	expired = "expired"
	""" User session expired; a login may be required.
	"""
	
	forbidden = "forbidden"
	""" The user does not have the rights to perform this action.
	"""
	
	suppressed = "suppressed"
	""" Some information was not or may not have been returned due to business rules, consent or privacy rules, or
	/// access permission constraints.  This information may be accessible through alternate processes.
	"""
	
	processing = "processing"
	""" Processing issues. These are expected to be final e.g. there is no point resubmitting the same content
	/// unchanged.
	"""
	
	notSupported = "not-supported"
	""" The resource or profile is not supported.
	"""
	
	duplicate = "duplicate"
	""" An attempt was made to create a duplicate record.
	"""
	
	notFound = "not-found"
	""" The reference provided was not found. In a pure RESTful environment, this would be an HTTP 404 error, but this
	/// code may be used where the content is not found further into the application architecture.
	"""
	
	tooLong = "too-long"
	""" Provided content is too long (typically, this is a denial of service protection type of error).
	"""
	
	codeInvalid = "code-invalid"
	""" The code or system could not be understood, or it was not valid in the context of a particular ValueSet.code.
	"""
	
	extension = "extension"
	""" An extension was found that was not acceptable, could not be resolved, or a modifierExtension was not
	/// recognized.
	"""
	
	tooCostly = "too-costly"
	""" The operation was stopped to protect server resources; e.g. a request for a value set expansion on all of SNOMED
	/// CT.
	"""
	
	businessRule = "business-rule"
	""" The content/operation failed to pass some business rule, and so could not proceed.
	"""
	
	conflict = "conflict"
	""" Content could not be accepted because of an edit conflict (i.e. version aware updates) (In a pure RESTful
	/// environment, this would be an HTTP 404 error, but this code may be used where the conflict is discovered further
	/// into the application architecture.)
	"""
	
	incomplete = "incomplete"
	""" Not all data sources typically accessed could be reached, or responded in time, so the returned information may
	/// not be complete.
	"""
	
	transient = "transient"
	""" Transient processing issues. The system receiving the error may be able to resubmit the same content once an
	/// underlying issue is resolved.
	"""
	
	lockError = "lock-error"
	""" A resource/record locking failure (usually in an underlying database).
	"""
	
	noStore = "no-store"
	""" The persistent store is unavailable; e.g. the database is down for maintenance or similar action.
	"""
	
	exception = "exception"
	""" An unexpected internal error has occurred.
	"""
	
	timeout = "timeout"
	""" An internal timeout has occurred.
	"""
	
	throttled = "throttled"
	""" The system is not prepared to handle this request due to load management.
	"""
	
	informational = "informational"
	""" A message unrelated to the processing success of the completed operation (examples of the latter include things
	/// like reminders of password expiry, system maintenance times, etc.).
	"""



class LOINC480020Answerlist(object):
	""" LOINC answer list for Genomic source class

	URL: http://hl7.org/fhir/LOINC-48002-0-answerlist
	ValueSet: http://hl7.org/fhir/ValueSet/LOINC-48002-0-answerlist
	"""
	
	LA66832 = "LA6683-2"
	""" Germline
	"""
	
	LA66840 = "LA6684-0"
	""" Somatic
	"""
	
	LA104291 = "LA10429-1"
	""" Prenatal
	"""
	
	LA181943 = "LA18194-3"
	""" Likely Germline
	"""
	
	LA181950 = "LA18195-0"
	""" Likely Somatic
	"""
	
	LA181968 = "LA18196-8"
	""" Likely Prenatal
	"""
	
	LA181976 = "LA18197-6"
	""" Unknown Genomic Origin
	"""



class LOINC480194Answerlist(object):
	""" LOINC answer list for Type of variation

	URL: http://hl7.org/fhir/LOINC-48019-4-answerlist
	ValueSet: http://hl7.org/fhir/ValueSet/LOINC-48019-4-answerlist
	"""
	
	LA96581 = "LA9658-1"
	""" Wild type
	"""
	
	LA66923 = "LA6692-3"
	""" Deletion
	"""
	
	LA66865 = "LA6686-5"
	""" Duplication
	"""
	
	LA66873 = "LA6687-3"
	""" Insertion
	"""
	
	LA66881 = "LA6688-1"
	""" Insertion/Deletion
	"""
	
	LA66899 = "LA6689-9"
	""" Inversion
	"""
	
	LA66907 = "LA6690-7"
	""" Substitution
	"""



class LOINC530345Answerlist(object):
	""" LOINC answer list for AllelicState

	URL: http://hl7.org/fhir/LOINC-53034-5-answerlist
	ValueSet: http://hl7.org/fhir/ValueSet/LOINC-53034-5-answerlist
	"""
	
	LA67038 = "LA6703-8"
	""" Heteroplasmic
	"""
	
	LA67046 = "LA6704-6"
	""" Homoplasmic
	"""
	
	LA67053 = "LA6705-3"
	""" Homozygous
	"""
	
	LA67061 = "LA6706-1"
	""" Heterozygous
	"""
	
	LA67079 = "LA6707-9"
	""" Hemizygous
	"""



class LibraryType(object):
	""" The type of knowledge asset this library contains

	URL: http://hl7.org/fhir/library-type
	ValueSet: http://hl7.org/fhir/ValueSet/library-type
	"""
	
	logicLibrary = "logic-library"
	""" The resource is a shareable library of formalized knowledge
	"""
	
	modelDefinition = "model-definition"
	""" The resource is a definition of an information model
	"""
	
	assetCollection = "asset-collection"
	""" The resource is a collection of knowledge assets
	"""
	
	moduleDefinition = "module-definition"
	""" The resource defines the dependencies, parameters, and data requirements for a particular module or evaluation
	/// context
	"""



class LinkType(object):
	""" The type of link between this patient resource and another patient resource.

	URL: http://hl7.org/fhir/link-type
	ValueSet: http://hl7.org/fhir/ValueSet/link-type
	"""
	
	replace = "replace"
	""" The patient resource containing this link must no longer be used. The link points forward to another patient
	/// resource that must be used in lieu of the patient resource that contains this link.
	"""
	
	refer = "refer"
	""" The patient resource containing this link is in use and valid but not considered the main source of information
	/// about a patient. The link points forward to another patient resource that should be consulted to retrieve
	/// additional patient information.
	"""
	
	seealso = "seealso"
	""" The patient resource containing this link is in use and valid, but points to another patient resource that is
	/// known to contain data about the same person. Data in this resource might overlap or contradict information found
	/// in the other patient resource. This link does not indicate any relative importance of the resources concerned,
	/// and both should be regarded as equally valid.
	"""



class LinkageType(object):
	""" Used to distinguish different roles a resource can play within a set of linked resources

	URL: http://hl7.org/fhir/linkage-type
	ValueSet: http://hl7.org/fhir/ValueSet/linkage-type
	"""
	
	source = "source"
	""" The record represents the "source of truth" (from the perspective of this Linkage resource) for the underlying
	/// event/condition/etc.
	"""
	
	alternate = "alternate"
	""" The record represents the alternative view of the underlying event/condition/etc.  The record may still be
	/// actively maintained, even though it is not considered to be the source of truth.
	"""
	
	historical = "historical"
	""" The record represents an obsolete record of the underlyng event/condition/etc.  It is not expected to be
	/// actively maintained.
	"""



class ListMode(object):
	""" The processing mode that applies to this list

	URL: http://hl7.org/fhir/list-mode
	ValueSet: http://hl7.org/fhir/ValueSet/list-mode
	"""
	
	working = "working"
	""" This list is the master list, maintained in an ongoing fashion with regular updates as the real world list it is
	/// tracking changes
	"""
	
	snapshot = "snapshot"
	""" This list was prepared as a snapshot. It should not be assumed to be current
	"""
	
	changes = "changes"
	""" A list that indicates where changes have been made or recommended
	"""



class ListStatus(object):
	""" The current state of the list

	URL: http://hl7.org/fhir/list-status
	ValueSet: http://hl7.org/fhir/ValueSet/list-status
	"""
	
	current = "current"
	""" The list is considered to be an active part of the patient's record.
	"""
	
	retired = "retired"
	""" The list is "old" and should no longer be considered accurate or relevant.
	"""
	
	enteredInError = "entered-in-error"
	""" The list was never accurate.  It is retained for medico-legal purposes only.
	"""



class LocationMode(object):
	""" Indicates whether a resource instance represents a specific location or a class of locations.

	URL: http://hl7.org/fhir/location-mode
	ValueSet: http://hl7.org/fhir/ValueSet/location-mode
	"""
	
	instance = "instance"
	""" The Location resource represents a specific instance of a location (e.g. Operating Theatre 1A).
	"""
	
	kind = "kind"
	""" The Location represents a class of locations (e.g. Any Operating Theatre) although this class of locations could
	/// be constrained within a specific boundary (such as organization, or parent location, address etc.).
	"""



class LocationStatus(object):
	""" Indicates whether the location is still in use.

	URL: http://hl7.org/fhir/location-status
	ValueSet: http://hl7.org/fhir/ValueSet/location-status
	"""
	
	active = "active"
	""" The location is operational.
	"""
	
	suspended = "suspended"
	""" The location is temporarily closed.
	"""
	
	inactive = "inactive"
	""" The location is no longer used.
	"""



class MPIMatch(object):
	""" A Master Patient Index (MPI) assessment of whether a candidate patient record is a match or not.

	URL: http://hl7.org/fhir/patient-mpi-match
	ValueSet: http://hl7.org/fhir/ValueSet/patient-mpi-match
	"""
	
	certain = "certain"
	""" This record meets the MPI criteria to be automatically considered as a full match.
	"""
	
	probable = "probable"
	""" This record is a close match, but not a certain match. Additional review (e.g. by a human) may be required
	/// before using this as a match.
	"""
	
	possible = "possible"
	""" This record may be a matching one. Additional review (e.g. by a human) SHOULD be performed before using this as
	/// a match.
	"""
	
	certainlyNot = "certainly-not"
	""" This record is known not to be a match. Note that usually non-matching records are not returned, but in some
	/// cases records previously or likely considered as a match may specifically be negated by the MPI.
	"""



class MatchGrade(object):
	""" A Master Patient Index (MPI) assessment of whether a candidate patient record is a match or not.

	URL: http://hl7.org/fhir/match-grade
	ValueSet: http://hl7.org/fhir/ValueSet/match-grade
	"""
	
	certain = "certain"
	""" This record meets the matching criteria to be automatically considered as a full match.
	"""
	
	probable = "probable"
	""" This record is a close match, but not a certain match. Additional review (e.g. by a human) may be required
	/// before using this as a match.
	"""
	
	possible = "possible"
	""" This record may be a matching one. Additional review (e.g. by a human) SHOULD be performed before using this as
	/// a match.
	"""
	
	certainlyNot = "certainly-not"
	""" This record is known not to be a match. Note that usually non-matching records are not returned, but in some
	/// cases records previously or likely considered as a match may specifically be negated by the matching engine
	"""



class MaxOccurs(object):
	""" Flags an element as having unlimited repetitions

	URL: http://hl7.org/fhir/question-max-occurs
	ValueSet: http://hl7.org/fhir/ValueSet/question-max-occurs
	"""
	
	max = "*"
	""" Element can repeat an unlimited number of times
	"""



class MeasmntPrinciple(object):
	""" Different measurement principle supported by the device.

	URL: http://hl7.org/fhir/measurement-principle
	ValueSet: http://hl7.org/fhir/ValueSet/measurement-principle
	"""
	
	other = "other"
	""" Measurement principle isn't in the list.
	"""
	
	chemical = "chemical"
	""" Measurement is done using the chemical principle.
	"""
	
	electrical = "electrical"
	""" Measurement is done using the electrical principle.
	"""
	
	impedance = "impedance"
	""" Measurement is done using the impedance principle.
	"""
	
	nuclear = "nuclear"
	""" Measurement is done using the nuclear principle.
	"""
	
	optical = "optical"
	""" Measurement is done using the optical principle.
	"""
	
	thermal = "thermal"
	""" Measurement is done using the thermal principle.
	"""
	
	biological = "biological"
	""" Measurement is done using the biological principle.
	"""
	
	mechanical = "mechanical"
	""" Measurement is done using the mechanical principle.
	"""
	
	acoustical = "acoustical"
	""" Measurement is done using the acoustical principle.
	"""
	
	manual = "manual"
	""" Measurement is done using the manual principle.
	"""



class MeasureDataUsage(object):
	""" The intended usage for supplemental data elements in the measure

	URL: http://hl7.org/fhir/measure-data-usage
	ValueSet: http://hl7.org/fhir/ValueSet/measure-data-usage
	"""
	
	supplementalData = "supplemental-data"
	""" The data is intended to be provided as additional information alongside the measure results
	"""
	
	riskAdjustmentFactor = "risk-adjustment-factor"
	""" The data is intended to be used to calculate and apply a risk adjustment model for the measure
	"""



class MeasurePopulationType(object):
	""" The type of population

	URL: http://hl7.org/fhir/measure-population
	ValueSet: http://hl7.org/fhir/ValueSet/measure-population
	"""
	
	initialPopulation = "initial-population"
	""" The initial population for the measure
	"""
	
	numerator = "numerator"
	""" The numerator for the measure
	"""
	
	numeratorExclusion = "numerator-exclusion"
	""" The numerator exclusion for the measure
	"""
	
	denominator = "denominator"
	""" The denominator for the measure
	"""
	
	denominatorExclusion = "denominator-exclusion"
	""" The denominator exclusion for the measure
	"""
	
	denominatorException = "denominator-exception"
	""" The denominator exception for the measure
	"""
	
	measurePopulation = "measure-population"
	""" The measure population for the measure
	"""
	
	measurePopulationExclusion = "measure-population-exclusion"
	""" The measure population exclusion for the measure
	"""
	
	measureObservation = "measure-observation"
	""" The measure observation for the measure
	"""



class MeasureReportStatus(object):
	""" The status of the measure report

	URL: http://hl7.org/fhir/measure-report-status
	ValueSet: http://hl7.org/fhir/ValueSet/measure-report-status
	"""
	
	complete = "complete"
	""" The report is complete and ready for use
	"""
	
	pending = "pending"
	""" The report is currently being generated
	"""
	
	error = "error"
	""" An error occurred attempting to generate the report
	"""



class MeasureReportType(object):
	""" The type of the measure report

	URL: http://hl7.org/fhir/measure-report-type
	ValueSet: http://hl7.org/fhir/ValueSet/measure-report-type
	"""
	
	individual = "individual"
	""" An individual report that provides information on the performance for a given measure with respect to a single
	/// patient
	"""
	
	patientList = "patient-list"
	""" A patient list report that includes a listing of patients that satisfied each population criteria in the measure
	"""
	
	summary = "summary"
	""" A summary report that returns the number of patients in each population criteria for the measure
	"""



class MeasureScoring(object):
	""" The scoring type of the measure

	URL: http://hl7.org/fhir/measure-scoring
	ValueSet: http://hl7.org/fhir/ValueSet/measure-scoring
	"""
	
	proportion = "proportion"
	""" The measure score is defined using a proportion
	"""
	
	ratio = "ratio"
	""" The measure score is defined using a ratio
	"""
	
	continuousVariable = "continuous-variable"
	""" The score is defined by a calculation of some quantity
	"""
	
	cohort = "cohort"
	""" The measure is a cohort definition
	"""



class MeasureType(object):
	""" The type of measure (includes codes from 2.16.840.1.113883.1.11.20368)

	URL: http://hl7.org/fhir/measure-type
	ValueSet: http://hl7.org/fhir/ValueSet/measure-type
	"""
	
	process = "process"
	""" A measure which focuses on a process which leads to a certain outcome, meaning that a scientific basis exists
	/// for believing that the process, when executed well, will increase the probability of achieving a desired outcome
	"""
	
	outcome = "outcome"
	""" A measure that indicates the result of the performance (or non-performance) of a function or process
	"""
	
	structure = "structure"
	""" A measure that focuses on a health care provider's capacity, systems, and processes to provide high-quality care
	"""
	
	patientReportedOutcome = "patient-reported-outcome"
	""" A measure that focuses on patient-reported information
	"""
	
	composite = "composite"
	""" A measure that combines multiple component measures in to a single quality measure
	"""



class MedicationAdministrationStatus(object):
	""" A set of codes indicating the current status of a MedicationAdministration.

	URL: http://hl7.org/fhir/medication-admin-status
	ValueSet: http://hl7.org/fhir/ValueSet/medication-admin-status
	"""
	
	inProgress = "in-progress"
	""" The administration has started but has not yet completed.
	"""
	
	onHold = "on-hold"
	""" Actions implied by the administration have been temporarily halted, but are expected to continue later. May also
	/// be called "suspended".
	"""
	
	completed = "completed"
	""" All actions that are implied by the administration have occurred.
	"""
	
	enteredInError = "entered-in-error"
	""" The administration was entered in error and therefore nullified.
	"""
	
	stopped = "stopped"
	""" Actions implied by the administration have been permanently halted, before all of them occurred.
	"""



class MedicationDispenseStatus(object):
	""" A coded concept specifying the state of the dispense event.

	URL: http://hl7.org/fhir/medication-dispense-status
	ValueSet: http://hl7.org/fhir/ValueSet/medication-dispense-status
	"""
	
	inProgress = "in-progress"
	""" The dispense has started but has not yet completed.
	"""
	
	onHold = "on-hold"
	""" Actions implied by the administration have been temporarily halted, but are expected to continue later. May also
	/// be called "suspended"
	"""
	
	completed = "completed"
	""" All actions that are implied by the dispense have occurred.
	"""
	
	enteredInError = "entered-in-error"
	""" The dispense was entered in error and therefore nullified.
	"""
	
	stopped = "stopped"
	""" Actions implied by the dispense have been permanently halted, before all of them occurred.
	"""



class MedicationRequestCategory(object):
	""" A coded concept identifying where the medication ordered is expected to be consumed or administered

	URL: http://hl7.org/fhir/medication-request-category
	ValueSet: http://hl7.org/fhir/ValueSet/medication-request-category
	"""
	
	inpatient = "inpatient"
	""" Includes orders for medications to be administered or consumed in an inpatient or acute care setting
	"""
	
	outpatient = "outpatient"
	""" Includes orders for medications to be administered or consumed in an outpatient setting (for example, Emergency
	/// Department, Outpatient Clinic, Outpatient Surgery, Doctor's office)
	"""
	
	community = "community"
	""" Includes orders for medications to be administered or consumed by the patient in their home (this would include
	/// long term care or nursing homes, hospices, etc)
	"""



class MedicationRequestStatus(object):
	""" A coded concept specifying the state of the prescribing event. Describes the lifecycle of the prescription

	URL: http://hl7.org/fhir/medication-request-status
	ValueSet: http://hl7.org/fhir/ValueSet/medication-request-status
	"""
	
	active = "active"
	""" The prescription is 'actionable', but not all actions that are implied by it have occurred yet.
	"""
	
	onHold = "on-hold"
	""" Actions implied by the prescription are to be temporarily halted, but are expected to continue later.  May also
	/// be called "suspended".
	"""
	
	cancelled = "cancelled"
	""" The prescription has been withdrawn.
	"""
	
	completed = "completed"
	""" All actions that are implied by the prescription have occurred.
	"""
	
	enteredInError = "entered-in-error"
	""" The prescription was entered in error.
	"""
	
	stopped = "stopped"
	""" Actions implied by the prescription are to be permanently halted, before all of them occurred.
	"""
	
	draft = "draft"
	""" The prescription is not yet 'actionable', i.e. it is a work in progress, requires sign-off or verification, and
	/// needs to be run through decision support process.
	"""



class MedicationStatementCategory(object):
	""" A coded concept identifying where the medication included in the medicationstatement is expected to be consumed or
administered

	URL: http://hl7.org/fhir/medication-statement-category
	ValueSet: http://hl7.org/fhir/ValueSet/medication-statement-category
	"""
	
	inpatient = "inpatient"
	""" Includes orders for medications to be administered or consumed in an inpatient or acute care setting
	"""
	
	outpatient = "outpatient"
	""" Includes orders for medications to be administered or consumed in an outpatient setting (for example, Emergency
	/// Department, Outpatient Clinic, Outpatient Surgery, Doctor's office)
	"""
	
	community = "community"
	""" Includes orders for medications to be administered or consumed by the patient in their home (this would include
	/// long term care or nursing homes, hospices, etc)
	"""
	
	patientspecified = "patientspecified"
	""" Includes statements about medication use, including over the counter medication, provided by the patient, agent
	/// or another provider
	"""



class MedicationStatementNotTaken(object):
	""" A coded concept identifying level of certainty if patient has taken or has not taken the medication

	URL: http://hl7.org/fhir/medication-statement-nottaken
	ValueSet: http://hl7.org/fhir/ValueSet/medication-statement-nottaken
	"""
	
	Y = "y"
	""" Positive assertion that patient has taken medication
	"""
	
	N = "n"
	""" Negative assertion that patient has not taken medication
	"""
	
	unk = "unk"
	""" Unknown assertion if patient has taken medication
	"""



class MedicationStatementStatus(object):
	""" A coded concept indicating the current status of a MedicationStatement.

	URL: http://hl7.org/fhir/medication-statement-status
	ValueSet: http://hl7.org/fhir/ValueSet/medication-statement-status
	"""
	
	active = "active"
	""" The medication is still being taken.
	"""
	
	completed = "completed"
	""" The medication is no longer being taken.
	"""
	
	enteredInError = "entered-in-error"
	""" The statement was entered in error.
	"""
	
	intended = "intended"
	""" The medication may be taken at some time in the future.
	"""
	
	stopped = "stopped"
	""" Actions implied by the statement have been permanently halted, before all of them occurred.
	"""
	
	onHold = "on-hold"
	""" Actions implied by the statement have been temporarily halted, but are expected to continue later. May also be
	/// called "suspended".
	"""



class MessageEvent(object):
	""" One of the message events defined as part of FHIR.

	URL: http://hl7.org/fhir/message-events
	ValueSet: http://hl7.org/fhir/ValueSet/message-events
	"""
	
	codeSystemExpand = "CodeSystem-expand"
	""" The definition of a code system is used to create a simple collection of codes suitable for use for data entry
	/// or validation. An expanded code system will be returned, or an error message.
	"""
	
	medicationAdministrationComplete = "MedicationAdministration-Complete"
	""" Change the status of a Medication Administration to show that it is complete.
	"""
	
	medicationAdministrationNullification = "MedicationAdministration-Nullification"
	""" Someone wishes to record that the record of administration of a medication is in error and should be ignored.
	"""
	
	medicationAdministrationRecording = "MedicationAdministration-Recording"
	""" Indicates that a medication has been recorded against the patient's record.
	"""
	
	medicationAdministrationUpdate = "MedicationAdministration-Update"
	""" Update a Medication Administration record.
	"""
	
	adminNotify = "admin-notify"
	""" Notification of a change to an administrative resource (either create or update). Note that there is no delete,
	/// though some administrative resources have status or period elements for this use.
	"""
	
	communicationRequest = "communication-request"
	""" Notification to convey information.
	"""
	
	diagnosticreportProvide = "diagnosticreport-provide"
	""" Provide a diagnostic report, or update a previously provided diagnostic report.
	"""
	
	observationProvide = "observation-provide"
	""" Provide a simple observation or update a previously provided simple observation.
	"""
	
	patientLink = "patient-link"
	""" Notification that two patient records actually identify the same patient.
	"""
	
	patientUnlink = "patient-unlink"
	""" Notification that previous advice that two patient records concern the same patient is now considered incorrect.
	"""
	
	valuesetExpand = "valueset-expand"
	""" The definition of a value set is used to create a simple collection of codes suitable for use for data entry or
	/// validation. An expanded value set will be returned, or an error message.
	"""



class MessageSignificanceCategory(object):
	""" The impact of the content of a message.

	URL: http://hl7.org/fhir/message-significance-category
	ValueSet: http://hl7.org/fhir/ValueSet/message-significance-category
	"""
	
	consequence = "Consequence"
	""" The message represents/requests a change that should not be processed more than once; e.g. Making a booking for
	/// an appointment.
	"""
	
	currency = "Currency"
	""" The message represents a response to query for current information. Retrospective processing is wrong and/or
	/// wasteful.
	"""
	
	notification = "Notification"
	""" The content is not necessarily intended to be current, and it can be reprocessed, though there may be version
	/// issues created by processing old notifications.
	"""



class MessageTransport(object):
	""" The protocol used for message transport.

	URL: http://hl7.org/fhir/message-transport
	ValueSet: http://hl7.org/fhir/ValueSet/message-transport
	"""
	
	http = "http"
	""" The application sends or receives messages using HTTP POST (may be over http: or https:).
	"""
	
	ftp = "ftp"
	""" The application sends or receives messages using File Transfer Protocol.
	"""
	
	mllp = "mllp"
	""" The application sends or receives messages using HL7's Minimal Lower Level Protocol.
	"""



class NHINPurposeOfUse(object):
	""" This value set is suitable for use with the provenance resource. It is derived from, but not compatible with, the HL7 v3
Purpose of use Code system.

	URL: http://healthit.gov/nhin/purposeofuse
	ValueSet: http://hl7.org/fhir/ValueSet/nhin-purposeofuse
	"""
	
	TREATMENT = "TREATMENT"
	""" Treatment
	"""
	
	PAYMENT = "PAYMENT"
	""" Payment
	"""
	
	OPERATIONS = "OPERATIONS"
	""" Healthcare Operations
	"""
	
	SYSADMIN = "SYSADMIN"
	""" System Administration
	"""
	
	FRAUD = "FRAUD"
	""" Fraud detection
	"""
	
	PSYCHOTHERAPY = "PSYCHOTHERAPY"
	""" Use or disclosure of Psychotherapy Notes
	"""
	
	TRAINING = "TRAINING"
	""" Use or disclosure by the covered entity for its own training programs
	"""
	
	LEGAL = "LEGAL"
	""" Use or disclosure by the covered entity to defend itself in a legal action
	"""
	
	MARKETING = "MARKETING"
	""" Marketing
	"""
	
	DIRECTORY = "DIRECTORY"
	""" Use and disclosure for facility directories
	"""
	
	FAMILY = "FAMILY"
	""" Disclose to a family member, other relative, or a close personal friend of the individual
	"""
	
	PRESENT = "PRESENT"
	""" Uses and disclosures with the individual present.
	"""
	
	EMERGENCY = "EMERGENCY"
	""" Permission cannot practicably be provided because of the individual's incapacity or an emergency.
	"""
	
	DISASTER = "DISASTER"
	""" Use and disclosures for disaster relief purposes.
	"""
	
	PUBLICHEALTH = "PUBLICHEALTH"
	""" Uses and disclosures for public health activities.
	"""
	
	ABUSE = "ABUSE"
	""" Disclosures about victims of abuse, neglect or domestic violence.
	"""
	
	OVERSIGHT = "OVERSIGHT"
	""" Uses and disclosures for health oversight activities.
	"""
	
	JUDICIAL = "JUDICIAL"
	""" Disclosures for judicial and administrative proceedings.
	"""
	
	LAW = "LAW"
	""" Disclosures for law enforcement purposes.
	"""
	
	DECEASED = "DECEASED"
	""" Uses and disclosures about decedents.
	"""
	
	DONATION = "DONATION"
	""" Uses and disclosures for cadaveric organ,  eye or tissue donation purposes
	"""
	
	RESEARCH = "RESEARCH"
	""" Uses and disclosures for research purposes.
	"""
	
	THREAT = "THREAT"
	""" Uses and disclosures to avert a serious threat to health or safety.
	"""
	
	GOVERNMENT = "GOVERNMENT"
	""" Uses and disclosures for specialized government functions.
	"""
	
	WORKERSCOMP = "WORKERSCOMP"
	""" Disclosures for workers' compensation.
	"""
	
	COVERAGE = "COVERAGE"
	""" Disclosures for insurance or disability coverage determination
	"""
	
	REQUEST = "REQUEST"
	""" Request of the Individual
	"""



class NameUse(object):
	""" The use of a human name

	URL: http://hl7.org/fhir/name-use
	ValueSet: http://hl7.org/fhir/ValueSet/name-use
	"""
	
	usual = "usual"
	""" Known as/conventional/the one you normally use
	"""
	
	official = "official"
	""" The formal name as registered in an official (government) registry, but which name might not be commonly used.
	/// May be called "legal name".
	"""
	
	temp = "temp"
	""" A temporary name. Name.period can provide more detailed information. This may also be used for temporary names
	/// assigned at birth or in emergency situations.
	"""
	
	nickname = "nickname"
	""" A name that is used to address the person in an informal manner, but is not part of their formal or usual name
	"""
	
	anonymous = "anonymous"
	""" Anonymous assigned name, alias, or pseudonym (used to protect a person's identity for privacy reasons)
	"""
	
	old = "old"
	""" This name is no longer in use (or was never correct, but retained for records)
	"""
	
	maiden = "maiden"
	""" A name used prior to changing name because of marriage. This name use is for use by applications that collect
	/// and store names that were used prior to a marriage. Marriage naming customs vary greatly around the world, and
	/// are constantly changing. This term is not gender specific. The use of this term does not imply any particular
	/// history for a person's name
	"""



class NamingSystemIdentifierType(object):
	""" Identifies the style of unique identifier used to identify a namespace.

	URL: http://hl7.org/fhir/namingsystem-identifier-type
	ValueSet: http://hl7.org/fhir/ValueSet/namingsystem-identifier-type
	"""
	
	oid = "oid"
	""" An ISO object identifier; e.g. 1.2.3.4.5.
	"""
	
	uuid = "uuid"
	""" A universally unique identifier of the form a5afddf4-e880-459b-876e-e4591b0acc11.
	"""
	
	uri = "uri"
	""" A uniform resource identifier (ideally a URL - uniform resource locator); e.g. http://unitsofmeasure.org.
	"""
	
	other = "other"
	""" Some other type of unique identifier; e.g. HL7-assigned reserved string such as LN for LOINC.
	"""



class NamingSystemType(object):
	""" Identifies the purpose of the naming system.

	URL: http://hl7.org/fhir/namingsystem-type
	ValueSet: http://hl7.org/fhir/ValueSet/namingsystem-type
	"""
	
	codesystem = "codesystem"
	""" The naming system is used to define concepts and symbols to represent those concepts; e.g. UCUM, LOINC, NDC
	/// code, local lab codes, etc.
	"""
	
	identifier = "identifier"
	""" The naming system is used to manage identifiers (e.g. license numbers, order numbers, etc.).
	"""
	
	root = "root"
	""" The naming system is used as the root for other identifiers and naming systems.
	"""



class NarrativeStatus(object):
	""" The status of a resource narrative

	URL: http://hl7.org/fhir/narrative-status
	ValueSet: http://hl7.org/fhir/ValueSet/narrative-status
	"""
	
	generated = "generated"
	""" The contents of the narrative are entirely generated from the structured data in the content.
	"""
	
	extensions = "extensions"
	""" The contents of the narrative are entirely generated from the structured data in the content and some of the
	/// content is generated from extensions
	"""
	
	additional = "additional"
	""" The contents of the narrative may contain additional information not found in the structured data. Note that
	/// there is no computable way to determine what the extra information is, other than by human inspection
	"""
	
	empty = "empty"
	""" The contents of the narrative are some equivalent of "No human-readable text provided in this case"
	"""



class NoteType(object):
	""" The presentation types of notes.

	URL: http://hl7.org/fhir/note-type
	ValueSet: http://hl7.org/fhir/ValueSet/note-type
	"""
	
	display = "display"
	""" Display the note.
	"""
	
	# print = "print"
	""" Print the note on the form.
	"""
	
	printoper = "printoper"
	""" Print the note for the operator.
	"""



class NutritionOrderStatus(object):
	""" Codes specifying the state of the request. Describes the lifecycle of the nutrition order.

	URL: http://hl7.org/fhir/nutrition-request-status
	ValueSet: http://hl7.org/fhir/ValueSet/nutrition-request-status
	"""
	
	proposed = "proposed"
	""" The request has been proposed.
	"""
	
	draft = "draft"
	""" The request is in preliminary form prior to being sent.
	"""
	
	planned = "planned"
	""" The request has been planned.
	"""
	
	requested = "requested"
	""" The request has been placed.
	"""
	
	active = "active"
	""" The request is 'actionable', but not all actions that are implied by it have occurred yet.
	"""
	
	onHold = "on-hold"
	""" Actions implied by the request have been temporarily halted, but are expected to continue later. May also be
	/// called "suspended".
	"""
	
	completed = "completed"
	""" All actions that are implied by the order have occurred and no continuation is planned (this will rarely be made
	/// explicit).
	"""
	
	cancelled = "cancelled"
	""" The request has been withdrawn and is no longer actionable.
	"""
	
	enteredInError = "entered-in-error"
	""" The request was entered in error and voided.
	"""



class ObservationRelationshipType(object):
	""" Codes specifying how two observations are related.

	URL: http://hl7.org/fhir/observation-relationshiptypes
	ValueSet: http://hl7.org/fhir/ValueSet/observation-relationshiptypes
	"""
	
	hasMember = "has-member"
	""" This observation is a group observation (e.g. a battery, a panel of tests, a set of vital sign measurements)
	/// that includes the target as a member of the group.
	"""
	
	derivedFrom = "derived-from"
	""" The target resource (Observation or QuestionnaireResponse) is part of the information from which this
	/// observation value is derived. (e.g. calculated anion gap, Apgar score)  NOTE:  "derived-from" is only logical
	/// choice when referencing QuestionnaireResponse.
	"""
	
	sequelTo = "sequel-to"
	""" This observation follows the target observation (e.g. timed tests such as Glucose Tolerance Test).
	"""
	
	replaces = "replaces"
	""" This observation replaces a previous observation (i.e. a revised value). The target observation is now obsolete.
	"""
	
	qualifiedBy = "qualified-by"
	""" The value of the target observation qualifies (refines) the semantics of the source observation (e.g. a lipemia
	/// measure target from a plasma measure).
	"""
	
	interferedBy = "interfered-by"
	""" The value of the target observation interferes (degrades quality, or prevents valid observation) with the
	/// semantics of the source observation (e.g. a hemolysis measure target from a plasma potassium measure which has
	/// no value).
	"""



class ObservationStatus(object):
	""" Codes providing the status of an observation.

	URL: http://hl7.org/fhir/observation-status
	ValueSet: http://hl7.org/fhir/ValueSet/observation-status
	"""
	
	registered = "registered"
	""" The existence of the observation is registered, but there is no result yet available.
	"""
	
	preliminary = "preliminary"
	""" This is an initial or interim observation: data may be incomplete or unverified.
	"""
	
	final = "final"
	""" The observation is complete.
	"""
	
	amended = "amended"
	""" The observation has been modified subsequent to being Final.
	"""
	
	cancelled = "cancelled"
	""" The observation is unavailable because the measurement was not started or not completed (also sometimes called
	/// "aborted").
	"""
	
	enteredInError = "entered-in-error"
	""" The observation has been withdrawn following previous final release.
	"""
	
	unknown = "unknown"
	""" The observation status is unknown.  Note that "unknown" is a value of last resort and every attempt should be
	/// made to provide a meaningful value other than "unknown".
	"""



class OperationKind(object):
	""" Whether an operation is a normal operation or a query.

	URL: http://hl7.org/fhir/operation-kind
	ValueSet: http://hl7.org/fhir/ValueSet/operation-kind
	"""
	
	operation = "operation"
	""" This operation is invoked as an operation.
	"""
	
	query = "query"
	""" This operation is a named query, invoked using the search mechanism.
	"""



class OperationOutcomeCodes(object):
	""" Operation Outcome codes used by FHIR test servers (see Implementation file translations.xml)

	URL: http://hl7.org/fhir/operation-outcome
	ValueSet: http://hl7.org/fhir/ValueSet/operation-outcome
	"""
	
	MSG_AUTH_REQUIRED = "MSG_AUTH_REQUIRED"
	""" MSG_AUTH_REQUIRED
	"""
	
	MSG_BAD_FORMAT = "MSG_BAD_FORMAT"
	""" MSG_BAD_FORMAT
	"""
	
	MSG_BAD_SYNTAX = "MSG_BAD_SYNTAX"
	""" MSG_BAD_SYNTAX
	"""
	
	MSG_CANT_PARSE_CONTENT = "MSG_CANT_PARSE_CONTENT"
	""" MSG_CANT_PARSE_CONTENT
	"""
	
	MSG_CANT_PARSE_ROOT = "MSG_CANT_PARSE_ROOT"
	""" MSG_CANT_PARSE_ROOT
	"""
	
	MSG_CREATED = "MSG_CREATED"
	""" MSG_CREATED
	"""
	
	MSG_DATE_FORMAT = "MSG_DATE_FORMAT"
	""" MSG_DATE_FORMAT
	"""
	
	MSG_DELETED = "MSG_DELETED"
	""" MSG_DELETED
	"""
	
	MSG_DELETED_DONE = "MSG_DELETED_DONE"
	""" MSG_DELETED_DONE
	"""
	
	MSG_DELETED_ID = "MSG_DELETED_ID"
	""" MSG_DELETED_ID
	"""
	
	MSG_DUPLICATE_ID = "MSG_DUPLICATE_ID"
	""" MSG_DUPLICATE_ID
	"""
	
	MSG_ERROR_PARSING = "MSG_ERROR_PARSING"
	""" MSG_ERROR_PARSING
	"""
	
	MSG_ID_INVALID = "MSG_ID_INVALID"
	""" MSG_ID_INVALID
	"""
	
	MSG_ID_TOO_LONG = "MSG_ID_TOO_LONG"
	""" MSG_ID_TOO_LONG
	"""
	
	MSG_INVALID_ID = "MSG_INVALID_ID"
	""" MSG_INVALID_ID
	"""
	
	MSG_JSON_OBJECT = "MSG_JSON_OBJECT"
	""" MSG_JSON_OBJECT
	"""
	
	MSG_LOCAL_FAIL = "MSG_LOCAL_FAIL"
	""" MSG_LOCAL_FAIL
	"""
	
	MSG_NO_MATCH = "MSG_NO_MATCH"
	""" MSG_NO_MATCH
	"""
	
	MSG_NO_EXIST = "MSG_NO_EXIST"
	""" MSG_NO_EXIST
	"""
	
	MSG_NO_MODULE = "MSG_NO_MODULE"
	""" MSG_NO_MODULE
	"""
	
	MSG_NO_SUMMARY = "MSG_NO_SUMMARY"
	""" MSG_NO_SUMMARY
	"""
	
	MSG_OP_NOT_ALLOWED = "MSG_OP_NOT_ALLOWED"
	""" MSG_OP_NOT_ALLOWED
	"""
	
	MSG_PARAM_CHAINED = "MSG_PARAM_CHAINED"
	""" MSG_PARAM_CHAINED
	"""
	
	MSG_PARAM_NO_REPEAT = "MSG_PARAM_NO_REPEAT"
	""" MSG_PARAM_NO_REPEAT
	"""
	
	MSG_PARAM_UNKNOWN = "MSG_PARAM_UNKNOWN"
	""" MSG_PARAM_UNKNOWN
	"""
	
	MSG_PARAM_INVALID = "MSG_PARAM_INVALID"
	""" MSG_PARAM_INVALID
	"""
	
	MSG_PARAM_MODIFIER_INVALID = "MSG_PARAM_MODIFIER_INVALID"
	""" MSG_PARAM_MODIFIER_INVALID
	"""
	
	MSG_RESOURCE_EXAMPLE_PROTECTED = "MSG_RESOURCE_EXAMPLE_PROTECTED"
	""" MSG_RESOURCE_EXAMPLE_PROTECTED
	"""
	
	MSG_RESOURCE_ID_FAIL = "MSG_RESOURCE_ID_FAIL"
	""" MSG_RESOURCE_ID_FAIL
	"""
	
	MSG_RESOURCE_NOT_ALLOWED = "MSG_RESOURCE_NOT_ALLOWED"
	""" MSG_RESOURCE_NOT_ALLOWED
	"""
	
	MSG_RESOURCE_REQUIRED = "MSG_RESOURCE_REQUIRED"
	""" MSG_RESOURCE_REQUIRED
	"""
	
	MSG_RESOURCE_ID_MISMATCH = "MSG_RESOURCE_ID_MISMATCH"
	""" MSG_RESOURCE_ID_MISMATCH
	"""
	
	MSG_RESOURCE_ID_MISSING = "MSG_RESOURCE_ID_MISSING"
	""" MSG_RESOURCE_ID_MISSING
	"""
	
	MSG_RESOURCE_TYPE_MISMATCH = "MSG_RESOURCE_TYPE_MISMATCH"
	""" MSG_RESOURCE_TYPE_MISMATCH
	"""
	
	MSG_SORT_UNKNOWN = "MSG_SORT_UNKNOWN"
	""" MSG_SORT_UNKNOWN
	"""
	
	MSG_TRANSACTION_DUPLICATE_ID = "MSG_TRANSACTION_DUPLICATE_ID"
	""" MSG_TRANSACTION_DUPLICATE_ID
	"""
	
	MSG_TRANSACTION_MISSING_ID = "MSG_TRANSACTION_MISSING_ID"
	""" MSG_TRANSACTION_MISSING_ID
	"""
	
	MSG_UNHANDLED_NODE_TYPE = "MSG_UNHANDLED_NODE_TYPE"
	""" MSG_UNHANDLED_NODE_TYPE
	"""
	
	MSG_UNKNOWN_CONTENT = "MSG_UNKNOWN_CONTENT"
	""" MSG_UNKNOWN_CONTENT
	"""
	
	MSG_UNKNOWN_OPERATION = "MSG_UNKNOWN_OPERATION"
	""" MSG_UNKNOWN_OPERATION
	"""
	
	MSG_UNKNOWN_TYPE = "MSG_UNKNOWN_TYPE"
	""" MSG_UNKNOWN_TYPE
	"""
	
	MSG_UPDATED = "MSG_UPDATED"
	""" MSG_UPDATED
	"""
	
	MSG_VERSION_AWARE = "MSG_VERSION_AWARE"
	""" MSG_VERSION_AWARE
	"""
	
	MSG_VERSION_AWARE_CONFLICT = "MSG_VERSION_AWARE_CONFLICT"
	""" MSG_VERSION_AWARE_CONFLICT
	"""
	
	MSG_VERSION_AWARE_URL = "MSG_VERSION_AWARE_URL"
	""" MSG_VERSION_AWARE_URL
	"""
	
	MSG_WRONG_NS = "MSG_WRONG_NS"
	""" MSG_WRONG_NS
	"""
	
	SEARCH_MULTIPLE = "SEARCH_MULTIPLE"
	""" SEARCH_MULTIPLE
	"""
	
	UPDATE_MULTIPLE_MATCHES = "UPDATE_MULTIPLE_MATCHES"
	""" UPDATE_MULTIPLE_MATCHES
	"""
	
	DELETE_MULTIPLE_MATCHES = "DELETE_MULTIPLE_MATCHES"
	""" DELETE_MULTIPLE_MATCHES
	"""
	
	SEARCH_NONE = "SEARCH_NONE"
	""" SEARCH_NONE
	"""



class OperationParameterUse(object):
	""" Whether an operation parameter is an input or an output parameter.

	URL: http://hl7.org/fhir/operation-parameter-use
	ValueSet: http://hl7.org/fhir/ValueSet/operation-parameter-use
	"""
	
	# in = "in"
	""" This is an input parameter.
	"""
	
	out = "out"
	""" This is an output parameter.
	"""



class ParticipantRequired(object):
	""" Is the Participant required to attend the appointment.

	URL: http://hl7.org/fhir/participantrequired
	ValueSet: http://hl7.org/fhir/ValueSet/participantrequired
	"""
	
	required = "required"
	""" The participant is required to attend the appointment.
	"""
	
	optional = "optional"
	""" The participant may optionally attend the appointment.
	"""
	
	informationOnly = "information-only"
	""" The participant is excluded from the appointment, and may not be informed of the appointment taking place.
	/// (Appointment is about them, not for them - such as 2 doctors discussing results about a patient's test).
	"""



class ParticipationStatus(object):
	""" The Participation status of an appointment.

	URL: http://hl7.org/fhir/participationstatus
	ValueSet: http://hl7.org/fhir/ValueSet/participationstatus
	"""
	
	accepted = "accepted"
	""" The participant has accepted the appointment.
	"""
	
	declined = "declined"
	""" The participant has declined the appointment and will not participate in the appointment.
	"""
	
	tentative = "tentative"
	""" The participant has  tentatively accepted the appointment. This could be automatically created by a system and
	/// requires further processing before it can be accepted. There is no commitment that attendance will occur.
	"""
	
	needsAction = "needs-action"
	""" The participant needs to indicate if they accept the appointment by changing this status to one of the other
	/// statuses.
	"""



class PayeeResourceType(object):
	""" The type of payee Resource

	URL: http://hl7.org/fhir/ex-payee-resource-type
	ValueSet: http://hl7.org/fhir/ValueSet/ex-payee-resource-type
	"""
	
	organization = "organization"
	""" Organization resource
	"""
	
	patient = "patient"
	""" Patient resource
	"""
	
	practitioner = "practitioner"
	""" Practitioner resource
	"""
	
	relatedperson = "relatedperson"
	""" RelatedPerson resource
	"""



class PlanActionCardinalityBehavior(object):
	""" Defines behavior for an action or a group for how many times that item may be repeated

	URL: http://hl7.org/fhir/action-cardinality-behavior
	ValueSet: http://hl7.org/fhir/ValueSet/action-cardinality-behavior
	"""
	
	single = "single"
	""" The action may only be selected one time
	"""
	
	multiple = "multiple"
	""" The action may be selected multiple times
	"""



class PlanActionConditionKind(object):
	""" Defines the kinds of conditions that can appear on actions

	URL: http://hl7.org/fhir/action-condition-kind
	ValueSet: http://hl7.org/fhir/ValueSet/action-condition-kind
	"""
	
	applicability = "applicability"
	""" The condition describes whether or not a given action is applicable
	"""
	
	start = "start"
	""" The condition is a starting condition for the action
	"""
	
	stop = "stop"
	""" The condition is a stop, or exit condition for the action
	"""



class PlanActionGroupingBehavior(object):
	""" Defines organization behavior of a group

	URL: http://hl7.org/fhir/action-grouping-behavior
	ValueSet: http://hl7.org/fhir/ValueSet/action-grouping-behavior
	"""
	
	visualGroup = "visual-group"
	""" Any group marked with this behavior should be displayed as a visual group to the end user
	"""
	
	logicalGroup = "logical-group"
	""" A group with this behavior logically groups its sub-elements, and may be shown as a visual group to the end
	/// user, but it is not required to do so
	"""
	
	sentenceGroup = "sentence-group"
	""" A group of related alternative actions is a sentence group if the target referenced by the action is the same in
	/// all the actions and each action simply constitutes a different variation on how to specify the details for the
	/// target. For example, two actions that could be in a SentenceGroup are "aspirin, 500 mg, 2 times per day" and
	/// "aspirin, 300 mg, 3 times per day". In both cases, aspirin is the target referenced by the action, and the two
	/// actions represent different options for how aspirin might be ordered for the patient. Note that a SentenceGroup
	/// would almost always have an associated selection behavior of "AtMostOne", unless it's a required action, in
	/// which case, it would be "ExactlyOne"
	"""



class PlanActionParticipantType(object):
	""" The type of participant for the action

	URL: http://hl7.org/fhir/action-participant-type
	ValueSet: http://hl7.org/fhir/ValueSet/action-participant-type
	"""
	
	patient = "patient"
	""" The participant is the patient under evaluation
	"""
	
	practitioner = "practitioner"
	""" The participant is a practitioner involved in the patient's care
	"""
	
	relatedPerson = "related-person"
	""" The participant is a person related to the patient
	"""



class PlanActionPrecheckBehavior(object):
	""" Defines selection frequency behavior for an action or group

	URL: http://hl7.org/fhir/action-precheck-behavior
	ValueSet: http://hl7.org/fhir/ValueSet/action-precheck-behavior
	"""
	
	yes = "yes"
	""" An action with this behavior is one of the most frequent action that is, or should be, included by an end user,
	/// for the particular context in which the action occurs. The system displaying the action to the end user should
	/// consider "pre-checking" such an action as a convenience for the user
	"""
	
	no = "no"
	""" An action with this behavior is one of the less frequent actions included by the end user, for the particular
	/// context in which the action occurs. The system displaying the actions to the end user would typically not "pre-
	/// check" such an action
	"""



class PlanActionRelationshipType(object):
	""" Defines the types of relationships between actions

	URL: http://hl7.org/fhir/action-relationship-type
	ValueSet: http://hl7.org/fhir/ValueSet/action-relationship-type
	"""
	
	beforeStart = "before-start"
	""" The action must be performed before the start of the related action
	"""
	
	before = "before"
	""" The action must be performed before the related action
	"""
	
	beforeEnd = "before-end"
	""" The action must be performed before the end of the related action
	"""
	
	concurrentWithStart = "concurrent-with-start"
	""" The action must be performed concurrent with the start of the related action
	"""
	
	concurrent = "concurrent"
	""" The action must be performed concurrent with the related action
	"""
	
	concurrentWithEnd = "concurrent-with-end"
	""" The action must be performed concurrent with the end of the related action
	"""
	
	afterStart = "after-start"
	""" The action must be performed after the start of the related action
	"""
	
	after = "after"
	""" The action must be performed after the related action
	"""
	
	afterEnd = "after-end"
	""" The action must be performed after the end of the related action
	"""



class PlanActionRequiredBehavior(object):
	""" Defines requiredness behavior for selecting an action or an action group

	URL: http://hl7.org/fhir/action-required-behavior
	ValueSet: http://hl7.org/fhir/ValueSet/action-required-behavior
	"""
	
	must = "must"
	""" An action with this behavior must be included in the actions processed by the end user; the end user may not
	/// choose not to include this action
	"""
	
	could = "could"
	""" An action with this behavior may be included in the set of actions processed by the end user
	"""
	
	mustUnlessDocumented = "must-unless-documented"
	""" An action with this behavior must be included in the set of actions processed by the end user, unless the end
	/// user provides documentation as to why the action was not included
	"""



class PlanActionSelectionBehavior(object):
	""" Defines selection behavior of a group

	URL: http://hl7.org/fhir/action-selection-behavior
	ValueSet: http://hl7.org/fhir/ValueSet/action-selection-behavior
	"""
	
	any = "any"
	""" Any number of the actions in the group may be chosen, from zero to all
	"""
	
	all = "all"
	""" All the actions in the group must be selected as a single unit
	"""
	
	allOrNone = "all-or-none"
	""" All the actions in the group are meant to be chosen as a single unit: either all must be selected by the end
	/// user, or none may be selected
	"""
	
	exactlyOne = "exactly-one"
	""" The end user must choose one and only one of the selectable actions in the group. The user may not choose none
	/// of the actions in the group
	"""
	
	atMostOne = "at-most-one"
	""" The end user may choose zero or at most one of the actions in the group
	"""
	
	oneOrMore = "one-or-more"
	""" The end user must choose a minimum of one, and as many additional as desired
	"""



class PlanActionType(object):
	""" The type of action to be performed

	URL: http://hl7.org/fhir/action-type
	ValueSet: http://hl7.org/fhir/ValueSet/action-type
	"""
	
	create = "create"
	""" The action is to create a new resource
	"""
	
	update = "update"
	""" The action is to update an existing resource
	"""
	
	remove = "remove"
	""" The action is to remove an existing resource
	"""
	
	fireEvent = "fire-event"
	""" The action is to fire a specific event
	"""



class PlanDefinitionType(object):
	""" The type of PlanDefinition

	URL: http://hl7.org/fhir/plan-definition-type
	ValueSet: http://hl7.org/fhir/ValueSet/plan-definition-type
	"""
	
	orderSet = "order-set"
	""" A pre-defined and approved group of orders related to a particular clinical condition (e.g. hypertension
	/// treatment and monitoring) or stage of care (e.g. hospital admission to Coronary Care Unit). An order set is used
	/// as a checklist for the clinician when managing a patient with a specific condition. It is a structured
	/// collection of orders relevant to that condition and presented to the clinician in a computerized provider order
	/// entry (CPOE) system
	"""
	
	protocol = "protocol"
	""" A set of activities that can be peformed that have relationships in terms of order, pre-conditions etc
	"""
	
	ecaRule = "eca-rule"
	""" A decision support rule of the form [on Event] if Condition then Action. It is intended to be a shareable,
	/// computable definition of a actions that should be taken whenever some condition is met in response to a
	/// particular event or events
	"""



class ProcedureRelationshipType(object):
	""" The nature of the relationship with this procedure.

	URL: http://hl7.org/fhir/procedure-relationship-type
	ValueSet: http://hl7.org/fhir/ValueSet/procedure-relationship-type
	"""
	
	causedBy = "caused-by"
	""" This procedure had to be performed because of the related one.
	"""
	
	becauseOf = "because-of"
	""" This procedure caused the related one to be performed.
	"""



class ProcedureRequestPriority(object):
	""" The priority of the request.

	URL: http://hl7.org/fhir/procedure-request-priority
	ValueSet: http://hl7.org/fhir/ValueSet/procedure-request-priority
	"""
	
	routine = "routine"
	""" The request has a normal priority.
	"""
	
	urgent = "urgent"
	""" The request should be done urgently.
	"""
	
	stat = "stat"
	""" The request is time-critical.
	"""
	
	asap = "asap"
	""" The request should be acted on as soon as possible.
	"""



class ProcedureRequestStatus(object):
	""" The status of the request.

	URL: http://hl7.org/fhir/procedure-request-status
	ValueSet: http://hl7.org/fhir/ValueSet/procedure-request-status
	"""
	
	proposed = "proposed"
	""" The request has been proposed.
	"""
	
	draft = "draft"
	""" The request is in preliminary form, prior to being requested.
	"""
	
	requested = "requested"
	""" The request has been placed.
	"""
	
	received = "received"
	""" The receiving system has received the request but not yet decided whether it will be performed.
	"""
	
	accepted = "accepted"
	""" The receiving system has accepted the request, but work has not yet commenced.
	"""
	
	inProgress = "in-progress"
	""" The work to fulfill the request is happening.
	"""
	
	completed = "completed"
	""" The work has been completed, the report(s) released, and no further work is planned.
	"""
	
	suspended = "suspended"
	""" The request has been held by originating system/user request.
	"""
	
	rejected = "rejected"
	""" The receiving system has declined to fulfill the request.
	"""
	
	aborted = "aborted"
	""" The request was attempted, but due to some procedural error, it could not be completed.
	"""



class ProcedureStatus(object):
	""" A code specifying the state of the procedure.

	URL: http://hl7.org/fhir/procedure-status
	ValueSet: http://hl7.org/fhir/ValueSet/procedure-status
	"""
	
	inProgress = "in-progress"
	""" The procedure is still occurring.
	"""
	
	aborted = "aborted"
	""" The procedure was terminated without completing successfully.
	"""
	
	completed = "completed"
	""" All actions involved in the procedure have taken place.
	"""
	
	enteredInError = "entered-in-error"
	""" The statement was entered in error and Is not valid.
	"""
	
	unknown = "unknown"
	""" The authoring system doesn't know the current state of the procedure.
	"""



class PropertyRepresentation(object):
	""" How a property is represented on the wire.

	URL: http://hl7.org/fhir/property-representation
	ValueSet: http://hl7.org/fhir/ValueSet/property-representation
	"""
	
	xmlAttr = "xmlAttr"
	""" In XML, this property is represented as an attribute not an element.
	"""
	
	xmlText = "xmlText"
	""" This element is represented using the XML text attribute (primitives only)
	"""
	
	typeAttr = "typeAttr"
	""" The type of this element is indicated using xsi:type
	"""
	
	cdaText = "cdaText"
	""" Use CDA narrative instead of XHTML
	"""
	
	xhtml = "xhtml"
	""" The property is represented using XHTML
	"""



class PropertyType(object):
	""" The type of a property value

	URL: http://hl7.org/fhir/concept-property-type
	ValueSet: http://hl7.org/fhir/ValueSet/concept-property-type
	"""
	
	code = "code"
	""" The property value is a code that identifies a concept defined in the code system
	"""
	
	coding = "Coding"
	""" The property  value is a code defined in an external code system. This may be used for translations, but is not
	/// the intent
	"""
	
	string = "string"
	""" The property value is a string
	"""
	
	integer = "integer"
	""" The property value is a string (often used to assign ranking values to concepts for supporting score
	/// assessments)
	"""
	
	boolean = "boolean"
	""" The property value is a boolean true | false
	"""
	
	dateTime = "dateTime"
	""" The property is a date or a date + time
	"""



class ProvenanceEntityRole(object):
	""" How an entity was used in an activity.

	URL: http://hl7.org/fhir/provenance-entity-role
	ValueSet: http://hl7.org/fhir/ValueSet/provenance-entity-role
	"""
	
	derivation = "derivation"
	""" A transformation of an entity into another, an update of an entity resulting in a new one, or the construction
	/// of a new entity based on a preexisting entity.
	"""
	
	revision = "revision"
	""" A derivation for which the resulting entity is a revised version of some original.
	"""
	
	quotation = "quotation"
	""" The repeat of (some or all of) an entity, such as text or image, by someone who may or may not be its original
	/// author.
	"""
	
	source = "source"
	""" A primary source for a topic refers to something produced by some agent with direct experience and knowledge
	/// about the topic, at the time of the topic's study, without benefit from hindsight.
	"""
	
	removal = "removal"
	""" A derivation for which the entity is removed from accessibility usually through the use of the Delete operation.
	"""



class PublicationStatus(object):
	""" The lifecycle status of a Value Set or Concept Map.

	URL: http://hl7.org/fhir/publication-status
	ValueSet: http://hl7.org/fhir/ValueSet/publication-status
	"""
	
	draft = "draft"
	""" This resource is still under development.
	"""
	
	active = "active"
	""" This resource is ready for normal use.
	"""
	
	retired = "retired"
	""" This resource has been withdrawn or superseded and should no longer be used.
	"""



class QualityOfEvidenceRating(object):
	""" A rating system that describes the quality of evidence such as the GRADE, DynaMed, or Oxford CEBM systems

	URL: http://hl7.org/fhir/evidence-quality
	ValueSet: http://hl7.org/fhir/ValueSet/cqif-evidence-quality
	"""
	
	high = "high"
	""" High quality evidence
	"""
	
	moderate = "moderate"
	""" Moderate quality evidence
	"""
	
	low = "low"
	""" Low quality evidence
	"""
	
	veryLow = "very-low"
	""" Very low quality evidence
	"""



class QualityType(object):
	""" Type for quality report

	URL: http://hl7.org/fhir/quality-type
	ValueSet: http://hl7.org/fhir/ValueSet/quality-type
	"""
	
	INDEL = "INDEL"
	""" INDEL Comparison
	"""
	
	SNP = "SNP"
	""" SNP Comparison
	"""
	
	UNKNOWN = "UNKNOWN"
	""" UNKNOWN Comparison
	"""



class QuantityComparator(object):
	""" How the Quantity should be understood and represented.

	URL: http://hl7.org/fhir/quantity-comparator
	ValueSet: http://hl7.org/fhir/ValueSet/quantity-comparator
	"""
	
	lt = "<"
	""" The actual value is less than the given value.
	"""
	
	lte = "<="
	""" The actual value is less than or equal to the given value.
	"""
	
	gte = ">="
	""" The actual value is greater than or equal to the given value.
	"""
	
	gt = ">"
	""" The actual value is greater than the given value.
	"""



class QuestionnaireItemType(object):
	""" Distinguishes groups from questions and display text and indicates data type for questions

	URL: http://hl7.org/fhir/item-type
	ValueSet: http://hl7.org/fhir/ValueSet/item-type
	"""
	
	group = "group"
	""" An item with no direct answer but which has descendant items that are questions
	"""
	
	display = "display"
	""" Text for display that will not capture an answer or have descendants
	"""
	
	question = "question"
	""" An item that defines a specific answer to be captured (and may have descendant items)
	"""
	
	boolean = "boolean"
	""" Question with a yes/no answer
	"""
	
	decimal = "decimal"
	""" Question with is a real number answer
	"""
	
	integer = "integer"
	""" Question with an integer answer
	"""
	
	date = "date"
	""" Question with adate answer
	"""
	
	dateTime = "dateTime"
	""" Question with a date and time answer
	"""
	
	instant = "instant"
	""" Question with a system timestamp answer
	"""
	
	time = "time"
	""" Question with a time (hour/minute/second) answer independent of date.
	"""
	
	string = "string"
	""" Question with a short (few words to short sentence) free-text entry answer
	"""
	
	text = "text"
	""" Question with a long (potentially multi-paragraph) free-text entry (still captured as a string) answer
	"""
	
	url = "url"
	""" Question with a url (website, FTP site, etc.) answer
	"""
	
	choice = "choice"
	""" Question with a Coding drawn from a list of options as an answer
	"""
	
	openChoice = "open-choice"
	""" Answer is a Coding drawn from a list of options or a free-text entry captured as Coding.display
	"""
	
	attachment = "attachment"
	""" Question with binary content such as a image, PDF, etc. as an answer
	"""
	
	reference = "reference"
	""" Question with a reference to another resource (practitioner, organization, etc.) as an answer
	"""
	
	quantity = "quantity"
	""" Question with a combination of a numeric value and unit, potentially with a comparator (<, >, etc.) as an
	/// answer.
	"""



class QuestionnaireItemUsageMode(object):
	""" Identifies the modes of usage of a questionnaire that should enable a particular questionnaire item

	URL: http://hl7.org/fhir/questionnaire-usage-mode
	ValueSet: http://hl7.org/fhir/ValueSet/questionnaire-usage-mode
	"""
	
	captureDisplay = "capture-display"
	""" Render the item regardless of usage mode
	"""
	
	capture = "capture"
	""" Render the item only when capturing data
	"""
	
	display = "display"
	""" Render the item only when displaying a completed form
	"""
	
	displayNonEmpty = "display-non-empty"
	""" Render the item only when displaying a completed form and the item has been answered (or has child items that
	/// have been answered)
	"""
	
	captureDisplayNonEmpty = "capture-display-non-empty"
	""" Render the item when capturing data or when displaying a completed form and the item has been answered (or has
	/// child items that have been answered)
	"""



class QuestionnaireResponseStatus(object):
	""" Lifecycle status of the questionnaire response.

	URL: http://hl7.org/fhir/questionnaire-answers-status
	ValueSet: http://hl7.org/fhir/ValueSet/questionnaire-answers-status
	"""
	
	inProgress = "in-progress"
	""" This QuestionnaireResponse has been partially filled out with answers, but changes or additions are still
	/// expected to be made to it.
	"""
	
	completed = "completed"
	""" This QuestionnaireResponse has been filled out with answers, and the current content is regarded as definitive.
	"""
	
	amended = "amended"
	""" This QuestionnaireResponse has been filled out with answers, then marked as complete, yet changes or additions
	/// have been made to it afterwards.
	"""
	
	enteredInError = "entered-in-error"
	""" This QuestionnaireResponse was entered in error and voided.
	"""



class QuestionnaireStatus(object):
	""" Lifecycle status of the questionnaire.

	URL: http://hl7.org/fhir/questionnaire-status
	ValueSet: http://hl7.org/fhir/ValueSet/questionnaire-status
	"""
	
	draft = "draft"
	""" This Questionnaire is not ready for official use.
	"""
	
	published = "published"
	""" This Questionnaire is ready for use.
	"""
	
	retired = "retired"
	""" This Questionnaire should no longer be used to gather data.
	"""



class ReferenceHandlingPolicy(object):
	""" A set of flags that defines how references are supported

	URL: http://hl7.org/fhir/reference-handling-policy
	ValueSet: http://hl7.org/fhir/ValueSet/reference-handling-policy
	"""
	
	literal = "literal"
	""" The server supports and populates Literal references where they are known (this code does not guarantee that all
	/// references are literal; see 'enforced')
	"""
	
	logical = "logical"
	""" The server allows logical references
	"""
	
	resolves = "resolves"
	""" The server will attempt to resolve logical references to literal references (if resolution fails, the server may
	/// still accept resources; see logical)
	"""
	
	enforced = "enforced"
	""" The server enforces that references have integrity - e.g. it ensures that references can always be resolved.
	/// This is typically the case for clinical record systems, but often no the case for middleware/proxy systems
	"""
	
	local = "local"
	""" The server does not support references that point to other servers
	"""



class ReferenceVersionRules(object):
	""" Whether a reference needs to be version specific or version independent, or whetehr either can be used

	URL: http://hl7.org/fhir/reference-version-rules
	ValueSet: http://hl7.org/fhir/ValueSet/reference-version-rules
	"""
	
	either = "either"
	""" The reference may be either version independent or version specific
	"""
	
	independent = "independent"
	""" The reference must be version independent
	"""
	
	specific = "specific"
	""" The reference must be version specific
	"""



class ReferralCategory(object):
	""" Identifies the degree of intention/authorization associated with the request

	URL: http://hl7.org/fhir/referralcategory
	ValueSet: http://hl7.org/fhir/ValueSet/referralcategory
	"""
	
	proposal = "proposal"
	""" The referral request represents a suggestion or recommendation that a referral be made.
	"""
	
	plan = "plan"
	""" The referral request represents an intention by the author to make a referral, but no actual referral has yet
	/// been made/authorized.
	"""
	
	request = "request"
	""" This is an actual referral request which, when active, will have the authorizations needed to allow it to be
	/// actioned.
	"""



class ReferralMethod(object):
	""" The methods of referral can be used when referring to a specific HealthCareService resource.

	URL: http://hl7.org/fhir/service-referral-method
	ValueSet: http://hl7.org/fhir/ValueSet/service-referral-method
	"""
	
	fax = "fax"
	""" Referrals may be accepted by fax.
	"""
	
	phone = "phone"
	""" Referrals may be accepted over the phone from a practitioner.
	"""
	
	elec = "elec"
	""" Referrals may be accepted via a secure messaging system. To determine the types of secure messaging systems
	/// supported, refer to the identifiers collection. Callers will need to understand the specific identifier system
	/// used to know that they are able to transmit messages.
	"""
	
	semail = "semail"
	""" Referrals may be accepted via a secure email. To send please enrypt with the services public key.
	"""
	
	mail = "mail"
	""" Referrals may be accepted via regular postage (or hand delivered).
	"""



class ReferralStatus(object):
	""" The status of the referral.

	URL: http://hl7.org/fhir/referralstatus
	ValueSet: http://hl7.org/fhir/ValueSet/referralstatus
	"""
	
	draft = "draft"
	""" A draft referral that has yet to be send.
	"""
	
	active = "active"
	""" The referral is complete and is ready for fulfillment.
	"""
	
	cancelled = "cancelled"
	""" The referral has been cancelled without being completed. For example it is no longer needed.
	"""
	
	completed = "completed"
	""" The referral has been completely actioned.
	"""
	
	enteredInError = "entered-in-error"
	""" This referral record should never have existed, though it's possible some degree of real-world activity or
	/// decisions may have been taken due to its existence
	"""



class RelatedArtifactType(object):
	""" The type of relationship to the related artifact

	URL: http://hl7.org/fhir/related-artifact-type
	ValueSet: http://hl7.org/fhir/ValueSet/related-artifact-type
	"""
	
	documentation = "documentation"
	""" Additional documentation for the knowledge resource. This would include additional instructions on usage as well
	/// as additional information on clinical context or appropriateness
	"""
	
	justification = "justification"
	""" A summary of the justification for the knowledge resource including supporting evidence, relevant guidelines, or
	/// other clinically important information. This information is intended to provide a way to make the justification
	/// for the knowledge resource available to the consumer of interventions or results produced by the knowledge
	/// resource
	"""
	
	citation = "citation"
	""" Bibliographic citation for papers, references, or other relevant material for the knowledge resource. This is
	/// intended to allow for citation of related material, but that was not necessarily specifically prepared in
	/// connection with this knowledge resource
	"""
	
	predecessor = "predecessor"
	""" The previous version of the knowledge resource
	"""
	
	successor = "successor"
	""" The next version of the knowledge resource
	"""
	
	derivedFrom = "derived-from"
	""" The knowledge resource is derived from the related artifact. This is intended to capture the relationship in
	/// which a particular knowledge resource is based on the content of another artifact, but is modified to capture
	/// either a different set of overall requirements, or a more specific set of requirements such as those involved in
	/// a particular institution or clinical setting
	"""
	
	dependsOn = "depends-on"
	""" The knowledge resource depends on the given related artifact
	"""
	
	composedOf = "composed-of"
	""" The knowledge resource is composed of the given related artifact
	"""



class RepositoryType(object):
	""" Type for access of external uri

	URL: http://hl7.org/fhir/repository-type
	ValueSet: http://hl7.org/fhir/ValueSet/repository-type
	"""
	
	directlink = "directlink"
	""" When url is clicked, the resource can be seen directly (by webpage or by download link format)
	"""
	
	openapi = "openapi"
	""" When the api method (e.g. [base_url]/[parameter]) related with the url website is executed, the resource can be
	/// seen directly (usually in json or xml format)
	"""
	
	login = "login"
	""" When logged into the website, the resource can be seen.
	"""
	
	oauth = "oauth"
	""" When logged in and follow the API in the website related with url, the resource can be seen.
	"""
	
	other = "other"
	""" Some other complicated or particular way to get resource from url.
	"""



class RequestIntent(object):
	""" Codes indicating the degree of authority/intentionality associated with a request

	URL: http://hl7.org/fhir/request-intent
	ValueSet: http://hl7.org/fhir/ValueSet/request-intent
	"""
	
	proposal = "proposal"
	""" The request is a suggestion made by someone/something that doesn't have an intention to ensure it occurs and
	/// without providing an authorization to act
	"""
	
	plan = "plan"
	""" The request represents an intension to ensure something occurs without providing an authorization for others to
	/// act
	"""
	
	order = "order"
	""" The request represents a request/demand and authorization for action
	"""
	
	originalOrder = "original-order"
	""" The request represents an original authorization for action
	"""
	
	reflexOrder = "reflex-order"
	""" The request represents an automatically generated supplemental authorization for action based on a parent
	/// authorization together with initial results of the action taken against that parent authorization
	"""
	
	fillerOrder = "filler-order"
	""" The request represents the view of an authorization instantiated by a fulfilling system representing the details
	/// of the fulfiller's intention to act upon a submitted order
	"""
	
	instanceOrder = "instance-order"
	""" An order created in fulfillment of a broader order that represents the authorization for a single activity
	/// occurrence.  E.g. The administration of a single dose of a drug.
	"""
	
	option = "option"
	""" The request represents a component or option for a RequestGroup that establishes timing, conditionality and/or
	/// other constraints among a set of requests.
	/// 
	/// Refer to [[[RequestGroup]]] for additional information on how this status is used
	"""



class RequestPriority(object):
	""" The clinical priority of an order.

	URL: http://hl7.org/fhir/request-priority
	ValueSet: http://hl7.org/fhir/ValueSet/request-priority
	"""
	
	routine = "routine"
	""" The order has a normal priority .
	"""
	
	urgent = "urgent"
	""" The order should be urgently.
	"""
	
	stat = "stat"
	""" The order is time-critical.
	"""
	
	asap = "asap"
	""" The order should be acted on as soon as possible.
	"""



class RequestStage(object):
	""" The kind of request.

	URL: http://hl7.org/fhir/request-stage
	ValueSet: http://hl7.org/fhir/ValueSet/request-stage
	"""
	
	proposal = "proposal"
	""" The request is a proposal
	"""
	
	plan = "plan"
	""" The request is a plan
	"""
	
	originalOrder = "original-order"
	""" The request is an order.
	"""
	
	encoded = "encoded"
	""" Represents an order created by a fulfiller as a representation of the specific action(s) they intend to take to
	/// fulfill the original order.  Typically these orders are more fully encoded than the original placer order.
	"""
	
	reflexOrder = "reflex-order"
	""" Represents a separate order created by a fulfiller as result of fulfilment of an order.
	"""



class RequestStatus(object):
	""" Codes identifying the stage lifecycle stage of a request

	URL: http://hl7.org/fhir/request-status
	ValueSet: http://hl7.org/fhir/ValueSet/request-status
	"""
	
	draft = "draft"
	""" The request has been created but is not yet complete or ready for action
	"""
	
	active = "active"
	""" The request is ready to be acted upon
	"""
	
	suspended = "suspended"
	""" The authorization/request to act has been temporarily withdrawn but is expected to resume in the future
	"""
	
	cancelled = "cancelled"
	""" The authorization/request to act has been terminated prior to the full completion of the intended actions.  No
	/// further activity should occur.
	"""
	
	completed = "completed"
	""" Activity against the request has been sufficiently completed to the satisfaction of the requester
	"""
	
	enteredInError = "entered-in-error"
	""" This electronic record should never have existed, though it is possible that real-world decisions were based on
	/// it.  (If real-world activity has occurred, the status should be "cancelled" rather than "entered-in-error".)
	"""
	
	unknown = "unknown"
	""" The authoring system does not know which of the status values currently applies for this request
	"""



class ResearchStudyStatus(object):
	""" Codes that convey the current status of the research study

	URL: http://hl7.org/fhir/research-study-status
	ValueSet: http://hl7.org/fhir/ValueSet/research-study-status
	"""
	
	draft = "draft"
	""" The study is undergoing design but the process of selecting study subjects and capturing data has not yet begun.
	"""
	
	inProgress = "in-progress"
	""" The study is currently being executed
	"""
	
	suspended = "suspended"
	""" Execution of the study has been temporarily paused
	"""
	
	stopped = "stopped"
	""" The study was terminated prior to the final determination of results
	"""
	
	completed = "completed"
	""" The information sought by the study has been gathered and compiled and no further work is being performed
	"""
	
	enteredInError = "entered-in-error"
	""" This study never actually existed.  The record is retained for tracking purposes in the event decisions may have
	/// been made based on this erroneous information.
	"""



class ResearchSubjectStatus(object):
	""" Indicates the progression of a study subject through a study

	URL: http://hl7.org/fhir/research-subject-status
	ValueSet: http://hl7.org/fhir/ValueSet/research-subject-status
	"""
	
	candidate = "candidate"
	""" The subject has been identified as a potential participant in the study but has not yet agreed to participate
	"""
	
	enrolled = "enrolled"
	""" The subject has agreed to participate in the study but has not yet begun performing any action within the study
	"""
	
	active = "active"
	""" The subject is currently being monitored and/or subject to treatment as part of the study
	"""
	
	suspended = "suspended"
	""" The subject has temporarily discontinued monitoring/treatment as part of the study
	"""
	
	withdrawn = "withdrawn"
	""" The subject has permanently ended participation in the study prior to completion of the intended
	/// monitoring/treatment
	"""
	
	completed = "completed"
	""" All intended monitoring/treatment of the subject has been completed and their engagement with the study is now
	/// ended
	"""



class ResourceTypeLink(object):
	""" The type of payee Resource

	URL: http://hl7.org/fhir/resource-type-link
	ValueSet: http://hl7.org/fhir/ValueSet/resource-type-link
	"""
	
	organization = "organization"
	""" Organization resource
	"""
	
	patient = "patient"
	""" Patient resource
	"""
	
	practitioner = "practitioner"
	""" Practitioner resource
	"""
	
	relatedperson = "relatedperson"
	""" RelatedPerson resource
	"""



class ResourceValidationMode(object):
	""" Codes indicating the type of validation to perform

	URL: http://hl7.org/fhir/resource-validation-mode
	ValueSet: http://hl7.org/fhir/ValueSet/resource-validation-mode
	"""
	
	create = "create"
	""" The server checks the content, and then checks that the content would be acceptable as a create (e.g. that the
	/// content would not violate any uniqueness constraints).
	"""
	
	update = "update"
	""" The server checks the content, and then checks that it would accept it as an update against the nominated
	/// specific resource (e.g. that there are no changes to immutable fields the server does not allow to change, and
	/// checking version integrity if appropriate).
	"""
	
	delete = "delete"
	""" The server ignores the content, and checks that the nominated resource is allowed to be deleted (e.g. checking
	/// referential integrity rules).
	"""



class ResourceVersionPolicy(object):
	""" How the system supports versioning for a resource.

	URL: http://hl7.org/fhir/versioning-policy
	ValueSet: http://hl7.org/fhir/ValueSet/versioning-policy
	"""
	
	noVersion = "no-version"
	""" VersionId meta-property is not supported (server) or used (client).
	"""
	
	versioned = "versioned"
	""" VersionId meta-property is supported (server) or used (client).
	"""
	
	versionedUpdate = "versioned-update"
	""" VersionId is must be correct for updates (server) or will be specified (If-match header) for updates (client).
	"""



class ResponseType(object):
	""" The kind of response to a message

	URL: http://hl7.org/fhir/response-code
	ValueSet: http://hl7.org/fhir/ValueSet/response-code
	"""
	
	ok = "ok"
	""" The message was accepted and processed without error.
	"""
	
	transientError = "transient-error"
	""" Some internal unexpected error occurred - wait and try again. Note - this is usually used for things like
	/// database unavailable, which may be expected to resolve, though human intervention may be required.
	"""
	
	fatalError = "fatal-error"
	""" The message was rejected because of some content in it. There is no point in re-sending without change. The
	/// response narrative SHALL describe the issue.
	"""



class RestfulCapabilityMode(object):
	""" The mode of a RESTful capability statement.

	URL: http://hl7.org/fhir/restful-capability-mode
	ValueSet: http://hl7.org/fhir/ValueSet/restful-capability-mode
	"""
	
	client = "client"
	""" The application acts as a client for this resource.
	"""
	
	server = "server"
	""" The application acts as a server for this resource.
	"""



class RestfulSecurityService(object):
	""" Types of security services used with FHIR.

	URL: http://hl7.org/fhir/restful-security-service
	ValueSet: http://hl7.org/fhir/ValueSet/restful-security-service
	"""
	
	oAuth = "OAuth"
	""" Oauth (unspecified version see oauth.net).
	"""
	
	sMARTOnFHIR = "SMART-on-FHIR"
	""" OAuth2 using SMART-on-FHIR profile (see http://docs.smarthealthit.org/).
	"""
	
	NTLM = "NTLM"
	""" Microsoft NTLM Authentication.
	"""
	
	basic = "Basic"
	""" Basic authentication defined in HTTP specification.
	"""
	
	kerberos = "Kerberos"
	""" see http://www.ietf.org/rfc/rfc4120.txt.
	"""
	
	certificates = "Certificates"
	""" SSL where client must have a certificate registered with the server.
	"""



class SearchComparator(object):
	""" What Search Comparator Codes are supported in search

	URL: http://hl7.org/fhir/search-comparator
	ValueSet: http://hl7.org/fhir/ValueSet/search-comparator
	"""
	
	eq = "eq"
	""" the value for the parameter in the resource is equal to the provided value
	"""
	
	ne = "ne"
	""" the value for the parameter in the resource is not equal to the provided value
	"""
	
	gt = "gt"
	""" the value for the parameter in the resource is greater than the provided value
	"""
	
	lt = "lt"
	""" the value for the parameter in the resource is less than the provided value
	"""
	
	ge = "ge"
	""" the value for the parameter in the resource is greater or equal to the provided value
	"""
	
	le = "le"
	""" the value for the parameter in the resource is less or equal to the provided value
	"""
	
	sa = "sa"
	""" the value for the parameter in the resource starts after the provided value
	"""
	
	eb = "eb"
	""" the value for the parameter in the resource ends before the provided value
	"""
	
	ap = "ap"
	""" the value for the parameter in the resource is approximately the same to the provided value.
	"""



class SearchEntryMode(object):
	""" Why an entry is in the result set - whether it's included as a match or because of an _include requirement.

	URL: http://hl7.org/fhir/search-entry-mode
	ValueSet: http://hl7.org/fhir/ValueSet/search-entry-mode
	"""
	
	match = "match"
	""" This resource matched the search specification.
	"""
	
	include = "include"
	""" This resource is returned because it is referred to from another resource in the search set.
	"""
	
	outcome = "outcome"
	""" An OperationOutcome that provides additional information about the processing of a search.
	"""



class SearchModifierCode(object):
	""" A supported modifier for a search parameter.

	URL: http://hl7.org/fhir/search-modifier-code
	ValueSet: http://hl7.org/fhir/ValueSet/search-modifier-code
	"""
	
	missing = "missing"
	""" The search parameter returns resources that have a value or not.
	"""
	
	exact = "exact"
	""" The search parameter returns resources that have a value that exactly matches the supplied parameter (the whole
	/// string, including casing and accents).
	"""
	
	contains = "contains"
	""" The search parameter returns resources that include the supplied parameter value anywhere within the field being
	/// searched.
	"""
	
	# not = "not"
	""" The search parameter returns resources that do not contain a match .
	"""
	
	text = "text"
	""" The search parameter is processed as a string that searches text associated with the code/value - either
	/// CodeableConcept.text, Coding.display, or Identifier.type.text.
	"""
	
	# in = "in"
	""" The search parameter is a URI (relative or absolute) that identifies a value set, and the search parameter tests
	/// whether the coding is in the specified value set.
	"""
	
	notIn = "not-in"
	""" The search parameter is a URI (relative or absolute) that identifies a value set, and the search parameter tests
	/// whether the coding is not in the specified value set.
	"""
	
	below = "below"
	""" The search parameter tests whether the value in a resource is subsumed by the specified value (is-a, or
	/// hierarchical relationships).
	"""
	
	above = "above"
	""" The search parameter tests whether the value in a resource subsumes the specified value (is-a, or hierarchical
	/// relationships).
	"""
	
	type = "type"
	""" The search parameter only applies to the Resource Type specified as a modifier (e.g. the modifier is not
	/// actually :type, but :Patient etc.).
	"""



class SearchParamType(object):
	""" Data types allowed to be used for search parameters.

	URL: http://hl7.org/fhir/search-param-type
	ValueSet: http://hl7.org/fhir/ValueSet/search-param-type
	"""
	
	number = "number"
	""" Search parameter SHALL be a number (a whole number, or a decimal).
	"""
	
	date = "date"
	""" Search parameter is on a date/time. The date format is the standard XML format, though other formats may be
	/// supported.
	"""
	
	string = "string"
	""" Search parameter is a simple string, like a name part. Search is case-insensitive and accent-insensitive. May
	/// match just the start of a string. String parameters may contain spaces.
	"""
	
	token = "token"
	""" Search parameter on a coded element or identifier. May be used to search through the text, displayname, code and
	/// code/codesystem (for codes) and label, system and key (for identifier). Its value is either a string or a pair
	/// of namespace and value, separated by a "|", depending on the modifier used.
	"""
	
	reference = "reference"
	""" A reference to another resource.
	"""
	
	composite = "composite"
	""" A composite search parameter that combines a search on two values together.
	"""
	
	quantity = "quantity"
	""" A search parameter that searches on a quantity.
	"""
	
	uri = "uri"
	""" A search parameter that searches on a URI (RFC 3986).
	"""



class SequenceStatus(object):
	""" Codes providing the status of the variant test result

	URL: http://hl7.org/fhir/variant-state
	ValueSet: http://hl7.org/fhir/ValueSet/variant-state
	"""
	
	positive = "positive"
	""" the variant is detected
	"""
	
	negative = "negative"
	""" no variant is detected
	"""
	
	absent = "absent"
	""" result of the variant is missing
	"""



class SequenceType(object):
	""" Type if a sequence -- DNA, RNA, or amino acid sequence

	URL: http://hl7.org/fhir/sequence-type
	ValueSet: http://hl7.org/fhir/ValueSet/sequence-type
	"""
	
	AA = "AA"
	""" Amino acid sequence
	"""
	
	DNA = "DNA"
	""" DNA Sequence
	"""
	
	RNA = "RNA"
	""" RNA Sequence
	"""



class ServiceProvisionConditions(object):
	""" The code(s) that detail the conditions under which the healthcare service is available/offered.

	URL: http://hl7.org/fhir/service-provision-conditions
	ValueSet: http://hl7.org/fhir/ValueSet/service-provision-conditions
	"""
	
	free = "free"
	""" This service is available for no patient cost.
	"""
	
	disc = "disc"
	""" There are discounts available on this service for qualifying patients.
	"""
	
	cost = "cost"
	""" Fees apply for this service.
	"""



class SlicingRules(object):
	""" How slices are interpreted when evaluating an instance.

	URL: http://hl7.org/fhir/resource-slicing-rules
	ValueSet: http://hl7.org/fhir/ValueSet/resource-slicing-rules
	"""
	
	closed = "closed"
	""" No additional content is allowed other than that described by the slices in this profile.
	"""
	
	open = "open"
	""" Additional content is allowed anywhere in the list.
	"""
	
	openAtEnd = "openAtEnd"
	""" Additional content is allowed, but only at the end of the list. Note that using this requires that the slices be
	/// ordered, which makes it hard to share uses. This should only be done where absolutely required.
	"""



class SlotStatus(object):
	""" The free/busy status of the slot.

	URL: http://hl7.org/fhir/slotstatus
	ValueSet: http://hl7.org/fhir/ValueSet/slotstatus
	"""
	
	busy = "busy"
	""" Indicates that the time interval is busy because one  or more events have been scheduled for that interval.
	"""
	
	free = "free"
	""" Indicates that the time interval is free for scheduling.
	"""
	
	busyUnavailable = "busy-unavailable"
	""" Indicates that the time interval is busy and that the interval can not be scheduled.
	"""
	
	busyTentative = "busy-tentative"
	""" Indicates that the time interval is busy because one or more events have been tentatively scheduled for that
	/// interval.
	"""
	
	enteredInError = "entered-in-error"
	""" This instance should not have been part of this patient's medical record.
	"""



class SpecialValues(object):
	""" A set of generally useful codes defined so they can be included in value sets.

	URL: http://hl7.org/fhir/special-values
	ValueSet: http://hl7.org/fhir/ValueSet/special-values
	"""
	
	true = "true"
	""" Boolean true.
	"""
	
	false = "false"
	""" Boolean false.
	"""
	
	trace = "trace"
	""" The content is greater than zero, but too small to be quantified.
	"""
	
	sufficient = "sufficient"
	""" The specific quantity is not known, but is known to be non-zero and is not specified because it makes up the
	/// bulk of the material.
	"""
	
	withdrawn = "withdrawn"
	""" The value is no longer available.
	"""
	
	nilKnown = "nil-known"
	""" The are no known applicable values in this context.
	"""



class SpecimenStatus(object):
	""" Codes providing the status/availability of a specimen.

	URL: http://hl7.org/fhir/specimen-status
	ValueSet: http://hl7.org/fhir/ValueSet/specimen-status
	"""
	
	available = "available"
	""" The physical specimen is present and in good condition.
	"""
	
	unavailable = "unavailable"
	""" There is no physical specimen because it is either lost, destroyed or consumed.
	"""
	
	unsatisfactory = "unsatisfactory"
	""" The specimen cannot be used because of a quality issue such as a broken container, contamination, or too old.
	"""
	
	enteredInError = "entered-in-error"
	""" The specimen was entered in error and therefore nullified.
	"""



class StrengthOfRecommendationRating(object):
	""" A rating system that describes the strength of the recommendation, such as the GRADE, DynaMed, or HGPS systems

	URL: http://hl7.org/fhir/recommendation-strength
	ValueSet: http://hl7.org/fhir/ValueSet/cqif-recommendation-strength
	"""
	
	strong = "strong"
	""" Strong recommendation
	"""
	
	weak = "weak"
	""" Weak recommendation
	"""



class StructureDefinitionKind(object):
	""" Defines the type of structure that a definition is describing.

	URL: http://hl7.org/fhir/structure-definition-kind
	ValueSet: http://hl7.org/fhir/ValueSet/structure-definition-kind
	"""
	
	primitiveType = "primitive-type"
	""" A data type, which is a primitive type that has a value and an extension. These can be used throughout Resource
	/// and extension definitions. Only tbe base specification can define primitive types.
	"""
	
	complexType = "complex-type"
	""" A data type - either a complex structure that defines a set of data elements. These can be used throughout
	/// Resource and extension definitions, and in logical models.
	"""
	
	resource = "resource"
	""" A resource defined by the FHIR specification.
	"""
	
	logical = "logical"
	""" A logical model - a conceptual package of data that will be mapped to resources for implementation.
	"""



class StructureMapContextType(object):
	""" How to interpret the context

	URL: http://hl7.org/fhir/map-context-type
	ValueSet: http://hl7.org/fhir/ValueSet/map-context-type
	"""
	
	type = "type"
	""" The context specifies a type
	"""
	
	variable = "variable"
	""" The context specifies a variable
	"""



class StructureMapInputMode(object):
	""" Mode for this instance of data

	URL: http://hl7.org/fhir/map-input-mode
	ValueSet: http://hl7.org/fhir/ValueSet/map-input-mode
	"""
	
	source = "source"
	""" Names an input instance used a source for mapping
	"""
	
	target = "target"
	""" Names an instance that is being populated
	"""



class StructureMapListMode(object):
	""" If field is a list, how to manage the list

	URL: http://hl7.org/fhir/map-list-mode
	ValueSet: http://hl7.org/fhir/ValueSet/map-list-mode
	"""
	
	first = "first"
	""" when the target list is being assembled, the items for this rule go first. If more that one rule defines a first
	/// item (for a given instance of mapping) then this is an error
	"""
	
	share = "share"
	""" the target instance is shared with the target instances generated by another rule (up to the first common n
	/// items, then create new ones)
	"""
	
	last = "last"
	""" when the target list is being assembled, the items for this rule go last. If more that one rule defines a last
	/// item (for a given instance of mapping) then this is an error
	"""



class StructureMapModelMode(object):
	""" How the referenced structure is used in this mapping

	URL: http://hl7.org/fhir/map-model-mode
	ValueSet: http://hl7.org/fhir/ValueSet/map-model-mode
	"""
	
	source = "source"
	""" This structure describes an instance passed to the mapping engine that is used a source of data
	"""
	
	queried = "queried"
	""" This structure describes an instance that the mapping engine may ask for that is used a source of data
	"""
	
	target = "target"
	""" This structure describes an instance passed to the mapping engine that is used a target of data
	"""
	
	produced = "produced"
	""" This structure describes an instance that the mapping engine may ask to create that is used a target of data
	"""



class StructureMapTransform(object):
	""" How data is copied / created

	URL: http://hl7.org/fhir/map-transform
	ValueSet: http://hl7.org/fhir/ValueSet/map-transform
	"""
	
	create = "create"
	""" create(type : string) - type is passed through to the application on the standard API, and must be known by it
	"""
	
	copy = "copy"
	""" copy(source)
	"""
	
	truncate = "truncate"
	""" truncate(source, length) - source must be stringy type
	"""
	
	escape = "escape"
	""" escape(source, fmt1, fmt2) - change source from one kind of escaping to another (plain, java, xml, json). note
	/// that this is for when the string itself is escaped
	"""
	
	cast = "cast"
	""" cast(source, type?) - case source from one type to another. target type can be left as implicit if there is one
	/// and only one target type known
	"""
	
	append = "append"
	""" append(source...) - source is element or string
	"""
	
	translate = "translate"
	""" translate(source, uri_of_map) - use the translate operation
	"""
	
	reference = "reference"
	""" reference(source : object) - return a string that references the provided tree properly
	"""
	
	dateOp = "dateOp"
	""" Perform a date operation. Parameters to be documented
	"""
	
	uuid = "uuid"
	""" Generate a random UUID (in lowercase). No Parameters
	"""
	
	pointer = "pointer"
	""" Return the appropriate string to put in a Reference that refers to the resource provided as a parameter
	"""
	
	evaluate = "evaluate"
	""" Execute the supplied fluentpath expression and use the value returned by that
	"""
	
	cc = "cc"
	""" Create a CodeableConcept. Parameters = (text) or (system. Code[, display])
	"""
	
	C = "c"
	""" Create a Coding. Parameters = (system. Code[, display])
	"""
	
	qty = "qty"
	""" Create a quantity. Parameters = (text) or (value, unit, [system, code]) where text =s the natural represenation
	/// e.g. [comparator]value[space]unit
	"""
	
	id = "id"
	""" Create an identifier. Parameters = (system, value[, type]) where type is a code from the identifier type value
	/// set
	"""
	
	cp = "cp"
	""" Create a contact details. Parameters = (value) or (system, value). If no system is provided, the system should
	/// be inferred from the content of the value
	"""



class SubscriptionChannelType(object):
	""" The type of method used to execute a subscription.

	URL: http://hl7.org/fhir/subscription-channel-type
	ValueSet: http://hl7.org/fhir/ValueSet/subscription-channel-type
	"""
	
	restHook = "rest-hook"
	""" The channel is executed by making a post to the URI. If a payload is included, the URL is interpreted as the
	/// service base, and an update (PUT) is made.
	"""
	
	websocket = "websocket"
	""" The channel is executed by sending a packet across a web socket connection maintained by the client. The URL
	/// identifies the websocket, and the client binds to this URL.
	"""
	
	email = "email"
	""" The channel is executed by sending an email to the email addressed in the URI (which must be a mailto:).
	"""
	
	sms = "sms"
	""" The channel is executed by sending an SMS message to the phone number identified in the URL (tel:).
	"""
	
	message = "message"
	""" The channel is executed by sending a message (e.g. a Bundle with a MessageHeader resource etc.) to the
	/// application identified in the URI.
	"""



class SubscriptionStatus(object):
	""" The status of a subscription.

	URL: http://hl7.org/fhir/subscription-status
	ValueSet: http://hl7.org/fhir/ValueSet/subscription-status
	"""
	
	requested = "requested"
	""" The client has requested the subscription, and the server has not yet set it up.
	"""
	
	active = "active"
	""" The subscription is active.
	"""
	
	error = "error"
	""" The server has an error executing the notification.
	"""
	
	off = "off"
	""" Too many errors have occurred or the subscription has expired.
	"""



class SubscriptionTag(object):
	""" Tags to put on a resource after subscriptions have been sent.

	URL: http://hl7.org/fhir/subscription-tag
	ValueSet: http://hl7.org/fhir/ValueSet/subscription-tag
	"""
	
	queued = "queued"
	""" The message has been queued for processing on a destination systems.
	"""
	
	delivered = "delivered"
	""" The message has been delivered to its intended recipient.
	"""



class SupplyDeliveryStatus(object):
	""" Status of the supply delivery.

	URL: http://hl7.org/fhir/supplydelivery-status
	ValueSet: http://hl7.org/fhir/ValueSet/supplydelivery-status
	"""
	
	inProgress = "in-progress"
	""" Supply has been requested, but not delivered.
	"""
	
	completed = "completed"
	""" Supply has been delivered ("completed").
	"""
	
	abandoned = "abandoned"
	""" Dispensing was not completed.
	"""



class SupplyRequestReason(object):
	""" Why the supply item was requested

	URL: http://hl7.org/fhir/supplyrequest-reason
	ValueSet: http://hl7.org/fhir/ValueSet/supplyrequest-reason
	"""
	
	patientCare = "patient-care"
	""" The supply has been requested for use in direct patient care.
	"""
	
	wardStock = "ward-stock"
	""" The supply has been requested for for creating or replenishing ward stock.
	"""



class SupplyRequestStatus(object):
	""" Status of the supply request

	URL: http://hl7.org/fhir/supplyrequest-status
	ValueSet: http://hl7.org/fhir/ValueSet/supplyrequest-status
	"""
	
	requested = "requested"
	""" Supply has been requested, but not dispensed.
	"""
	
	completed = "completed"
	""" Supply has been received by the requestor.
	"""
	
	failed = "failed"
	""" The supply will not be completed because the supplier was unable or unwilling to supply the item.
	"""
	
	cancelled = "cancelled"
	""" The orderer of the supply cancelled the request.
	"""



class SystemVersionProcessingMode(object):
	""" How to manage the intersection between a fixed version in a value set, and a fixed version of the system in the
expansion profile

	URL: http://hl7.org/fhir/system-version-processing-mode
	ValueSet: http://hl7.org/fhir/ValueSet/system-version-processing-mode
	"""
	
	default = "default"
	""" Use this version of the code system if a value set doesn't specify a version
	"""
	
	check = "check"
	""" Use this version of the code system. If a value set specifies a different version, the expansion operation
	/// should fail
	"""
	
	override = "override"
	""" Use this version of the code system irrespective of which version is specified by a value set. Note that this
	/// has obvious safety issues, in that it may result in a value set expansion giving a different list of codes that
	/// is both wrong and unsafe, and implementers should only use this capability reluctantly. It primarily exists to
	/// deal with situations where specifications have fallen into decay as time passes
	"""



class TaskPerformerType(object):
	""" The type(s) of task performers allowed

	URL: http://hl7.org/fhir/task-performer-type
	ValueSet: http://hl7.org/fhir/ValueSet/task-performer-type
	"""
	
	requester = "requester"
	""" A workflow participant that requests services.
	"""
	
	dispatcher = "dispatcher"
	""" A workflow participant that dispatches services (assigns another task to a participant).
	"""
	
	scheduler = "scheduler"
	""" A workflow participant that schedules (dispatches and sets the time or date for performance of) services.
	"""
	
	performer = "performer"
	""" A workflow participant that performs services.
	"""
	
	monitor = "monitor"
	""" A workflow participant that monitors task activity.
	"""
	
	manager = "manager"
	""" A workflow participant that manages task activity.
	"""
	
	acquirer = "acquirer"
	""" A workflow participant that acquires resources (specimens, images, etc) necessary to perform the task.
	"""
	
	reviewer = "reviewer"
	""" A workflow participant that reviews task inputs or outputs.
	"""



class TaskStatus(object):
	""" The current status of the task.

	URL: http://hl7.org/fhir/task-status
	ValueSet: http://hl7.org/fhir/ValueSet/task-status
	"""
	
	draft = "draft"
	""" The task is not yet ready to be acted upon.
	"""
	
	requested = "requested"
	""" The task is ready to be acted upon and action is sought
	"""
	
	received = "received"
	""" A potential performer has claimed ownership of the task and is evaluating whether to perform it
	"""
	
	accepted = "accepted"
	""" The potential performer has agreed to execute the task but has not yet started work
	"""
	
	rejected = "rejected"
	""" The potential performer who claimed ownership of the task has decided not to execute it prior to performing any
	/// action.
	"""
	
	ready = "ready"
	""" Task is ready to be performed, but no action has yet been taken.  Used in place of
	/// requested/received/accepted/rejected when request assignment and acceptance is a given.
	"""
	
	cancelled = "cancelled"
	""" the task was not completed (more or less) as requested
	"""
	
	inProgress = "in-progress"
	""" Task has been started but is not yet complete.
	"""
	
	onHold = "on-hold"
	""" Task has been started but work has been paused
	"""
	
	failed = "failed"
	""" The task was attempted but could not be completed due to some error.
	"""
	
	completed = "completed"
	""" The task has been completed (more or less) as requested.
	"""
	
	enteredInError = "entered-in-error"
	""" The task should never have existed and is retained only because of the possibility it may have used
	"""



class TestReportParticipantType(object):
	""" The type of participant.

	URL: http://hl7.org/fhir/report-participant-type
	ValueSet: http://hl7.org/fhir/ValueSet/report-participant-type
	"""
	
	testEngine = "test-engine"
	""" The test execution engine.
	"""
	
	client = "client"
	""" A FHIR Client
	"""
	
	server = "server"
	""" A FHIR Server
	"""



class TestReportResultCodes(object):
	""" The results of executing an action.

	URL: http://hl7.org/fhir/report-result-codes
	ValueSet: http://hl7.org/fhir/ValueSet/report-result-codes
	"""
	
	# pass = "pass"
	""" The action was successful.
	"""
	
	skip = "skip"
	""" The action was skipped.
	"""
	
	fail = "fail"
	""" The action failed.
	"""
	
	warning = "warning"
	""" The action passed but with warnings.
	"""
	
	error = "error"
	""" The action encountered a fatal error and the engine was unable to process.
	"""



class TestReportStatus(object):
	""" The execution status of the TestReport.

	URL: http://hl7.org/fhir/report-status-codes
	ValueSet: http://hl7.org/fhir/ValueSet/report-status-codes
	"""
	
	complete = "complete"
	""" The TestReport is complete.
	"""
	
	pending = "pending"
	""" The TestReport is pending.
	"""
	
	error = "error"
	""" The TestReport failed with an error.
	"""



class TransactionMode(object):
	""" A code that indicates how transactions are supported.

	URL: http://hl7.org/fhir/transaction-mode
	ValueSet: http://hl7.org/fhir/ValueSet/transaction-mode
	"""
	
	notSupported = "not-supported"
	""" Neither batch or transaction is supported.
	"""
	
	batch = "batch"
	""" Batches are  supported.
	"""
	
	transaction = "transaction"
	""" Transactions are supported.
	"""
	
	both = "both"
	""" Both batches and transactions are supported.
	"""



class TriggerType(object):
	""" The type of trigger

	URL: http://hl7.org/fhir/trigger-type
	ValueSet: http://hl7.org/fhir/ValueSet/cqif-trigger-type
	"""
	
	namedEvent = "named-event"
	""" The trigger occurs in response to a specific named event
	"""
	
	periodic = "periodic"
	""" The trigger occurs at a specific time or periodically as described by a timing or schedule
	"""
	
	dataAdded = "data-added"
	""" The trigger occurs whenever data of a particular type is added
	"""
	
	dataModified = "data-modified"
	""" The trigger occurs whenever data of a particular type is modified
	"""
	
	dataRemoved = "data-removed"
	""" The trigger occurs whenever data of a particular type is removed
	"""
	
	dataAccessed = "data-accessed"
	""" The trigger occurs whenever data of a particular type is accessed
	"""
	
	dataAccessEnded = "data-access-ended"
	""" The trigger occurs whenever access to data of a particular type is completed
	"""



class TypeDerivationRule(object):
	""" How a type relates to it's baseDefinition.

	URL: http://hl7.org/fhir/type-derivation-rule
	ValueSet: http://hl7.org/fhir/ValueSet/type-derivation-rule
	"""
	
	specialization = "specialization"
	""" This definition defines a new type that adds additional elements to the base type
	"""
	
	constraint = "constraint"
	""" This definition adds additional rules to an existing concrete type
	"""



class UnknownContentCode(object):
	""" A code that indicates whether an application accepts unknown elements or extensions when reading resources.

	URL: http://hl7.org/fhir/unknown-content-code
	ValueSet: http://hl7.org/fhir/ValueSet/unknown-content-code
	"""
	
	no = "no"
	""" The application does not accept either unknown elements or extensions.
	"""
	
	extensions = "extensions"
	""" The application accepts unknown extensions, but not unknown elements.
	"""
	
	elements = "elements"
	""" The application accepts unknown elements, but not unknown extensions.
	"""
	
	both = "both"
	""" The application accepts unknown elements and extensions.
	"""



class UsageContextType(object):
	""" A code the specifies a type of context being specified by a usage context

	URL: http://hl7.org/fhir/usage-context-type
	ValueSet: http://hl7.org/fhir/ValueSet/usage-context-type
	"""
	
	gender = "gender"
	""" The gender of the patient. For this context type, the value should be a code taken from the
	/// [AdministrativeGender](valueset-administrative-gender.html) value set
	"""
	
	age = "age"
	""" The age of the patient. For this context type, the value should be a range the specifies the applicable ages or
	/// a code from the MeSH value set AgeGroupObservationValue
	"""
	
	focus = "focus"
	""" The clinical concept(s) addressed by the artifact. For example, disease, diagnostic test interpretation,
	/// medication ordering.
	"""
	
	user = "user"
	""" The clinical speciality of the context in which the patient is bring treated - For example, PCP, Patient,
	/// Cardiologist, Behavioral Professional, Oral Health Professional, Prescriber, etc... taken from the NUCC Health
	/// Care provider taxonomyCode system (OID: 2.16.840.1.113883.6.101).
	"""
	
	workflow = "workflow"
	""" The settings in which the artifact is intended for use. For example, admission, pre-op, etc
	"""
	
	task = "task"
	""" The context for the clinical task(s) represented by this artifact. Can be any task context represented by the
	/// HL7 ActTaskCode value set (OID: 2.16.840.1.113883.1.11.19846). General categories include: order entry, patient
	/// documentation and patient information review.
	"""
	
	venue = "venue"
	""" The venue in which an artifact could be used. For example, Outpatient, Inpatient, Home, Nursing home. The code
	/// value may originate from either the HL7 ActEncounter (OID: 2.16.840.1.113883.1.11.13955) or NUCC non-individual
	/// provider codes OID: 2.16.840.1.113883.1.11.19465.
	"""



class Use(object):
	""" Complete, proposed, exploratory, other

	URL: http://hl7.org/fhir/claim-use
	ValueSet: http://hl7.org/fhir/ValueSet/claim-use
	"""
	
	complete = "complete"
	""" The treatment is complete and this represents a Claim for the services.
	"""
	
	proposed = "proposed"
	""" The treatment is proposed and this represents a Pre-authorization for the services.
	"""
	
	exploratory = "exploratory"
	""" The treatment is proposed and this represents a Pre-determination for the services.
	"""
	
	other = "other"
	""" A locally defined or otherwise resolved status.
	"""



class VisionBase(object):
	""" A coded concept listing the base codes.

	URL: http://hl7.org/fhir/vision-base-codes
	ValueSet: http://hl7.org/fhir/ValueSet/vision-base-codes
	"""
	
	up = "up"
	""" top
	"""
	
	down = "down"
	""" bottom
	"""
	
	# in = "in"
	""" inner edge
	"""
	
	out = "out"
	""" outer edge
	"""



class VisionEyes(object):
	""" A coded concept listing the eye codes.

	URL: http://hl7.org/fhir/vision-eye-codes
	ValueSet: http://hl7.org/fhir/ValueSet/vision-eye-codes
	"""
	
	right = "right"
	""" Right Eye
	"""
	
	left = "left"
	""" Left Eye
	"""



class XPathUsageType(object):
	""" How a search parameter relates to the set of elements returned by evaluating its xpath query.

	URL: http://hl7.org/fhir/search-xpath-usage
	ValueSet: http://hl7.org/fhir/ValueSet/search-xpath-usage
	"""
	
	normal = "normal"
	""" The search parameter is derived directly from the selected nodes based on the type definitions.
	"""
	
	phonetic = "phonetic"
	""" The search parameter is derived by a phonetic transform from the selected nodes.
	"""
	
	nearby = "nearby"
	""" The search parameter is based on a spatial transform of the selected nodes.
	"""
	
	distance = "distance"
	""" The search parameter is based on a spatial transform of the selected nodes, using physical distance from the
	/// middle.
	"""
	
	other = "other"
	""" The interpretation of the xpath statement is unknown (and can't be automated).
	"""

