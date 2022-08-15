from .models import User, Inventory, Transactions, Employee
import json
import datetime

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


def login_api_helper(request):

    data = json.loads(request.body)



    username = data.get("username", "")
    password = data.get("password", "")

    if username == "" or password == "":
        return {"success": False, "message": "Username or password cannot be empty"}

    users = User.objects.filter(username=username)

    if len(users) == 0:
        context = {"success": False, "message": "Username does not exists"}
        return context
    stored_password = ""
    for user in users:
        stored_password = user.password
        break

    if stored_password == password:
        context = {"success": True, "message": "ok"}
    else:
        context = {"success": False, "message": "Password does not match, try again"}
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
    data = Transactions.objects.filter(status="open").values()
    return list(data)


def add_transaction(request):
    name = request.POST.get("name", "")
    item = request.POST.get("item", "")
    part_number = request.POST.get("part_number", "")
    quantity = request.POST.get("quantity", "")

    # print("got request, ", request.POST)

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
            # print("Got 0 results for item - {} with part number - {} in inventory".format(item, part_number))
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
        # print("Got 0 results for {}".format(item))
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
                # print("Got 0 results for {}".format(item))
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
    # print(data)
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



def get_unique_part_number_based_on_items(item):
    data = Inventory.objects.filter(name__iexact=item).values('part_number').distinct()
    return list(data)

def get_item_names_wise_data():
    items = get_unique_inventory()
    data = {}
    for item in items:
        it = item['name']
        data[it] = get_unique_part_number_based_on_items(it)
        # print(part_number)
    # print(data)
    return data

def get_all_employees_names():
    data = list(Employee.objects.values('name').distinct())
    data = [x['name'] for x in data]
    # print(data)
    return data


def dashboard_api_helper():
    names = get_unique_inventory()
    unique_part_names = get_unique_part_numbers()
    groups = get_item_names_wise_data()
    # print(groups)
    default_item_name = names[0]['name']
    # print("groups:", json.dumps(groups))
    default_options = groups[default_item_name]
    context = {"names": names, 'part_numbers': unique_part_names,
               'groups': groups, 'default_item_name': default_item_name, 'default_item_name': default_item_name}
    context['data'] = get_all_transactions()
    for d in context['data']:
        create_date = d['created_at'].replace(tzinfo=None)
        diff = (datetime.datetime.today().replace(tzinfo=None) - create_date).days
        d['days'] = diff

    # print(context['data'])

    context['employees'] = get_all_employees_names()
    # print(context)
    return context



def add_inventory_api_helper(request):
    data = json.loads(request.body)

    name = data.get("name", "")
    part_number = data.get("part_number", "")
    quantity = data.get("quantity", "")
    comment = data.get("comment", "")

    if name == "" or part_number == "" or quantity == "":
        return {"success": False, "message": "name or part_number or quantity cannot be empty"}

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
        context = {"success": True, "display_message": True, "message": "Successfully added"}
    except Exception as e:
        context = {"success": False, "display_message": True, "message": str(e)}

    return context




def add_employee_api_helper(request):
    data = json.loads(request.body)

    name = data.get("name", "")
    email = data.get("email", "")
    mobile = data.get("mobile", "")
    comment = data.get("comment", "")

    if name == "" or email == "" or mobile == "":
        return {"success": False, "message": "name or mobile or email cannot be empty"}

    e = Employee()
    e.name = name
    e.mobile = mobile
    e.email = email
    e.comment = "created"

    try:
        e.save()
        return {"success": True, "message": "ok"}
    except Exception as e:
        return {"success": True, "message": str(e)}



def available_quantity_api_helper(request):
    data = json.loads(request.body)

    name = data.get("name", "")
    part_number = data.get("part_number", "")

    if name == "" or part_number == ""  :
        return {"success": False, "message": "name or part_number cannot be empty"}

    all = Inventory.objects.filter(name__iexact=name).filter(part_number__iexact=part_number)

    if len(all) == 0:
        return {"success": False, "message": "does not exist"}

    for a in all:
        current_quantity = a.current_quantity
        return {"success": True, "message": "ok", "quantity": current_quantity}



