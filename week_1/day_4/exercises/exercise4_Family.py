class Family:
    def __init__(self, last_name, members=None):
        self.last_name = last_name
        self.members = members if members else {}

    def born(self, **kwargs):
        name = kwargs["name"]
        self.members[name] = {
            "age": kwargs["age"],
            "gender": kwargs["gender"]
        }
        print(f"Congratulations to the {self.last_name} family! A new child is born: {name}")

    def is_18(self, name):
        if name in self.members:
            return self.members[name]["age"] >= 18
        return False

    def family_presentation(self):
        print(f"Family name is : {self.last_name}")
        print("the members are : ")
        for name, info in self.members.items():
            print(f"{name}, {info["age"]} years old, {info["gender"]}")
            

family = Family("Smith", {
    "John": {"age": 35, "gender": "Male"},
    "Jane": {"age": 34, "gender": "Female"},
    "Tom": {"age": 10, "gender": "Male"}
})

print(family.is_18("John"))
family.born(name="Anna", age=0, gender="Female")
family.family_presentation()
