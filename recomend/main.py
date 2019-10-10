from review import Review
import sys


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("ERROR:: Please set URL on arg1")
        exit()
    url = sys.argv[1]

    header = {"User-Agent": "test"}

    if len(sys.argv) < 2:
        star_filter = 4.0
    star_filter = float(sys.argv[2])

    model = Review(url, header, star_filter)
    model.get_star()
    print("---SUCCESS----")