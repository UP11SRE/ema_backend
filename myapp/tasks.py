#    # file_manager/tasks.py
# from celery import shared_task
# from .models import File
# from .googleDriveService import get_drive_service
# import logging

# logger = logging.getLogger(__name__)

# @shared_task
# def process_file(file_id):
#        logger.info(f"Processing file with ID: {file_id}")
#        print(f"Processing file with ID: {file_id}")
#        try:
#            file = File.objects.get(id=file_id)
#            logger.info(f"File found: {file.name}")
#            service = get_drive_service()
#            # Fetch file content from Google Drive
#            request = service.files().get_media(fileId=file.google_drive_id)
#            file_content = request.execute()
#            logger.info(f"File content fetched successfully for: {file.name}")
#            # Update file processing status
#            FileProcessingStatus.objects.update_or_create(
#                file=file,
#                defaults={'status': 'Processed'}
#            )
#            logger.info(f"Processing status updated for file: {file.name}")
#        except File.DoesNotExist:
#            logger.error(f"File with ID {file_id} does not exist.")
#            FileProcessingStatus.objects.update_or_create(
#                file_id=file_id,
#                defaults={'status': 'Error: File not found'}
#            )
#        except Exception as e:
#            logger.error(f"Error processing file {file_id}: {str(e)}")
#            FileProcessingStatus.objects.update_or_create(
#                file_id=file_id,
#                defaults={'status': f'Error: {str(e)}'}
#            )