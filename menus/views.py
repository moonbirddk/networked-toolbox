from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from .models import MenuItem

@login_required
@permission_required('is_staff')
def edit_menus(request):
    menus = []
    for menu, label in MenuItem.MENU_CHOICES:
        menus.append({
            'label': label,
            'items': MenuItem.objects.filter(menu=menu).order_by('order')
        })
    context = {
        'menus': menus
    }
    print('context', context)
    return render(request, 'menus/edit_menus.html', context)