def add_transaction_api_helper(request):
    data = json.loads(request.body)

    name = data.get("name", "")
    part_number = data.get("part_number", "")
    quantity = data.get("quantity", "")
    item = data.get("item", "")

    if name == "" or quantity == "" or item == "" or part_number == "":
        return {"success": False, "display_message": True,
                "message": "name or quantity or item or part number cannot be empty"}

    ## check if transaction already exists
    tr = Transactions.objects.filter(name__iexact=name).filter(inventory__iexact=item).filter(
                 part_number__iexact=part_number).filter(status__iexact='open')

    if len(tr) > 0:
        for t in tr:
            t.quantity = float(t.quantity) + float(quantity)
            try:
                t.save()
                return  {"success": True, "display_message": True, "message": "Item added"}
            except Exception as e:
                return {"success": False, "message": str(e)}


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
            # print("Got 0 results for item - {} with part number - {} in inventory".format(item, part_number))
            return {"success": True, "display_message": True, "message": "Item added"}

        for i in inv:
            i.current_quantity = float(i.current_quantity) - float(quantity)
            i.save()
            return {"success": True, "display_message": True, "message": "Item added"}

    except Exception as e:
        return {"success": False, "display_message": True, "message": str(e)}




def inventory_api_helper(request):
    data = Inventory.objects.all().values()
    context = {
        'success': True,
        'data': list(data)
    }
    return context


def add_or_remove_quantity_to_inventory(quantity, item, part_number, add=True):
    inv = Inventory.objects.filter(name__iexact=item).filter(part_number__iexact=part_number)
    if len(inv) == 0:
        # print("Got 0 results for {}".format(item))
        return {"success": False,  "message": "Items: {}, {} foes not exist".format(item, part_number)}

    try:
        for i in inv:
            if add:
                i.current_quantity = float(i.current_quantity) + float(quantity)
            else:
                i.current_non_working_quantity = float(i.current_non_working_quantity) + float(quantity)
            i.save()

        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}


def return_inventory_api_helper(request):
    data = json.loads(request.body)

    name = data.get("name", "")
    part_number = data.get("part_number", "")
    quantity = data.get("quantity", "")
    item = data.get("item", "")
    not_working = data.get("not_working", '')
    if str(not_working).lower() == 'true':
        not_working = True
    else:
        not_working = False
    if name == "" or quantity == "" or item == "" or part_number == "":
        return {"success": False, "display_message": True,
                "message": "name or quantity or item or part number cannot be empty"}
    tr = Transactions.objects.filter(name__iexact=name).filter(inventory__iexact=item).filter(part_number__iexact=part_number).filter(status__iexact="open")
    if len(tr) == 0:
        return {"success": False, "display_message": True, "message": "Nothing found with {} and {}".format(name, item)}
    print("length", len(tr))
    for t in tr:
        tr_quantity = t.quantity
        if not_working:
            if float(quantity) <= float(tr_quantity):
                result = add_or_remove_quantity_to_inventory(quantity, item, part_number, False)
                if not result['success']:
                    return result

                if float(quantity) == float(tr_quantity):
                    t.quantity = 0
                    t.status = 'closed'
                    t.return_status = 'damaged'
                    t.closed_at = datetime.datetime.now()
                    try:
                        t.save()
                        return {"success": True, "message": 'ok'}
                    except Exception as e:
                        return {"success": True, "message": str(e)}

                t.quantity = float(t.quantity) - float(quantity)
                t.return_status = 'damaged'
                t.closed_at = datetime.datetime.now()
                try:
                    t.save()
                    return {"success": True, "message": 'ok'}
                except Exception as e:
                    return {"success": True, "message": str(e)}
        else:
            if float(quantity) <= float(tr_quantity):
                print("quantities: ", tr_quantity, quantity)
                result = add_or_remove_quantity_to_inventory(quantity, item, part_number)
                if not result['success']:
                    return result
                if float(quantity) == float(tr_quantity):
                    t.quantity = 0
                    t.return_status = 'ok'
                    t.status = 'closed'
                    t.closed_at = datetime.datetime.now()
                    # print(t)
                    print("closing now", t.status)
                    print(t.created_at)
                    try:
                        t.save()
                        print("save success")
                        print(t.values())
                        return {"success": True, "message": 'ok'}
                    except Exception as e:
                        return {"success": True, "message": str(e)}

                t.quantity = float(t.quantity) - float(quantity)
                t.return_status = 'ok'
                t.closed_at = datetime.datetime.now()

                try:
                    t.save()
                    return {"success": True, "message": 'ok'}
                except Exception as e:
                    return {"success": True, "message": str(e)}

    return {"success": False, "message": "something went wrong"}
