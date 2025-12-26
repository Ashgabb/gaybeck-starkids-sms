from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm
from .models import ActivityLog

User = get_user_model()

class LoginView(View):
    template_name = 'accounts/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Use the custom email authentication backend
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                ActivityLog.objects.create(
                    user=user,
                    action='LOGIN',
                    model_name='User',
                    ip_address=self.get_client_ip(request)
                )
                return redirect('dashboard:home')
            else:
                form.add_error(None, 'Invalid email or password')
        return render(request, self.template_name, {'form': form})
    
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        ActivityLog.objects.create(
            user=request.user,
            action='LOGOUT',
            model_name='User',
            ip_address=LoginView.get_client_ip(request)
        )
        logout(request)
        return redirect('accounts:login')

class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': form})

class ProfileView(LoginRequiredMixin, View):
    
    def get(self, request):
        user = request.user
        activity_logs = ActivityLog.objects.filter(user=user).values(
            'action', 'model_name', 'timestamp'
        )[:10]
        return JsonResponse({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'activity_logs': list(activity_logs)
        })

class ProfileEditView(LoginRequiredMixin, View):
    
    def post(self, request):
        user = request.user
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        return JsonResponse({'errors': form.errors}, status=400)

class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin()

class UserListView(LoginRequiredMixin, IsAdminMixin, View):
    
    def get(self, request):
        users = User.objects.values('id', 'email', 'first_name', 'last_name', 'role', 'is_active')
        return JsonResponse({
            'users': list(users),
            'count': users.count()
        })

class UserCreateView(LoginRequiredMixin, IsAdminMixin, View):
    
    def get(self, request):
        return JsonResponse({'message': 'Use POST to create user'})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'id': user.id,
                'email': user.email,
                'message': 'User created successfully'
            })
        return JsonResponse({'errors': form.errors}, status=400)

class UserEditView(LoginRequiredMixin, IsAdminMixin, View):
    
    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            form = CustomUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'User updated successfully'})
            return JsonResponse({'errors': form.errors}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

class UserDeleteView(LoginRequiredMixin, IsAdminMixin, View):
    
    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
