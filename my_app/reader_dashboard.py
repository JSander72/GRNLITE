from django.shortcuts import render, redirect


def reader_dashboard(request):
    # Check user type (assuming you have a way to access it)
    if request.user.profile.user_type != "reader":
        # Redirect to appropriate dashboard (e.g., author dashboard)
        return redirect("author-dashboard")

    # ... Your reader dashboard logic and template rendering code ...
    return render(request, "reader-dashboard.html")
