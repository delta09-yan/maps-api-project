def coord_to_spn(coord):
    x1, y1, x2, y2 = [float(n) for n in coord['lowerCorner'].split() + coord['upperCorner'].split()]
    return round(max(abs(x1 - x2), abs(y1 - y2)), str(abs(x1 - x2)).count('0') + 1)


if __name__ == '__main__':
    coords = {'lowerCorner': '-122.091252 '
                             '37.278595',
              'upperCorner': '-121.995941 '
                             '37.340088'}
    print(coord_to_spn(coords))
