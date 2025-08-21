from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Review


def review_list(request):
    reviews = Review.objects.select_related("user", "content_type").order_by("-created")[:100]
    return render(request, "reviews/review_list.html", {"reviews": reviews})


@login_required
def review_create(request):
    if request.method == "POST":
        model_label = request.POST.get("model")  # e.g., "products.Product" or "services.Service"
        object_id = request.POST.get("object_id")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")

        try:
            app_label, model_name = model_label.split(".")
            ct = ContentType.objects.get(app_label=app_label, model=model_name.lower())
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError("Invalid rating range")
            Review.objects.create(
                user=request.user,
                content_type=ct,
                object_id=int(object_id),
                rating=rating_int,
                comment=comment,
                status="pending",
            )
            messages.success(request, "রিভিউ সাবমিট হয়েছে (মডারেশনে আছে)।")
            return redirect("reviews:review_list")
        except Exception as e:
            messages.error(request, f"রিভিউ সাবমিট ব্যর্থ: {e}")

    return render(request, "reviews/review_form.html")

