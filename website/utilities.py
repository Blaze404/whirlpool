from .models import User, Inventory, Transactions


def create_user_helper(request):
    phone = request.POST.get("phone", "")
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    if phone == "" or username == "" or password == "":
        context = {"success": False, "message": "Username or password or phone is empty", "display_message": True}
        return context
    qs = User.objects.filter(username=username)
    if len(qs) >= 1:
        context = {"success": False, "message": "Username already taken try different", "display_message": True}
        return context
    user = User()
    user.username = username
    user.password = password
    user.phone = phone
    user.user_type = "admin"
    user.created_by = "admin"
    try:
        user.save()
        context = {"success": True, "message": "ok", "display_message": True}
    except Exception as e:
        context = {"success": False, "message": str(e), "display_message": True}
    return context


def login_helper(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    users = User.objects.filter(username=username)

    if len(users) == 0:
        context = {"success": False, "message": "Username does not exists", "display_message": True}
        return context
    stored_password = ""
    for user in users:
        stored_password = user.password
        break

    if stored_password == password:
        context = {"success": True, "message": "ok"}
    else:
        context = {"success": False, "message": "Password does not match, try again", "display_message": True}
    return context


def add_inventory(request):
    name = request.POST.get("name", "")
    part_number = request.POST.get('part_number', "")
    quantity = request.POST.get("quantity", "")
    comment = request.POST.get("comment", "")

    if name == "" or quantity == "" or part_number == "":
        return { "success": False, "display_message": True, "message": "name, quantity, or part number cannot be empty" }

    ## check if that name already there
    inventory = Inventory.objects.filter(name__iexact=name).filter(part_number__iexact=part_number)

    if len(inventory) >= 1:
        ## found an inventory with given name
        for inve in inventory:
            inve.quantity = float(inve.quantity) + float(quantity)
            inve.current_quantity = float(inve.current_quantity) + float(quantity)
            try:
                inve.save()
                context = {"success": True, "display_message": True, "message": "Successfully added"}
            except Exception as e:
                context = {"success": False, "display_message": True, "message": str(e)}
            return context


    inv = Inventory()

    inv.name = name
    inv.quantity = quantity
    inv.current_quantity = quantity
    inv.description = comment
    inv.part_number = part_number

    try:
        inv.save()
        context = { "success": True, "display_message": True, "message": "Successfully added" }
    except Exception as e:
        context = { "success": False, "display_message": True, "message": str(e)}

    return context


def remove_inventory(request):
    name = request.POST.get("name", "")
    quantity = request.POST.get("quantity", "")
    comment = request.POST.get("comment", "")

    if name == "" or quantity == "":
        return {"success": False, "display_message": True, "message": "name or quantity cannot be empty"}

    inventory = Inventory.objects.filter(name__iexact=name)

    if len(inventory) == 0:
        return {"success": False, "display_message": True, "message": "You done have anything with name {}".format(name)}

    for inv in inventory:
        total_quantity = float(inv.quantity)
        if float(quantity) > total_quantity:
            return {"success": False, "display_message": True, "message": "{} only have {} available quantity".format(name, total_quantity)}

        if float(quantity) == total_quantity:
            inventory_id = inv.inventory_id
            Inventory.objects.filter(inventory_id=inventory_id).delete()
            return {"success": True, "display_message": True, "message": "Successfully deleted {}".format(name)}

        inv.quantity = float(inv.quantity) - float(quantity)
        inv.current_quantity = float(inv.current_quantity) - float(quantity)

        try:
            inv.save()
            return {"success": True, "display_message": True, "message": "Successfully reduced quantity of {}".format(name)}
        except Exception as e:
            return  { "success": False, "display_message": True, "message": str(e)}

def get_inventory():
    data = Inventory.objects.all()
    return data


def get_unique_inventory():
    data = Inventory.objects.values('name').distinct()
    return list(data)



def get_all_transactions():
    data = Transactions.objects.filter(status="open")
    return data


def add_transaction(request):
    name = request.POST.get("name", "")
    item = request.POST.get("item", "")
    part_number = request.POST.get("part_number", "")
    quantity = request.POST.get("quantity", "")

    print("got request, ", request.POST)

    if name == "" or quantity == "" or item == "" or part_number:
        return {"success": False, "display_message": True, "message": "name or quantity or item or part number cannot be empty"}

    tr = Transactions()

    tr.created_by = "admin"
    tr.name = name
    tr.inventory = item
    tr.quantity = quantity
    tr.status = "open"
    tr.part_number = part_number


    try:
        tr.save()
        context = {"success": True, "display_message": True, "message": "Item added"}
        ## reduce current quantity
        inv = Inventory.objects.filter(part_number__iexact=part_number).filter(name__iexact=item)

        if len(inv) == 0:
            print("Got 0 results for item - {} with part number - {} in inventory".format(item, part_number))
            return {"success": True, "display_message": True, "message": "Item added"}


        for i in inv:
            i.current_quantity = float(i.current_quantity) - float(quantity)
            i.save()
            return {"success": True, "display_message": True, "message": "Item added"}

    except Exception as e:
        return {"success": False, "display_message": True, "message": str(e)}


def delete_transactions():
    Transactions.objects.all().delete()


def add_quantity_to_inventory(quantity, item):
    inv = Inventory.objects.filter(name__iexact=item)
    if len(inv) == 0:
        print("Got 0 results for {}".format(item))
        return {"success": True, "display_message": True, "message": "Item added"}

    for i in inv:
        i.current_quantity = float(i.current_quantity) + float(quantity)
        i.save()


def return_inventory(request):
    name = request.POST.get("name", "")
    item = request.POST.get("item", "")
    quantity = request.POST.get("quantity", "")

    if name == "" or quantity == "" or item == "":
        return {"success": False, "display_message": True, "message": "name or quantity or item cannot be empty"}


    tr = Transactions.objects.filter(name__iexact=name).filter(inventory__iexact=item)

    if len(tr) == 0:
        return {"success": False, "display_message": True, "message": "Nothing found with {} and {}".format(name, item)}

    for t in tr:
        tr_item = t.inventory
        if float(t.quantity) <= float(quantity):
            # he returned all
            id = t.transaction_id
            Transactions.objects.filter(transaction_id=id).delete()
            try:
                add_quantity_to_inventory(quantity, item)
            except Exception as e:
                return {"success": True, "display_message": True, "message": str(e)}
            return {"success": True, "display_message": True,
                    "message": "Deleted transaction successfully"}
        t.quantity = float(t.quantity) - float(quantity)
        try:
            t.save()

            ## edit inventory
            inv = Inventory.objects.filter(name__iexact=item)

            if len(inv) == 0:
                print("Got 0 results for {}".format(item))
                return {"success": True, "display_message": True, "message": "Item added"}

            for i in inv:
                i.current_quantity = float(i.current_quantity) + float(quantity)
                i.save()
                return {"success": True, "display_message": True, "message": "Item added"}

        except Exception as e:
            return {"success": False, "display_message": True, "message": str(e)}


def show_all_users_helper():
    return {'data': list(User.objects.all().values())}


def get_unique_inventory_based_on_part_number(part_number):
    data = Inventory.objects.filter(part_number__iexact=part_number).values('name').distinct()
    return list(data)

def get_unique_part_numbers():
    data = Inventory.objects.values('part_number').distinct()
    return list(data)

def get_part_numbers_wise_data():
    part_numbers = get_unique_part_numbers()
    data = {}
    for part_number in part_numbers:
        pn = part_number['part_number']
        data[pn] = get_unique_inventory_based_on_part_number(pn)
        # print(part_number)
    print(data)
    return data


def get_dashboard_context():
    names = get_unique_inventory()
    unique_part_names = get_unique_part_numbers()
    groups = get_part_numbers_wise_data()
    # print(groups)
    default_part_number = unique_part_names[0]['part_number']
    # print("groups:", json.dumps(groups))
    default_options = groups[default_part_number]
    context = {"names": names, 'part_numbers': unique_part_names,
               'groups': groups, 'default_part_number': default_part_number
        , 'default_options': default_options}
    context['data'] = get_all_transactions()
    return context