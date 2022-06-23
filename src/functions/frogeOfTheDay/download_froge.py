import requests

for i in range(1, 54):
    print(f"{i:004.0f}")
    data = requests.get(f"http://www.allaboutfrogs.org/funstuff/random/{i:004.0f}.jpg")
    if data.content:
        with open(f"{i:004.0f}.jpg", "wb") as f:
            print(f"Saving image {i:004.0f}.jpg")
            f.write(data.content)
