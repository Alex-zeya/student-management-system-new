from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .models import CourseResource
from .serializers import CourseResourceSerializer


class CourseResourceViewSet(viewsets.ModelViewSet):
    """
    Course resource ViewSet: Provides CRUD operations for course resources
    """
    queryset = CourseResource.objects.all()
    serializer_class = CourseResourceSerializer
    
    def get_queryset(self):
        """Filter resources by user role"""
        user = self.request.user
        if not user.is_authenticated:
            return CourseResource.objects.none()
        
        if user.role == 'student':
            from courses.models import Enrollment
            enrolled_course_ids = Enrollment.objects.filter(
                student=user,
                status='active'
            ).values_list('course_id', flat=True)
            return CourseResource.objects.filter(
                course_id__in=enrolled_course_ids,
                is_visible=True
            )
        elif user.role == 'teacher':
            return CourseResource.objects.filter(course__teacher=user)
        return CourseResource.objects.filter(is_visible=True)
    
    def perform_create(self, serializer):
        """Set uploaded_by when creating resource"""
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download resource endpoint
        """
        resource = self.get_object()
        resource.download_count += 1
        resource.save()
        
        return FileResponse(
            resource.file,
            as_attachment=True,
            filename=resource.file.name.split('/')[-1]
        )
    
    @action(detail=False, methods=['get'])
    def course_resources(self, request):
        """
        Get course resource list
        """
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {'error': 'Please provide course_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resources = self.get_queryset().filter(course_id=course_id)
        serializer = CourseResourceSerializer(resources, many=True)
        return Response(serializer.data)
