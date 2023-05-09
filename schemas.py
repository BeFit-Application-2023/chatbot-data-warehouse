# Importing all needed modules.
from marshmallow import Schema, fields, ValidationError


# Defining the Named-Entities Schema.
class NamedEntitiesSchema(Schema):
    # Defining the required schema fields.
    PERSON = fields.List(fields.Str(), required=False)
    NORP = fields.List(fields.Str(), required=False)
    FAC = fields.List(fields.Str(), required=False)
    ORG = fields.List(fields.Str(), required=False)
    GPE = fields.List(fields.Str(), required=False)
    LOC = fields.List(fields.Str(), required=False)
    PRODUCT = fields.List(fields.Str(), required=False)
    EVENT = fields.List(fields.Str(), required=False)
    WORD_OF_ART = fields.List(fields.Str(), required=False)
    LAW = fields.List(fields.Str(), required=False)
    LANGUAGE = fields.List(fields.Str(), required=False)
    DATE = fields.List(fields.Str(), required=False)
    TIME = fields.List(fields.Str(), required=False)
    PERCENT = fields.List(fields.Str(), required=False)
    MONEY = fields.List(fields.Str(), required=False)
    QUANTITY = fields.List(fields.Str(), required=False)
    ORDINAL = fields.List(fields.Str(), required=False)
    CARDINAL = fields.List(fields.Str(), required=False)

    def validate_json(self, json_data : dict):
        '''
            This function validates the requests body.
                :param json_data: dict
                    The request body.
                :returns: dict, int
                    Returns the validated json or the errors in the json
                    and the status code.
        '''
        try:
            result = self.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        return result, 200


# Defining the Message Schema.
class MessageSchema(Schema):
    # Defining the required schema fields.
    time = fields.Float(required=True)
    correlation_id = fields.Str(required=True)
    text = fields.Str(required=True)
    intent = fields.Str(required=True)
    sentiment = fields.Float(required=True)
    ner = fields.Nested(NamedEntitiesSchema, required=True)
    response = fields.Str(required=True)
    is_seq2seq = fields.Bool(required=True)
    business_logic_response = fields.Raw(required=True, allow_none=True)
    is_intent_cached = fields.Bool(required=True)
    is_sentiment_cached = fields.Bool(required=True)
    is_ner_cached = fields.Bool(required=True)
    is_sequence_cached = fields.Bool(required=True)
    telegram_user_id = fields.Integer(required=True)

    def validate_json(self, json_data : dict):
        '''
            This function validates the requests body.
                :param json_data: dict
                    The request body.
                :returns: dict, int
                    Returns the validated json or the errors in the json
                    and the status code.
        '''
        try:
            result = self.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        return result, 200


# Defining the User Schema.
class UserSchema(Schema):
    # Defining the required schema fields.
    user_id = fields.Str(required=True)
    telegram_user_id = fields.Integer(required=True)
    chat_id = fields.Integer(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    telegram_username = fields.Str(required=True)
    app_id = fields.Integer(required=True)

    def validate_json(self, json_data : dict):
        '''
            This function validates the requests body.
                :param json_data: dict
                    The request body.
                :returns: dict, int
                    Returns the validated json or the errors in the json
                    and the status code.
        '''
        try:
            result = self.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        return result, 200


# Defining the Latency Schema.
class LatencySchema(Schema):
    # Defining the required schema fields.
    lock_time = fields.Number(required=True)
    queue_waiting_time = fields.Number(required=True)
    actual_processing = fields.Number(required=True)
    task_service_time = fields.Number(required=True)
    database_response_time = fields.Number(required=True)

    def validate_json(self, json_data : dict):
        '''
            This function validates the requests body.
                :param json_data: dict
                    The request body.
                :returns: dict, int
                    Returns the validated json or the errors in the json
                    and the status code.
        '''
        try:
            result = self.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        return result, 200


# Defining the Saturation Schema.
class SaturationSchema(Schema):
    # Defining the required schema fields.
    cpu_utilization = fields.Number(required=True)
    ram_utilization = fields.Number(required=True)
    waiting_queue_length = fields.Number(required=True)
    thread_capacity = fields.Number(required=True)

    def validate_json(self, json_data : dict):
        '''
            This function validates the requests body.
                :param json_data: dict
                    The request body.
                :returns: dict, int
                    Returns the validated json or the errors in the json
                    and the status code.
        '''
        try:
            result = self.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        return result, 200


# Defining the Errors Schema.
class ErrorsSchema(Schema):
    # Defining the required schema fields.
    request_status = fields.Integer(required=True)
    request_reason = fields.Str(required=True)
    db_error = fields.Str(required=True, allow_none=True)

    def validate_json(self, json_data : dict):
        '''
            This function validates the requests body.
                :param json_data: dict
                    The request body.
                :returns: dict, int
                    Returns the validated json or the errors in the json
                    and the status code.
        '''
        try:
            result = self.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        return result, 200


# Defining the Traffic Schema.
class TrafficSchema(Schema):
    # Defining the required schema fields.
    write_query = fields.Integer(required=True)
    read_query = fields.Integer(required=True)

    def validate_json(self, json_data : dict):
        '''
            This function validates the requests body.
                :param json_data: dict
                    The request body.
                :returns: dict, int
                    Returns the validated json or the errors in the json
                    and the status code.
        '''
        try:
            result = self.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        return result, 200


# Defining the Metrics Schema.
class MetricsSchema(Schema):
    # Defining the required schema fields.
    correlation_id = fields.Str(required=True)
    service_name = fields.Str(required=True)
    latency = fields.Nested(LatencySchema, required=False)
    saturation = fields.Nested(SaturationSchema, required=False)
    errors = fields.Nested(ErrorsSchema, required=True)
    traffic = fields.Nested(TrafficSchema, required=False)

    def validate_json(self, json_data : dict):
        '''
            This function validates the requests body.
                :param json_data: dict
                    The request body.
                :returns: dict, int
                    Returns the validated json or the errors in the json
                    and the status code.
        '''
        try:
            result = self.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        return result, 200
