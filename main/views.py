import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .models import LikedListing, Listing, ChatQA
from .forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter

# ----------------------
# Main / Home Views
# ----------------------
def main_view(request):
    return render(request, "views/main.html", {"name": "Automax"})


def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(
        profile=request.user.profile
    ).values_list('listing', flat=True)

    context = {
        'listing_filter': listing_filter,
        'liked_listings_ids': list(user_liked_listings),
    }
    return render(request, "views/home.html", context)


# ----------------------
# Listing Views
# ----------------------
@login_required
def list_view(request):
    if request.method == 'POST':
        listing_form = ListingForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)
        if listing_form.is_valid() and location_form.is_valid():
            listing = listing_form.save(commit=False)
            listing_location = location_form.save()
            listing.seller = request.user.profile
            listing.location = listing_location
            listing.save()
            messages.info(request, f'{listing.model} Listing Posted Successfully!')
            return redirect('home')
        messages.error(request, 'An error occurred while posting the listing.')
    else:
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html', {
        'listing_form': listing_form,
        'location_form': location_form,
    })


@login_required
def listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    return render(request, 'views/listing.html', {'listing': listing})


@login_required
def edit_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.method == 'POST':
        listing_form = ListingForm(request.POST, request.FILES, instance=listing)
        location_form = LocationForm(request.POST, instance=listing.location)
        if listing_form.is_valid() and location_form.is_valid():
            listing_form.save()
            location_form.save()
            messages.info(request, f'Listing {id} updated successfully!')
            return redirect('home')
        messages.error(request, f'Error updating listing {id}.')
    else:
        listing_form = ListingForm(instance=listing)
        location_form = LocationForm(instance=listing.location)

    context = {'listing_form': listing_form, 'location_form': location_form}
    return render(request, 'views/edit.html', context)


@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    liked_listing, created = LikedListing.objects.get_or_create(
        profile=request.user.profile, listing=listing
    )
    if not created:
        liked_listing.delete()
    return JsonResponse({'is_liked_by_user': created})


@login_required
def inquire_listing_using_email(request, id):
    listing = get_object_or_404(Listing, id=id)
    try:
        subject = f'{request.user.username} is interested in {listing.model}'
        message = f'Hi {listing.seller.user.username}, {request.user.username} is interested in your {listing.model} listing on AutoMax'
        send_mail(subject, message, 'noreply@automax.com', [listing.seller.user.email], fail_silently=True)
        return JsonResponse({"success": True})
    except Exception as e:
        print(e)
        return JsonResponse({"success": False, "info": str(e)})


# ----------------------
# Chatbot View (ML-Free)
# ----------------------
@csrf_exempt
def chatbot_reply(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request method."})

    try:
        data = json.loads(request.body.decode('utf-8'))
        user_msg = data.get("message", "").strip().lower()
        response = "Sorry, I couldn't understand that. Can you rephrase?"

        qa_pairs = ChatQA.objects.all()

        for qa in qa_pairs:
            question_keywords = qa.question.lower().split()
            if any(word in user_msg for word in question_keywords):
                response = qa.answer
                break

        return JsonResponse({"reply": response})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"reply": "Error processing message.", "error": str(e)})