from django.shortcuts import render, redirect


def author_dashboard(request):
    # Check user type (assuming you have a way to access it)
    if request.user.profile.user_type != "author":
        # Redirect to appropriate dashboard (e.g., reader dashboard)
        return redirect("reader-dashboard")

    # ... Your author dashboard logic and template rendering code ...
    return render(request, "author-dashboard.html")
