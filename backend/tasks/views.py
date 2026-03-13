from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task, TaskSubmission
from .serializers import TaskSerializer, TaskSubmissionSerializer, StudentTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Task ViewSet: Provides CRUD operations for tasks
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Filter tasks by user role"""
        user = self.request.user
        if not user.is_authenticated:
            return Task.objects.none()

        if user.role == 'student':
            # Students can only see tasks for enrolled courses
            from courses.models import Enrollment
            enrolled_course_ids = Enrollment.objects.filter(
                student=user,
                status='active'
            ).values_list('course_id', flat=True)
            return Task.objects.filter(course_id__in=enrolled_course_ids)
        elif user.role == 'teacher':
            # Teachers can only see tasks for their courses
            return Task.objects.filter(course__teacher=user)
        return Task.objects.all()

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """
        Get current student's all tasks
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can view task list'},
                status=status.HTTP_403_FORBIDDEN
            )

        tasks = self.get_queryset()
        serializer = StudentTaskSerializer(
            tasks,
            many=True,
            context={'student': request.user}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Get pending tasks list
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can view pending tasks'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Filter pending submission tasks
        from courses.models import Enrollment
        enrolled_course_ids = Enrollment.objects.filter(
            student=request.user,
            status='active'
        ).values_list('course_id', flat=True)

        tasks = Task.objects.filter(course_id__in=enrolled_course_ids)

        # Filter unsubmitted tasks
        submitted_task_ids = TaskSubmission.objects.filter(
            student=request.user
        ).values_list('task_id', flat=True)

        pending_tasks = tasks.exclude(id__in=submitted_task_ids)

        serializer = StudentTaskSerializer(
            pending_tasks,
            many=True,
            context={'student': request.user}
        )
        return Response(serializer.data)


class TaskSubmissionViewSet(viewsets.ModelViewSet):
    """
    Task Submission ViewSet: Provides CRUD operations for task submissions
    """
    queryset = TaskSubmission.objects.all()
    serializer_class = TaskSubmissionSerializer

    def get_queryset(self):
        """Filter submissions by user role"""
        user = self.request.user
        if not user.is_authenticated:
            return TaskSubmission.objects.none()

        if user.role == 'student':
            # Students can only see their own submissions
            return TaskSubmission.objects.filter(student=user)
        elif user.role == 'teacher':
            # Teachers can see submissions for their courses
            return TaskSubmission.objects.filter(task__course__teacher=user)
        return TaskSubmission.objects.all()

    def perform_create(self, serializer):
        """Auto set student and status when creating submission"""
        serializer.save(
            student=self.request.user,
            status='submitted'
        )

    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """
        Teacher grading endpoint
        """
        submission = self.get_object()

        if request.user.role != 'teacher':
            return Response(
                {'error': 'Only teachers can grade'},
                status=status.HTTP_403_FORBIDDEN
            )

        if submission.task.course.teacher != request.user:
            return Response(
                {'error': 'You are not authorized to grade this submission'},
                status=status.HTTP_403_FORBIDDEN
            )

        score = request.data.get('score')
        feedback = request.data.get('feedback', '')

        if score is None:
            return Response(
                {'error': 'Please provide a score'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            score = float(score)
            if score < 0 or score > submission.task.total_score:
                return Response(
                    {'error': f'Score must be between 0 and {submission.task.total_score}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Score must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        submission.score = score
        submission.feedback = feedback
        submission.status = 'graded'
        submission.graded_at = timezone.now()
        submission.save()

        return Response(TaskSubmissionSerializer(submission).data)

    @action(detail=False, methods=['get'])
    def course_submissions(self, request):
        """
        Get all submissions for a course (for teachers)
        """
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {'error': 'Please provide course ID'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.role != 'teacher':
            return Response(
                {'error': 'Only teachers can view course submissions'},
                status=status.HTTP_403_FORBIDDEN
            )

        submissions = TaskSubmission.objects.filter(
            task__course_id=course_id,
            task__course__teacher=request.user
        )

        serializer = TaskSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
