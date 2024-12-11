from django.urls import path, include
from . import views

app_name = 'my_app'

urlpatterns = [
    path('', views.home, name='home'),
    # User URLs
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),    
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),   


    # Profile URLs
    path('profiles/', views.ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),

    # Manuscript URLs
    path('manuscripts/', views.ManuscriptListCreateView.as_view(), name='manuscript-list-create'),
    path('manuscripts/<int:pk>/', views.ManuscriptDetailView.as_view(), name='manuscript-detail'),

    # Keyword URLs
    path('keywords/', views.KeywordListCreateView.as_view(), name='keyword-list'),
    path('keywords/<int:pk>/', views.KeywordDetailView.as_view(), name='keyword-detail'),

    # Feedback Question URLs
    path('feedback-questions/', views.FeedbackQuestionListCreateView.as_view(), name='feedback-question-list'),
    path('feedback-questions/<int:pk>/', views.FeedbackQuestionDetailView.as_view(), name='feedback-question-detail'),

    # Manuscript Feedback Preference URLs
    path('manuscript-feedback-preferences/', views.ManuscriptFeedbackPreferenceListCreateView.as_view(), name='manuscript-feedback-preference-list'),
    path('manuscript-feedback-preferences/<int:pk>/', views.ManuscriptFeedbackPreferenceDetailView.as_view(), name='manuscript-feedback-preference-detail'),

    # Feedback Response URLs
    path('feedback-responses/', views.FeedbackResponseListCreateView.as_view(), name='feedback-response-list'),
    path('feedback-responses/<int:pk>/', views.FeedbackResponseDetailView.as_view(), name='feedback-response-detail'),

    # Author Settings URLs
    path('author-settings/', views.AuthorSettingsListCreateView.as_view(), name='author-settings-list'),
    path('author-settings/<int:pk>/', views.AuthorSettingsDetailView.as_view(), name='author-settings-detail'),

    # Resource URLs
    path('resources/', views.ResourceListCreateView.as_view(), name='resource-list'),
    path('resources/<int:pk>/', views.ResourceDetailView.as_view(), name='resource-detail'),

    # Resource Interactions URLs
    path('resource-interactions/', views.ResourceInteractionListCreateView.as_view(), name='resource-interaction-list'),
    path('resource-interactions/<int:pk>/', views.ResourceInteractionDetailView.as_view(), name='resource-interaction-detail'),

    # Notification URLs
    path('notifications/', views.NotificationListCreateView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),

    # Beta Reader Application URLs
    path('beta-reader-applications/', views.BetaReaderApplicationListCreateView.as_view(), name='beta-reader-application-list'),
    path('beta-reader-applications/<int:pk>/', views.BetaReaderApplicationDetailView.as_view(), name='beta-reader-application-detail'),

    # Reader Dashboard URLs
    path('reader-dashboard/', views.reader_dashboard, name='reader-dashboard'),
    path('available-books/', views.available_books, name='available-books'),
    path('reader-feedback/', views.reader_feedback, name='reader-feedback'),
    path('reader-profile/', views.reader_profile, name='reader-profile'),
    path('reader-resource-library/', views.reader_resource_library, name='reader-resource-library'),
    path('beta-reader-training/', views.beta_reader_training, name='beta-reader-training'),
    path('beta-reader-performance-metrics/', views.beta_reader_performance_metrics, name='beta-reader-performance-metrics'),
    path('reader-payment-page/', views.reader_payment_page, name='reader-payment-page'),
    path('reader-settings/', views.reader_settings, name='reader-settings'),

    # Author Dashboard URLs
    path('author-dashboard/', views.author_dashboard, name='author-dashboard'),
    path('my-books/', views.my_books, name='my-books'),
    path('find-beta-readers/', views.find_beta_readers, name='find-beta-readers'),
    path('manuscript-submission/', views.manuscript_submission, name='manuscript-submission'),
    path('feedback-summary/', views.feedback_summary, name='feedback-summary'),
    path('author-resource-library/', views.author_resource_library, name='author-resource-library'),
    path('author-community-groups/', views.author_community_groups, name='author-community-groups'),
    path('author-profile/', views.author_profile, name='author-profile'),
    path('author-payment-page/', views.author_payment_page, name='author-payment-page'),
    path('author-settings/', views.author_settings, name='author-settings'),
]


