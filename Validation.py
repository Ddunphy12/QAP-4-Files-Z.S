def ValidateProvince(Province):
    ValidProvinces = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
    return Province in ValidProvinces

def ValidatePaymentMethod(PaymentMethod):
    ValidMethods = ["Full", "Monthly", "Down Pay"]
    return PaymentMethod in ValidMethods

def ValidateYesNo(Value):
    return Value in ["Y", "N"]

def ValidatePositiveNumber(Value):
    try:
        Number = float(Value)
        return Number > 0
    except ValueError:
        return False

def ValidateNotBlank(Value):
    return bool(Value.strip())