import json
from cassowary.mq.message_queues import MessageQueues


class BaseParser:
    """
    The target of this class is to represent a parser.
    Each parser has the opportunity to init a message queue
    and to parse results
    """

    def __init__(self):
        self.queue = None

    def parse(self, data: dict) -> dict:
        """
        :param data: the data as received from the message queue
        :return: the parsed data to send to the message queue
        """
        raise NotImplementedError()

    def init_message_queue(self, publish_url):
        """
        This method initialized a rabbitMQ message queue
        :param publish_url: the path to mq server
        """
        print('establishing a message queue...')
        MessageQueues.load_mqs()
        queue = MessageQueues.get_message_queue(publish_url)
        self.queue = queue
        queue.define_queue('parsed-result')
        queue.define_publish_queue('raw-snapshot')
        print('start listening for snapshots...')
        queue.bind_queue_to_exchange('raw-snapshot', self.callback)

    def callback(self, raw_result):
        """
        This is our MQ callback, responsible for receiving the raw data
        and passing the parsed result to the message queue
        """
        parsed_data = self.parse(json.loads(raw_result))
        print('parsed data: ', parsed_data)
        self.queue.publish_to_queue('', 'parsed-result',
                                    json.dumps(parsed_data))
