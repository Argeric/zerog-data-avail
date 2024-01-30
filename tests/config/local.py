#!/usr/bin/python3

class DAEncoder:
    def __init__(self):
        self.name = 'DAEncoder'


class DABatcher:
    def __init__(self, name):
        self.name = name


class DAServer:
    def __init__(self):
        self.name = 'DAServer'


da_services = []


def run():
    classes = [DAEncoder, DABatcher, DAServer]
    for Clazz in classes:
        if Clazz == DABatcher:
            print("here1")
            service = Clazz('DABatcher')
        else:
            print("here2")
            service = Clazz()
        print(f"class {service.__class__}")
        da_services.append(service)
    print(f"len {len(da_services)}")


if __name__ == "__main__":
    run()
