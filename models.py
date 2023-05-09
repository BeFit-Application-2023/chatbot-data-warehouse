from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Defining the date table.
class DateModel(db.Model):
    # Setting up the table name.
    __tablename__ = "date"

    # Setting up the column names and data types.
    id = db.Column(db.String(64), primary_key=True)
    date = db.Column(db.Date, unique=False)
    month = db.Column(db.Integer, unique=False)
    month_str = db.Column(db.String(16), unique=False)
    year = db.Column(db.Integer, unique=False)
    hour = db.Column(db.Integer, unique=False)
    minute = db.Column(db.Integer, unique=False)
    seconds = db.Column(db.Integer, unique=False)
    day_of_week = db.Column(db.Integer, unique=False)
    is_weekend = db.Column(db.Boolean, unique=False)
    is_holiday = db.Column(db.Boolean, unique=False)

    def __init__(self, index, date, month, month_str, year, hour, minute, seconds, day_of_week, is_weekend, is_holiday):

        self.id = index
        self.date = date
        self.month = month
        self.month_str = month_str
        self.year = year
        self.hour = hour
        self.minute = minute
        self.seconds = seconds
        self.day_of_week = day_of_week
        self.is_weekend = is_weekend
        self.is_holiday = is_holiday

    def __repr__(self):
        return f"<Date date = ({self.date})>"

# Defining the Latency Table.
class LatencyModel(db.Model):
    # Setting up the table name.
    __tablename__ = "latency"

    # Setting up the column names and data types.
    id = db.Column(db.String(64), primary_key=True)
    lock_time_per_process = db.Column(db.Float, unique=False)
    queue_waiting_time = db.Column(db.Float, unique=False)
    actual_processing_time = db.Column(db.Float, unique=False)
    task_service_time = db.Column(db.Float, unique=False)
    database_response_time = db.Column(db.Float, unique=False)
    service_name = db.Column(db.String(64), unique=False)

    def __init__(self,
                 index,
                 lock_time_per_process,
                 queue_waiting_time,
                 actual_processing_time,
                 task_service_time,
                 database_response_time,
                 service_name):
        self.id = index
        self.lock_time_per_process = lock_time_per_process
        self.queue_waiting_time = queue_waiting_time
        self.actual_processing_time = actual_processing_time
        self.task_service_time = task_service_time
        self.database_response_time = database_response_time
        self.service_name = service_name

    def __repr__(self):
        return f"<Latency(service name = {self.service_name})[lock time = {self.lock_time_per_process}, " \
               f"queue waiting time = {self.queue_waiting_time}, actual processing time = {self.actual_processing_time}," \
               f"task service time = {self.task_service_time}, database response time = {self.database_response_time}]>"

# Defining the Traffic Table.
class TrafficModel(db.Model):
    # Setting up the table name.
    __tablename__ = "traffic"

    # Setting up the column names and data types.
    id = db.Column(db.String(64), primary_key=True)
    write_query = db.Column(db.Integer, unique=False)
    read_query = db.Column(db.Integer, unique=False)
    service_name = db.Column(db.String(64), unique=False)

    def __init__(self, index, write_query, read_query, service_name):
        self.id = index
        self.write_query = write_query
        self.read_query = read_query
        self.service_name = service_name

    def __repr__(self):
        return f"<Traffic(service name = {self.service_name})[write query count = {self.write_query}, " \
               f"read query = {self.read_query}]>"

# Defining the Errors Table.
class ErrorsModel(db.Model):
    # Setting up the errors name.
    __tablename__ = "errors"

    # Setting up the column names and data types.
    id = db.Column(db.String(64), primary_key=True)
    status_code = db.Column(db.Integer, unique=False)
    db_error = db.Column(db.Text, unique=False, nullable=True)
    reason = db.Column(db.Text, unique=False, nullable=True)
    service_name = db.Column(db.String(64), unique=False)

    def __init__(self, index, status_code, db_error, reason, service_name):
        self.id = index
        self.status_code = status_code
        self.db_error = db_error
        self.reason = reason
        self.service_name = service_name

    def __repr__(self):
        return f"<Errors(service name = {self.service_name})[status code = {self.status_code}, " \
               f"database error = {self.db_error}, reason = {self.reason}]>"

# Defining the Saturation Table.
class SaturationModel(db.Model):
    # Setting up the table name.
    __tablename__ = "saturation"

    # Setting up the column names and data types.
    id = db.Column(db.String(64), primary_key=True)
    cpu_utilization = db.Column(db.Float, unique=False)
    ram_utilization = db.Column(db.Float, unique=False)
    waiting_queue_length = db.Column(db.Integer, unique=False)
    thread_capacity = db.Column(db.Float, unique=False)
    service_name = db.Column(db.String(64), unique=False)

    def __init__(self, index, cpu_utilization, ram_utilization, waiting_queue_length, thread_capacity, service_name):
        self.id = index
        self.cpu_utilization = cpu_utilization
        self.ram_utilization = ram_utilization
        self.waiting_queue_length = waiting_queue_length
        self.thread_capacity = thread_capacity
        self.service_name = service_name

    def __repr__(self):
        return f"<Saturation(service name = {self.service_name})[CPU utilization = {self.cpu_utilization}, " \
               f"RAM utilization = {self.ram_utilization}, waiting queue length = {self.waiting_queue_length}, " \
               f"thread capacity = {self.thread_capacity}]>"


