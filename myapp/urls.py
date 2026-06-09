from django.urls import path
from .views import (
    signup,
    login,
    forgot_password,
    reset_password,
    analyze_code,
   
    ai_chat,
    practice_question,
    test_mode,
    evaluate_answer,
    generate_test,
    run_code,
    get_profile,
    update_profile,
    user_data,
    delete_history,


)

urlpatterns = [

    # AUTH
    path('signup/', signup),
    path('login/', login),

    path('forgot-password/', forgot_password),
    path('reset-password/', reset_password),

    # CODE
    path('analyze/', analyze_code),
    path('run/', run_code),

    # AI
    path('chat/', ai_chat),

    # PRACTICE
    path('practice/', practice_question),
    path('test/', test_mode),
    path('evaluate/', evaluate_answer),
    path('generate-test/', generate_test),

    # HISTORY
   
    # path('api/history/', views.get_history),
    # path('api/history/clear/', views.clear_history),        # ← pehle
    # path('api/history/<int:pk>/delete/', views.delete_history),  # ← baad mein
    # PROFILE
    path('profile/', get_profile),
    path('profile/update/', update_profile),
    path('user/', user_data),
    
]




# from django.urls import path
# from .views import (
#     signup,
#     login,
#     forgot_password,
#     reset_password,
#     analyze_code,
#     ai_chat,
#     practice_question,
#     test_mode,
#     evaluate_answer,
#     generate_test,
#     run_code,
#     get_profile,
#     update_profile,
#     user_data,
#     get_history,       # ← add karo
#     delete_history,
#     clear_history,     # ← add karo
# )

# urlpatterns = [

#     # AUTH
#     path('signup/', signup),
#     path('login/', login),
#     path('forgot-password/', forgot_password),
#     path('reset-password/', reset_password),

#     # CODE
#     path('analyze/', analyze_code),
#     path('run/', run_code),

#     # AI
#     path('chat/', ai_chat),

#     # PRACTICE
#     path('practice/', practice_question),
#     path('test/', test_mode),
#     path('evaluate/', evaluate_answer),
#     path('generate-test/', generate_test),

#     # HISTORY
#     path('history/', get_history),
#     path('history/clear/', clear_history),
#     path('history/<int:pk>/delete/', delete_history),

#     # PROFILE
#     path('profile/', get_profile),
#     path('profile/update/', update_profile),
#     path('user/', user_data),
# ]