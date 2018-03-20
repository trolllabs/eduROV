from pkg_resources import Requirement, resource_filename


def print_me():
    filename = resource_filename(Requirement.parse("edurov"),
                                 "examples_edurov/entry_points.py")
    print(filename)
