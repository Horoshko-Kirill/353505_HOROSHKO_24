import json
import os
from geometric_lib import circle, square

def main():
   
    env_data = os.getenv("SHAPE_JSON")

    if env_data:
        data = json.loads(env_data)

    shape = data.get("shape")
    size = data.get("size")

    if shape == "circle":
        area = circle.area(size)
        perimeter = circle.perimeter(size)
    elif shape == "square":
        area = square.area(size)
        perimeter = square.perimeter(size)
    else:
        print("Ошибка: неизвестная фигура")
        return

    print(f"Фигура: {shape}")
    print(f"Площадь: {area:.2f}")
    print(f"Периметр: {perimeter:.2f}")

if __name__ == "__main__":
    main()
