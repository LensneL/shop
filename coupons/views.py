from django.shortcuts import render, redirect
from .models import Coupon
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_form__lte=now,
                                        valid_form_gte=now,
                                        active=True)
            request.session['coupond_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
