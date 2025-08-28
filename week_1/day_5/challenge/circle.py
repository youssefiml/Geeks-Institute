import math

class Circle:
    def __init__(self, radius = None, diameter = None):
        if radius is None and diameter is None:
            raise ValueError("You must provide either radius or diameter")
        if radius is not None:
            self.radius = radius
        else:
            self.radius = diameter / 2
    
    @property
    def diameter(self):
        return self.radius *2
    
    @property
    def area(self):
        return math.pi ** (self.radius ** 2)
    
    def __str__(self):
        return f"Circle with radius {self.radius} and diameter {self.diameter}"
    
    def __add__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return Circle(radius = self.radius + other.radius)
    
    def __eq__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius
    
    def __lt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius
    
    def __gt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius
    
c1 = Circle(radius=4)
c2 = Circle(diameter=10)

print(c1)
print(c2)

c3 = c1 + c2
print(c3)

print(c1 == c2)
print(c1 < c2)
print(c1 > c2)

circles = [c1, c2, c3]
sorted_circles = sorted(circles)
for c in sorted_circles:
    print(c)