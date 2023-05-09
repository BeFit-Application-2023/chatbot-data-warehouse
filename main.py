# Importing the external libraries.
from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
import threading
import requests
import time
import uuid

# Importing all needed modules.
from models import db, MessagesModel, DateModel, LatencyModel, TrafficModel, ErrorsModel, SaturationModel, UserModel
from schemas import MetricsSchema, UserSchema, MessageSchema
from cerber import SecurityManager
from config import ConfigManager
from utils import unix_to_date_dict

# Creation of the Validation Schemas.
metrics_schema = MetricsSchema()
user_schema = UserSchema()
message_schema = MessageSchema()

# Creation of the config manager.
config = ConfigManager("config.ini")

# Creation of the Security Manager.
security_manager = SecurityManager(config.security.secret_key)

# Setting up the sqlalchemy database uri.
sqlalchemy_database_uri = f"postgresql://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.db_name}"

# Setting up the Flask dependencies.
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_database_uri
app.secret_key = config.security.secret_key

#db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Creating the security manager for the service discovery.
service_discovery_security_manager = SecurityManager(config.service_discovery.secret_key)

# Computing the HMAC for Service Discovery registration.
SERVICE_DISCOVERY_HMAC = service_discovery_security_manager._SecurityManager__encode_hmac(
    config.generate_info_for_service_discovery()
)

def send_heartbeats():
    '''
        This function sends heartbeat requests to the service discovery.
    '''
    # Getting the Service discovery hmac for message.
    service_discovery_hmac = service_discovery_security_manager._SecurityManager__encode_hmac({"status_code" : 200})
    while True:
        # Senting the request.
        response = requests.post(
            f"http://{config.service_discovery.host}:{config.service_discovery.port}/heartbeat/{config.general.name}",
            json = {"status_code" : 200},
            headers = {"Token" : service_discovery_hmac}
        )
        # Making a pause of 30 seconds before sending the next request.
        status_code = response.status_code
        time.sleep(30)


# Registering to the Service discovery.
while True:
    # Sending the request to the service discovery.
    resp = requests.post(
        f"http://{config.service_discovery.host}:{config.service_discovery.port}/{config.service_discovery.register_endpoint}",
        json = config.generate_info_for_service_discovery(),
        headers={"Token" : SERVICE_DISCOVERY_HMAC}
    )
    # If the request is succesfull then sending of heartbeat requests is starting.
    if resp.status_code == 200:
        threading.Thread(target=send_heartbeats).start()
        break


# Creation of the tables in the database.
with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

@app.route("/metrics", methods = ["POST"])
def metrics():
    # Checking the access token.
    check_response = security_manager.check_request(request)
    if check_response != "OK":
        return check_response, check_response["code"]
    else:
        status_code = 200
        # Validating the request body schema.
        result, status_code = metrics_schema.validate_json(request.json)
        if status_code != 200:
            return result, status_code
        else:
            # Extracting the correlation id and the service name.
            correlation_id = result["correlation_id"]
            service_name = result["service_name"]

            # Extracting from the database the message with the correlation id.
            message = MessagesModel.query.filter_by(id=correlation_id).first()

            # Creating the Latency metrics record.
            latency_index = uuid.uuid4()
            latency_record = LatencyModel(
                latency_index,
                result["latency"]["lock_time"],
                result["latency"]["queue_waiting_time"],
                result["latency"]["actual_processing"],
                result["latency"]["task_service_time"],
                result["latency"]["database_response_time"],
                service_name
            )

            # Creating the Traffic metrics record.
            traffic_index = uuid.uuid4()
            traffic_record = TrafficModel(
                traffic_index,
                result["traffic"]["write_query"],
                result["traffic"]["read_query"],
                service_name
            )

            # Creating the Errors metrics record.
            errors_index = uuid.uuid4()
            errors_record = ErrorsModel(
                errors_index,
                result["errors"]["request_status"],
                result["errors"]["db_error"],
                result["errors"]["request_reason"],
                service_name
            )

            # Creating the Saturation metrics record.
            saturation_index = uuid.uuid4()
            saturation_record = SaturationModel(
                saturation_index,
                result["saturation"]["cpu_utilization"],
                result["saturation"]["ram_utilization"],
                result["saturation"]["waiting_queue_length"],
                result["saturation"]["thread_capacity"],
                service_name
            )

            # Inserting the metrics records into the tables.
            db.session.add(latency_record)
            db.session.add(errors_record)
            db.session.add(traffic_record)
            db.session.add(saturation_record)

            # Trying to commit the records to the database.
            try:
                db.session.commit()
            except Exception as e:
                error = {
                    "name" : e.__class__.__name__,
                    "cause" : e.__cause__.__repr__()
                }
                return error, 500

            # Checking if there is a message with the provided correlation id.
            if not message:
                # In case the message is missing a new message record is created.
                message = MessagesModel(correlation_id)

            # Updating the message record with the service metrics indexes.
            if service_name == "intent-service":
                message.intent_errors_id = errors_index
                message.intent_traffic_id = traffic_index
                message.intent_saturation_id = saturation_index,
                message.intent_latency_id = latency_index
            elif service_name == "named-entity-recognition-service":
                message.ner_errors_id = errors_index
                message.ner_saturation_id = saturation_index
                message.ner_traffic_id = traffic_index
                message.ner_latency_id = latency_index
            elif service_name == "sentiment-service":
                message.sentiment_errors_id = errors_index
                message.sentiment_traffic_id = traffic_index
                message.sentiment_saturation_id = saturation_index
                message.sentiment_latency_id = latency_index
            elif service_name == "sequence2sequence-service":
                message.seq_errors_id = errors_index
                message.seq_traffic_id = traffic_index
                message.seq_saturation_id = saturation_index
                message.seq_latency_id = latency_index
            # Adding the message to the Messages table.
            db.session.add(message)

            # Trying to commit the changes.
            try:
                db.session.commit()
            except Exception as e:
                error = {
                    "name" : e.__class__.__name__,
                    "cause" : e.__cause__.__repr__()
                    }
                return error, 500
            # Returning the successful message.
            return {
                "message" : "Data saved!",
            }, 200

