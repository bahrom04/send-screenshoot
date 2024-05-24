text = 'confirm_11077504_vip'

filtered = text.split("_")

print(filtered)

if user_id == admin_id and callback_data.startswith("confirm_"):
    u = User.objects.get(user_id=filtered[1], cources=filtered[2], is_payed=True)

