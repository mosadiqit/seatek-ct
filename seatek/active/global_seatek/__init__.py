num = {
    "0": "không",
    "1": "một",
    "2": "hai",
    "3": "ba",
    "4": "bốn",
    "5": "năm",
    "6": "sáu",
    "7": "bảy",
    "8": "tám",
    "9": "chín",
}
ten = {
    "00": "không mươi",
    "01": "lẻ một",
    "02": "lẻ hai",
    "03": "lẻ ba",
    "04": "lẻ bốn",
    "05": "lẻ lăm",
    "06": "lẻ sáu",
    "07": "lẻ bảy",
    "08": "lẻ tám",
    "09": "lẻ chín",
    "10": "mười",
    "11": "mười một",
    "12": "mười hai",
    "13": "mười ba",
    "14": "mười bốn",
    "15": "mười lăm",
    "16": "mười sáu",
    "17": "mười bảy",
    "18": "mười tám",
    "19": "mười chín"
}

greaters = {
    2: "nghìn",
    3: "triệu",
    4: "tỷ",
}


def readGreater(l):
    x = l
    if x <= 3:
        return 0, ""
    # elif x == 2:
    #     return "mươi"
    # elif x == 3:
    #     return "trăm"
    m = 0
    while x > 3:
        m = x % 3
        x = x // 3
        if x == 4:
            break

    if x != 4 and m > 0:
        x += 1
    return x, greaters[x]


def read3Num(s):
    if s == "000":
        return num["0"]
    l = len(s)
    if l == 0:
        return ""
    elif l == 1:
        return num[s]
    elif l == 2:
        if int(s) < 20:
            return ten[s]
        else:
            x = "mươi"
            if s[1] != "0":
                x += " " + num[s[1]]
            return num[s[0]] + " " + x
    else:
        x = num[s[0]] + " trăm"
        s1 = s[1] + s[2]
        if s1 == "00":
            return x
        x += " " + read3Num(s[1] + s[2])
        return x


def readFreeNum(x):
    isNegative = False
    if x < 0:
        isNegative = True
        x = x * -1
    s = str(x)
    l = len(s)
    mod = l % 3
    count = l // 3
    kq = ""
    if isNegative:
        kq = "Âm"
    if mod == 1:
        x, greater = readGreater(l)
        num3 = num[s[0]]
        kq += " " + num3 + " " + greater
    elif mod == 2:
        x, greater = readGreater(l)
        num3 = read3Num(s[0] + s[1])
        kq += " " + num3 + " " + greater

    l = l - mod
    s = s[mod:]
    if mod > 0 and s.replace('0', '') == "":
        return kq
    for c in range(0, count):
        s1 = s[0]
        s2 = s[1]
        s3 = s[2]
        x, greater = readGreater(l)
        num3 = read3Num(s1 + s2 + s3)
        if x == 4 and num3 == num["0"]:
            kq += " " + greater
        else:
            kq += " " + num3 + " " + greater
        l -= 3
        s = s[3:]
        if l > 0 and s.replace('0', '') == "":
            return kq
    return kq


def format_number(num):
    num = float('{0:.3f}'.format(num))
    negative = -1
    if num >= 0:
        negative *= -1
    number_dec = str(num*negative - int(num))[2:]
    if int(number_dec[:3]) > 0:
        return '{0:,}'.format(num)
    else:
        return '{0:,}'.format(int(num))


class Seatek(object):

    @staticmethod
    def formatNum(num):
        return format_number(num)

    @staticmethod
    def readNum(num):
        return readFreeNum(int(num))