# Defining the User Table.
class UserModel(db.Model):
    # Setting up the table name.
    __tablename__ = "user"

    # Setting up the column names and data types.
    id = db.Column(db.String(64), primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True)
    chat_id = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(32), unique=False, nullable=True)
    last_name = db.Column(db.String(32), unique=False, nullable=True)
    telegram_username = db.Column(db.String(64), unique=True, nullable=True)
    app_id = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, index, telegram_id, chat_id, first_name, last_name, telegram_username, app_id):
        self.id = index
        self.telegram_id = telegram_id
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.telegram_username = telegram_username
        self.app_id = app_id

    def __repr__(self):
        return f"<User telegram_id = {self.telegram_id}>"


# Defining the Fact Table.
class MessagesModel(db.Model):
    # Setting up the table name.
    __tablename__ = 'messages'

    # Setting up the column names and data types.
    id = db.Column(db.String(64), primary_key=True)
    text = db.Column(db.Text, unique=False, nullable=True)
    intent = db.Column(db.String(32), unique=False, nullable=True)
    sentiment = db.Column(db.Float, unique=False, nullable=True)
    ner = db.Column(db.JSON, unique=False, nullable=True)
    response = db.Column(db.Text, unique=False, nullable=True)
    is_seq2seq = db.Column(db.Boolean, unique=False, nullable=True)
    business_logic_response = db.Column(db.JSON, unique=False, nullable=True)

    # Cached values.
    is_intent_cached = db.Column(db.Boolean, unique=False, nullable=True)
    is_sentiment_cached = db.Column(db.Boolean, unique=False, nullable=True)
    is_ner_cached = db.Column(db.Boolean, unique=False, nullable=True)
    is_sequence_cached = db.Column(db.Boolean, unique=False, nullable=True)

    # Ids.
    date_id = db.Column(db.String(64), db.ForeignKey("date.id"), nullable=True)
    user_id = db.Column(db.String(64), db.ForeignKey("user.id"), nullable=True)

    # Metrics ids.
    intent_latency_id = db.Column(db.String(64), db.ForeignKey("latency.id"), nullable=True)
    intent_traffic_id = db.Column(db.String(64), db.ForeignKey("traffic.id"), nullable=True)
    intent_errors_id = db.Column(db.String(64), db.ForeignKey("errors.id"), nullable=True)
    intent_saturation_id = db.Column(db.String(64), db.ForeignKey("saturation.id"), nullable=True)

    sentiment_latency_id = db.Column(db.String(64), db.ForeignKey("latency.id"), nullable=True)
    sentiment_traffic_id = db.Column(db.String(64), db.ForeignKey("traffic.id"), nullable=True)
    sentiment_errors_id = db.Column(db.String(64), db.ForeignKey("errors.id"), nullable=True)
    sentiment_saturation_id = db.Column(db.String(64), db.ForeignKey("saturation.id"), nullable=True)

    ner_latency_id = db.Column(db.String(64), db.ForeignKey("latency.id"), nullable=True)
    ner_traffic_id = db.Column(db.String(64), db.ForeignKey("traffic.id"), nullable=True)
    ner_errors_id = db.Column(db.String(64), db.ForeignKey("errors.id"), nullable=True)
    ner_saturation_id = db.Column(db.String(64), db.ForeignKey("saturation.id"), nullable=True)

    seq_latency_id = db.Column(db.String(64), db.ForeignKey("latency.id"), nullable=True)
    seq_traffic_id = db.Column(db.String(64), db.ForeignKey("traffic.id"), nullable=True)
    seq_errors_id = db.Column(db.String(64), db.ForeignKey("errors.id"), nullable=True)
    seq_saturation_id = db.Column(db.String(64), db.ForeignKey("saturation.id"), nullable=True)

    bl_latency_id = db.Column(db.String(64), db.ForeignKey("latency.id"), nullable=True)
    bl_traffic_id = db.Column(db.String(64), db.ForeignKey("traffic.id"), nullable=True)
    bl_errors_id = db.Column(db.String(64), db.ForeignKey("errors.id"), nullable=True)
    bl_saturation_id = db.Column(db.String(64), db.ForeignKey("saturation.id"), nullable=True)

    def __init__(self, index):
        self.id = index
        self.text = None
        self.intent = None
        self.sentiment = None
        self.ner = None
        self.response = None
        self.is_seq2seq = None
        self.business_logic_response = None
        self.is_intent_cached = None
        self.is_sentiment_cached = None
        self.is_ner_cached = None
        self.is_sequence_cached = None
        self.date_id = None
        self.user_id = None

        self.intent_latency_id = None
        self.intent_traffic_id = None
        self.intent_errors_id = None
        self.intent_saturation_id = None

        self.sentiment_latency_id = None
        self.sentiment_traffic_id = None
        self.sentiment_errors_id = None
        self.sentiment_saturation_id = None

        self.ner_latency_id = None
        self.ner_traffic_id = None
        self.ner_errors_id = None
        self.ner_saturation_id = None

        self.seq_latency_id = None
        self.seq_traffic_id = None
        self.seq_errors_id = None
        self.seq_saturation_id = None

    def __repr__(self):
        return f"<Message(text = {self.text}, response = {self.response})>"