@app.route("/user", methods=["POST"])
def user():
    # Checking the access token.
    check_response = security_manager.check_request(request)
    if check_response != "OK":
        return check_response, check_response["code"]
    else:
        status_code = 200
        # Validating the request body schema.
        result, status_code = user_schema.validate_json(request.json)
        if status_code != 200:
            return result, status_code
        else:
            # Creating a new user record.
            new_user = UserModel(
                result["user_id"],
                result["telegram_user_id"],
                result["chat_id"],
                result["first_name"],
                result["last_name"],
                result["telegram_username"],
                result["app_id"]
            )
            # Inserting the user record into the User table.
            db.session.add(new_user)

            # Trying to commit the changes to the database.
            try:
                db.session.commit()
            except Exception as e:
                error = {
                    "name" : e.__class__.__name__,
                    "cause" : e.__cause__.__repr__()
                }
                return error, 500
            # Returning the successful message.
            return {
                "message" : "Data saved!",
            }, 200

@app.route("/message", methods=["POST"])
def message():
    # Checking the access token.
    check_response = security_manager.check_request(request)
    if check_response != "OK":
        return check_response, check_response["code"]
    else:
        status_code = 200
        # Validating the request body schema.
        result, status_code = message_schema.validate_json(request.json)
        if status_code != 200:
            return result, status_code
        else:
            # Creating a new id for the Date table.
            date_id = uuid.uuid4()

            # Converting the UNIX timestamp into date features.
            date_dict = unix_to_date_dict(result["time"])

            # Getting the id of the user sanding the message.
            user_id = UserModel.query.filter_by(telegram_id=result["telegram_user_id"]).first().id

            # Creating a new Date record.
            new_date_record = DateModel(
                date_id,
                date_dict["date"],
                date_dict["month"],
                date_dict["month_str"],
                date_dict["year"],
                date_dict["hour"],
                date_dict["minute"],
                date_dict["seconds"],
                date_dict["day_of_week"],
                date_dict["is_weekend"],
                date_dict["is_holiday"]
            )
            # Getting the Message record with the provided correlation id.
            message = MessagesModel.query.filter_by(id=result["correlation_id"]).first()

            # If there is a message with such a correlation id, then it's record is updated with the values
            # from the request body.
            if message:
                message.text = result["text"]
                message.intent = result["intent"]
                message.sentiment = result["sentiment"]
                message.ner = result["ner"]
                message.response = result["response"]
                message.is_seq2seq = result["is_seq2seq"]
                message.business_logic_response = result["business_logic_response"]
                message.is_intent_cached = result["is_intent_cached"]
                message.is_sentiment_cached = result["is_sentiment_cached"]
                message.is_ner_cached = result["is_ner_cached"]
                message.is_sequence_cached = result["is_sequence_cached"]
                message.user_id = user_id
                message.date_id = date_id
            # Inserting the date record to the data base.
            db.session.add(new_date_record)

            # Trying to commit the changes to the data base.
            try:
                db.session.commit()
            except Exception as e:
                error = {
                    "name" : e.__class__.__name__,
                    "cause" : e.__cause__.__repr__()
                }
                return error, 500
            # Returning the successful message.
            return {
                "message" : "Data saved!",
            }, 200

# Running the main flask module.
if __name__ == "__main__":
    app.run(
        #port=config.general.port,
        port=config.general.port,
        #host=config.general.host
        host="0.0.0.0"
    )