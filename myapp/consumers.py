#    # file_manager/consumers.py
# import json
# from channels.generic.websocket import WebsocketConsumer


# class FileProcessingConsumer(WebsocketConsumer):
#        def connect(self):
#            self.accept()

#        def disconnect(self, close_code):
#            pass

#        def receive(self, text_data):
#            data = json.loads(text_data)
#            file_id = data['file_id']
#            try:
#                status = FileProcessingStatus.objects.get(file_id=file_id).status
#            except FileProcessingStatus.DoesNotExist:
#                status = 'Unknown'
#            self.send(text_data=json.dumps({
#                'status': status,
#                'file_id': file_id
#            }))