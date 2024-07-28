   # file_manager/views.py
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import File
import base64
from django.http import FileResponse, JsonResponse


from .googleDriveService import check_file_permissions, list_files, download_file
from .serializers import UserSerializer, RegisterSerializer, FileSerializer

class FileUploadView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
      files_data = request.data.get('files', [])  # Expecting a list of files
      if not isinstance(files_data, list):
          return Response({"error": "Invalid data format. Expected a list of files."}, status=status.HTTP_400_BAD_REQUEST)

      uploaded_files = []
      for file_data in files_data:
          google_drive_id = file_data.get('google_drive_id')

          # Check if the file already exists
          existing_file = File.objects.filter(google_drive_id=google_drive_id).first()
          if existing_file:
              # If the file exists, check if the user is the owner or already in shared_with
              if existing_file.owner == request.user or existing_file.shared_with.filter(id=request.user.id).exists():
                  return Response({"error": f"File '{existing_file.name}' is already uploaded by you or shared with you."}, status=status.HTTP_400_BAD_REQUEST)
              else:
                  # Add the current user to the shared_with field
                  existing_file.shared_with.add(request.user)
                  uploaded_files.append({"file_id": existing_file.id, "name": existing_file.name, "message": "File already uploaded by another user, you have been added to shared_with."})
          else:
              # If the file does not exist, create a new file entry
              serializer = FileSerializer(data=file_data, context={'request': request})
              if serializer.is_valid():
                  file = serializer.save(owner=request.user)
                  file.shared_with.add(request.user)  # Ensure the current user is in shared_with
                  uploaded_files.append({"file_id": file.id, "name": file.name})
              else:
                  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      return Response({"message": "Files processed successfully", "uploaded_files": uploaded_files}, status=status.HTTP_201_CREATED)
       
   # file_manager/views.py
class FileReadView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, file_id):
      try:
          file = File.objects.get(id=file_id)
          if request.user != file.owner and request.user not in file.shared_with.all():
              return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

          # Check permissions with Google Drive
          if not check_file_permissions(file.google_drive_id, request.user):
              print("p", file.google_drive_id, request.user.email)
              return Response({"error": "Permission denied by Google Drive"}, status=status.HTTP_403_FORBIDDEN)

          # Read the file content
          file_stream, file_name, mime_type = download_file(file.google_drive_id, file.name,request.user)  # Get mime_type
          if mime_type == 'text/csv' or mime_type == 'text/plain':
              file_content = file_stream.read().decode('utf-8')
              return JsonResponse({
                  'content': file_content,
                  'type': mime_type,
                  'name': file_name
              })
          else:
              file_content = file_stream.read()
              encoded_content = base64.b64encode(file_content).decode('utf-8')
              return JsonResponse({
                  'content': encoded_content,
                  'type': mime_type,
                  'name': file_name
              })
      except File.DoesNotExist:
          return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
      except Exception as e:
          return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
class RegisterView(generics.CreateAPIView):
       queryset = User.objects.all()
       serializer_class = RegisterSerializer


class ListFilesView(APIView):
       permission_classes = [IsAuthenticated]

       def get(self, request):
           files = list_files(request.user)
           return Response(files, status=200)
       
class ListAllFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id  # Get the ID of the currently authenticated user

        # Query to filter files where the user is either the owner or shared with
        files = File.objects.filter(Q(owner_id=user_id) | Q(shared_with=user_id))

        serializer = FileSerializer(files, many=True)  # Serialize the filtered file data
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data