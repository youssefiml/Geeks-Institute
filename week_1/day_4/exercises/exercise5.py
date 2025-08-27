from exercise4_Family import Family

class TheIncredibles(Family):
    def use_power(self, name):
        for member in initial_members:
            if member.get("name") == name:
                age = member.get("age", 0)
                if age >= 18:
                    print(member.get(["power"]))
                    return
                else:
                    print((f"{name} is not over 18 years old!"))
        print("Violet is not over 18")
        
    def incredible_presentation(self):
        print("Here is our powerful family : ")
        super().family_presentation()
        
initial_members = {
    "Bob": {"age": 44, "gender": "Male", "power": "super strength", "incredible_name": "Mr. Incredible"},
    "Helen": {"age": 41, "gender": "Female", "power": "elasticity", "incredible_name": "Elastigirl"},
    "Violet": {"age": 16, "gender": "Female", "power": "invisibility", "incredible_name": "Violet"},
    "Dash": {"age": 10, "gender": "Male", "power": "super speed", "incredible_name": "Dash"}
}


incredibles = TheIncredibles("The incredibles", initial_members)
incredibles.incredible_presentation()
incredibles.born(
    name="Baby Jack",
    age=0,
    gender="Male",
    power="Unknown Power",
    incredible_name="Baby Jack"
)
incredibles.incredible_presentation()