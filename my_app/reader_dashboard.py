# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required


# @login_required
# def reader_dashboard(request):
#     # Debug statement to check user authentication status
#     print(f"User authenticated: {request.user.is_authenticated}")

#     # Check user type (assuming you have a way to access it)
#     if request.user.profile.user_type != "reader":
#         # Redirect to appropriate dashboard (e.g., author dashboard)
#         return redirect("author-dashboard")

#     # Debug statement to check user type
#     print(f"User type: {request.user.profile.user_type}")

#     # ... Your reader dashboard logic and template rendering code ...
#     return render(request, "reader-dashboard.html")
