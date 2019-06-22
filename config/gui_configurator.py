import json
from browser import document, alert
'''
Graphical editor for the config file of the anonymizer
Start the web application using a webserver
'''

__author__ = "Samuele Pozzani"
__version__ = "1.0"

# Libraries


configuration = {}
selected_profile = ""


def load_configuration(filename):
    try:
        with open(filename, "r") as filein:
            global configuration, profile
            configuration = json.loads(filein.read())
            profile = configuration["selected_profile"]
    except Exception as e:
        alert("Error occured: " + str(e))


def save_configuration(filename):
    try:
        with open(filename, "w") as fileout:
            global configuration
            fileout.write(json.dump(configuration))
    except Exception as e:
        alert("Error occured: " + str(e))


def change_profile(ev):
    global selected_profile
    profile_selector = document.select("#profile")
    selected_profile = profile_selector[0].value
    if selected_profile != "":
        draw_fields()
    else:
        clean_fields()


def draw_fields():
    fields_list = document.createElement('ul')
    fields_list.classList.add("mdl-list")
    fields_list.classList.add("flist")
    page = document.select(".fields-container")
    page[0].appendChild(fields_list)
    n = 0
    for field in list(configuration["profiles"][selected_profile]["fields_list"]):
        element = document.createElement("li")
        element.classList.add("mdl-list__item")
        text_field = create_input_field(field, n)
        element.appendChild(text_field)
        fields_list.appendChild(element)
        n += 1
    add_field = document.createElement('button')
    add_field.classList.add("mdl-button", "mdl-js-button",
                            "mdl-button--fab", "add-button")
    content = document.createElement("i")
    content <= "+"
    add_field.appendChild(content)
    page[0].appendChild(add_field)


def clean_fields():
    fields_list = document.select('.flist')
    fields_list[0].remove()
    add_button = document.select('.add-button')
    add_button[0].remove()


def create_input_field(name, n):
    div = document.createElement("div")
    div.classList.add("mdl-textfield", "mdl-js-textfield")
    input_field = document.createElement("input")
    input_field.classList.add("mdl-textfield__input", "field-input", str(n))
    input_field.attrs["placeholder"] = "Field name..."
    input_field.value = name
    input_field.bind("change", change_field_name)
    div.appendChild(input_field)
    return div


def change_field_name(ev):
    global selected_profile, configuration
    old_value = configuration["profiles"][selected_profile]["fields_list"][int(ev.target.classList[2])]
    if ev.target.value == "":
        ev.target.value = old_value
        return
    configuration["profiles"][selected_profile]["fields"][ev.target.value] = configuration["profiles"][selected_profile]["fields"].pop(
        old_value
    )
    configuration["profiles"][selected_profile]["fields_list"][int(ev.target.classList[2])] = ev.target.value
    change_field_dependencies(configuration["profiles"][selected_profile]["fields"], old_value, ev.target.value)
    print(configuration["profiles"][selected_profile]["fields"])


def change_field_dependencies(position, old_value, new_value):
    if type(position) == list:
        for item in position:
            change_field_dependencies(item, old_value, new_value)
    elif type(position) == dict:
        for item in position.values():
            change_field_dependencies(item, old_value, new_value)
    else:
        position = position.replace(old_value, new_value)


def main():

    global configuration, selected_profile
    load_configuration("config.json")

    # Profile selector
    profile_selector = document.select("#profile")
    profile_selector[0].appendChild(document.createElement("option"))
    for profile in list(configuration["profiles"].keys())[1:]:
        option = document.createElement("option")
        option.value = profile
        option.innerHTML = profile
        profile_selector[0].appendChild(option)
    profile_selector[0].bind("change", change_profile)


if __name__ == "__main__":
    main()
