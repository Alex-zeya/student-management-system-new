from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer, StudentCourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Course ViewSet: Provides CRUD operations for courses
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """Filter courses by user role"""
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.filter(is_active=True)

        if user.role == 'teacher':
            return Course.objects.filter(teacher=user)
        elif user.role == 'student':
            # Students can only see enrolled courses and active courses
            return Course.objects.filter(is_active=True)
        return Course.objects.all()

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """
        Student course enrollment endpoint
        """
        course = self.get_object()
        student = request.user

        if student.role != 'student':
            return Response(
                {'error': 'Only students can enroll in courses'},
                status=status.HTTP_403_FORBIDDEN
            )

        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response(
                {'error': 'You have already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if course.enrollments.count() >= course.max_students:
            return Response(
                {'error': 'Course is full'},
                status=status.HTTP_400_BAD_REQUEST
            )

        enrollment = Enrollment.objects.create(student=student, course=course)
        return Response(
            EnrollmentSerializer(enrollment).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def drop(self, request, pk=None):
        """
        Student course drop endpoint
        """
        course = self.get_object()
        student = request.user

        try:
            enrollment = Enrollment.objects.get(student=student, course=course)
            enrollment.status = 'dropped'
            enrollment.save()
            return Response({'message': 'Course dropped successfully'})
        except Enrollment.DoesNotExist:
            return Response(
                {'error': 'You have not enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """
        Get current student's enrolled courses
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can view enrolled courses'},
                status=status.HTTP_403_FORBIDDEN
            )

        enrollments = Enrollment.objects.filter(
            student=request.user,
            status='active'
        )
        courses = [e.course for e in enrollments]
        serializer = StudentCourseSerializer(
            courses,
            many=True,
            context={'student': request.user}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Get available courses (not enrolled and not full)
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can view available courses'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Exclude already enrolled courses
        enrolled_course_ids = Enrollment.objects.filter(
            student=request.user
        ).values_list('course_id', flat=True)

        courses = Course.objects.filter(
            is_active=True
        ).exclude(
            id__in=enrolled_course_ids
        )

        # Filter courses that are not full
        result = []
        for course in courses:
            if course.enrollments.count() < course.max_students:
                result.append(course)

        serializer = CourseSerializer(result, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """
        Get course's student list
        """
        course = self.get_object()
        enrollments = Enrollment.objects.filter(
            course=course,
            status='active'
        ).select_related('student')

        students_list = [e.student for e in enrollments]
        from users.serializers import UserSerializer
        serializer = UserSerializer(students_list, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def teaching(self, request):
        """
        Get current teacher's teaching courses
        """
        if request.user.role != 'teacher':
            return Response(
                {'error': 'Only teachers can view teaching courses'},
                status=status.HTTP_403_FORBIDDEN
            )

        courses = Course.objects.filter(teacher=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    Enrollment ViewSet: Provides CRUD operations for enrollment (admin only)
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Enrollment.objects.none()

        if user.role == 'admin':
            return Enrollment.objects.all()
        if user.role == 'teacher':
            return Enrollment.objects.filter(course__teacher=user)
        if user.role == 'student':
            return Enrollment.objects.filter(student=user)
        return Enrollment.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'error': 'Only admins can manage enrollments'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'error': 'Only admins can manage enrollments'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'error': 'Only admins can manage enrollments'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'error': 'Only admins can manage enrollments'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        enrollment = serializer.instance
        status_value = serializer.validated_data.get('status')
        if status_value == 'completed' and enrollment.completed_at is None:
            serializer.save(completed_at=timezone.now())
            return
        if status_value != 'completed' and enrollment.completed_at is not None:
            serializer.save(completed_at=None)
            return
        serializer.save()
