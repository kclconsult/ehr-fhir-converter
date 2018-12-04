class TranslationConstants(object):

    MODELS_PATH = "models_subset";

    EHR_PATH = "tpp/tpp-extract";
    # EHR_PATH = "tpp/tpp-full";

    # Thresholds don't have to be the same at every stage.
    OVERALL_SIMILARITY_THRESHOLD = 0.95;

    TEXT_SIMILARITY_THRESHOLD = 0.95;

    SEMANTIC_SIMILARITY_THRESHOLD = 0.95;

    MORPHOLOGICAL_SIMILARITY_THRESHOLD = 0.95;

    # Might want to be more generous with child matches.
    OVERALL_CHILD_SIMILARITY_THRESHOLD = 0.95;

    # The portion of child fields in an EHR tag that must be housed by a FHIR class in order to consider that class a match (weighted by match strength (and candidate class specificity)).
    CHILD_MATCH_THRESHOLD = 0.1

    # If some metrics are too generous (e.g. semantic matching 'address' and 'reference'), then we can reduce their 'contribution' to the measure of similarity using a weighting.
    TEXT_SIMILARITY_WEIGHTING = 1;

    SEMANTIC_SIMILARITY_WEIGHTING = 0.95;

    MORPHOLOGICAL_SIMILARITY_WEIGHTING = 1;

    CONTEXT_WEIGHTING = 2;

    EXCLUDED_FHIR_CLASSES = { "Extension", "FHIR", "BackboneElement", "DomainResource" };

    # SELECTIVE_RECURSE = [];
    SELECTIVE_RECURSE = [ "CodeableConcept", "Coding" ];

    FIELDS_THAT_INDICATE_RESOURCE_CAN_HOLD_ANY_DATA = ["value", "text"];
