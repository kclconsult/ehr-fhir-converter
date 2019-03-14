from builtins import object

class TranslationConstants(object):

    DEMO = False;

    MODELS_PATH = "models_subset";

    EHR_PATH = "tpp/tpp";
    # EHR_PATH = "mmedica/mmedica";

    EHR_ENTRY_POINT = "Response";
    # EHR_ENTRY_POINT = "session";

    SEPARATOR = "";
    # SEPARATOR = "_";

    #

    COMPOSITE_STRING_SIMILARITY_HIGHEST_COMPOSITE_RESULT=True; # alpha

    METRICS_FIRST_PAST_THRESHOLD=False; # beta

    METRICS_HIGHEST_STRENGTH=False; # gamma

    METRICS_COMBINED=False; # delta

    METRICS_AVERAGE=True; # epsilon

    # Thresholds don't have to be the same at every stage.
    OVERALL_SIMILARITY_THRESHOLD = 0.95; # tau

    TEXT_SIMILARITY_THRESHOLD = 0.95; # tau_{t}

    MORPHOLOGICAL_SIMILARITY_THRESHOLD = 0.95; # tau_{m}

    SEMANTIC_SIMILARITY_THRESHOLD = 0.95; # tau_{s}

    # Might want to be more generous with child matches.
    OVERALL_CHILD_SIMILARITY_THRESHOLD = 0.95;

    FUZZY_SIMILARITY_THRESHOLD = 0.75;

    # If some metrics are too generous (e.g. semantic matching 'address' and 'reference'), then we can reduce their 'contribution' to the measure of similarity using a weighting.
    TEXT_SIMILARITY_WEIGHTING = 1; # omega_{t}

    MORPHOLOGICAL_SIMILARITY_WEIGHTING = 1; # omega_{m}

    SEMANTIC_SIMILARITY_WEIGHTING = 0.95; # omega_{s}

    #

    EXCLUDED_FHIR_CLASS_TYPES = { "Extension", "FHIR", "BackboneElement", "DomainResource", "Reference" };

    SELECTIVE_RECURSE = [];
    # SELECTIVE_RECURSE = [ "CodeableConcept", "Coding" ];

    FIELDS_THAT_INDICATE_RESOURCE_CAN_HOLD_ANY_DATA = ["value", "text", "val"];

    TYPES_TO_REGEX = { "str": "[A-Za-z]*", "bool": "([Tt]rue|[Ff]alse)"}

    LENGTH_TO_IGNORE_IN_COMPOSITE_HIGHEST = 2;

    # MAX_HOPS = ;
