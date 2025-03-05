def createHearts(text):
    heart_forms = [
        "  ****   ****  ",
        " ****** ****** ",
        "***************",
        " ************* ",
        "  ***********  ",
        "   *********   ",
        "    *******    ",
        "     *****     ",
        "      ***      ",
        "       *       "
    ]
    heart = []
    for line in heart_forms:
        heart_line = ""
        for char in line:
            if char == "*":
                heart_line += text
            else:
                heart_line += " "
        heart.append(heart_line)
    return "\n".join(heart)
bestGirlName = "ника"
heart = createHearts(bestGirlName)
print(heart)