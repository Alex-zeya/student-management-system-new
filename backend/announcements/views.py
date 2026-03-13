from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    Announcement ViewSet: Provides CRUD operations for announcements
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    
    def get_queryset(self):
        """Filter announcements by user role"""
        user = self.request.user
        if not user.is_authenticated:
            return Announcement.objects.none()
        
        if user.role == 'student':
            from courses.models import Enrollment
            enrolled_course_ids = Enrollment.objects.filter(
                student=user,
                status='active'
            ).values_list('course_id', flat=True)
            return Announcement.objects.filter(
                course_id__in=enrolled_course_ids,
                is_active=True
            )
        elif user.role == 'teacher':
            return Announcement.objects.filter(course__teacher=user)
        return Announcement.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        """Set created_by when creating announcement"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def course_announcements(self, request):
        """
        Get course announcement list
        """
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {'error': 'Please provide course_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        announcements = self.get_queryset().filter(course_id=course_id)
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)
