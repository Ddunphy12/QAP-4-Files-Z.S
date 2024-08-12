# Zackery Strickland
# Date: Mon, Jul 29
# One Stop Insurance QAP 4

# Imports
import datetime
import Validation

# Functions
def ReadConstants():
    with open('Const.dat', 'r') as file:
        Constants = [line.strip() for line in file]
    return Constants

def CalculatePremium(NumCars, ExtraLiability, GlassCoverage, LoanerCar, Constants):
    BasicPremium = float(Constants[1])
    Discount = float(Constants[2])
    LiabilityCost = float(Constants[3])
    GlassCost = float(Constants[4])
    LoanerCost = float(Constants[5])
    
    TotalPremium = BasicPremium + (NumCars - 1) * BasicPremium * (1 - Discount)
    ExtraCosts = 0
    if ExtraLiability == 'Y':
        ExtraCosts += NumCars * LiabilityCost
    if GlassCoverage == 'Y':
        ExtraCosts += NumCars * GlassCost
    if LoanerCar == 'Y':
        ExtraCosts += NumCars * LoanerCost
    
    TotalPremium += ExtraCosts
    return TotalPremium, ExtraCosts

def CalculateHst(TotalPremium, Constants):
    HstRate = float(Constants[6])
    Hst = TotalPremium * HstRate
    return Hst

def CalculateMonthlyPayment(TotalCost, DownPayment, Constants):
    ProcessingFee = float(Constants[7])
    if DownPayment > 0:
        MonthlyPayment = (TotalCost - DownPayment + ProcessingFee) / 8
    else:
        MonthlyPayment = (TotalCost + ProcessingFee) / 8
    return MonthlyPayment

def SavePolicyData(Filename, Data):
    with open(Filename, 'a') as file:
        for item in Data:
            file.write(f"{item},")
        file.write("\n")
    print("Saving: Please Stand By")
    for _ in range(3):
        print(".", end="", flush=True)
    print("\nData Saved Successfully.")

def ReadClaims():
    Claims = []
    with open('Claims.dat', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                ClaimNumber, ClaimDate, ClaimAmount = parts
                Claims.append((ClaimNumber, ClaimDate, ClaimAmount))
    return Claims

def GetCustomerInfo():
    while True:
        FirstName = input("Enter first name: ").title()
        if Validation.ValidateNotBlank(FirstName):
            break
        else:
            print("First name cannot be blank.")
    
    while True:
        LastName = input("Enter last name: ").title()
        if Validation.ValidateNotBlank(LastName):
            break
        else:
            print("Last name cannot be blank.")
    
    while True:
        Address = input("Enter address: ")
        if Validation.ValidateNotBlank(Address):
            break
        else:
            print("Address cannot be blank.")
    
    while True:
        City = input("Enter city: ").title()
        if Validation.ValidateNotBlank(City):
            break
        else:
            print("City cannot be blank.")
    
    while True:
        Province = input("Enter province: ").upper()
        if Validation.ValidateProvince(Province):
            break
        else:
            print("Invalid province. Please enter a valid province code.")
    
    while True:
        PostalCode = input("Enter postal code: ")
        if Validation.ValidateNotBlank(PostalCode):
            break
        else:
            print("Postal code cannot be blank.")
    
    while True:
        PhoneNumber = input("Enter phone number: ")
        if Validation.ValidateNotBlank(PhoneNumber):
            break
        else:
            print("Phone number cannot be blank.")
    
    while True:
        NumCars = input("Enter number of cars: ")
        if Validation.ValidatePositiveNumber(NumCars):
            NumCars = int(NumCars)
            break
        else:
            print("Number of cars must be a positive number.")
    
    while True:
        ExtraLiability = input("Extra liability (Y/N): ").upper()
        if Validation.ValidateYesNo(ExtraLiability):
            break
        else:
            print("Invalid input. Please enter Y or N.")
    
    while True:
        GlassCoverage = input("Glass coverage (Y/N): ").upper()
        if Validation.ValidateYesNo(GlassCoverage):
            break
        else:
            print("Invalid input. Please enter Y or N.")
    
    while True:
        LoanerCar = input("Loaner car (Y/N): ").upper()
        if Validation.ValidateYesNo(LoanerCar):
            break
        else:
            print("Invalid input. Please enter Y or N.")
    
    while True:
        PaymentMethod = input("Payment method (Full/Monthly/Down Pay): ").title()
        if Validation.ValidatePaymentMethod(PaymentMethod):
            break
        else:
            print("Invalid payment method. Please enter Full, Monthly, or Down Pay.")
    
    if PaymentMethod == "Down Pay":
        while True:
            DownPayment = input("Enter down payment amount: ")
            if Validation.ValidatePositiveNumber(DownPayment):
                DownPayment = float(DownPayment)
                break
            else:
                print("Invalid amount. Please enter a positive number.")
    else:
        DownPayment = 0
    
    return (FirstName, LastName, Address, City, Province, PostalCode, PhoneNumber, NumCars, ExtraLiability, GlassCoverage, LoanerCar, PaymentMethod, DownPayment)

# Input
Constants = ReadConstants()
NextPolicyNumber = int(Constants[0])

while True:
    CustomerInfo = GetCustomerInfo()
    Claims = ReadClaims()
    
    # Calculations
    TotalPremium, ExtraCosts = CalculatePremium(CustomerInfo[7], CustomerInfo[8], CustomerInfo[9], CustomerInfo[10], Constants)
    Hst = CalculateHst(TotalPremium, Constants)
    TotalCost = TotalPremium + Hst
    
    if CustomerInfo[11] == "Monthly" or CustomerInfo[11] == "Down Pay":
        MonthlyPayment = CalculateMonthlyPayment(TotalCost, CustomerInfo[12], Constants)
    else:
        MonthlyPayment = 0
    
    InvoiceDate = datetime.date.today()
    FirstPaymentDate = (InvoiceDate.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
    
    # Output
    print("\n          One Stop Insurance Company")
    print("           Insurance Claim Invoice:")
    print("______________________________________________")
    print()
    print(f"  Invoice Date: {InvoiceDate}   Policy No: {NextPolicyNumber}")
    print()
    print(f"  Customer:")
    print()
    print(f"    {CustomerInfo[0]} {CustomerInfo[1]}")
    print(f"    {CustomerInfo[2]}")
    print(f"    {CustomerInfo[3]} {CustomerInfo[4]} {CustomerInfo[5]}")
    print(f"    {CustomerInfo[6]}")
    print()
    print("----------------------------------------------")
    print()
    print(f"    Number of Cars: {CustomerInfo[7]}")
    print()
    print(f"       Premium:              ${TotalPremium:.2f}")
    if CustomerInfo[8] == "Y":
        print(f"       Extra Liability:      ${CustomerInfo[7] * float(Constants[3]):.2f}")
    if CustomerInfo[9] == "Y":
        print(f"       Glass Coverage:       ${CustomerInfo[7] * float(Constants[4]):.2f}")
    if CustomerInfo[10] == "Y":    
        print(f"       Loaner Car:           ${CustomerInfo[7] * float(Constants[5]):.2f}")
    print(f"       Total Extras:         ${ExtraCosts:.2f}")
    print(f"       Subtotal:             ${TotalPremium:.2f}")
    print(f"       HST:                  ${Hst:.2f}")
    print("                             ----------")
    print(f"       Total Due:            ${TotalCost:.2f}")
    if CustomerInfo[11] == "Monthly" or CustomerInfo[11] == "Down Pay":
        print(f"       Downpayment:          ${CustomerInfo[12]:.2f}")
        print("                             ----------")
        print(f"       Total Due:            ${TotalCost - CustomerInfo[12]:.2f}")
        print()
        print("----------------------------------------------")
        print()
        print(f"  Processing Fee:    ${float(Constants[7]):.2f}  (one time only)")
        print(f"  Monthly Payment:   ${MonthlyPayment:.2f} (for 8 months)")
        print()
        print(f"  First Payment Due: {FirstPaymentDate}")
        print()
    print("----------------------------------------------")
    print()
    print("          One Stop: Look No Further!")
    print()
    print("----------------------------------------------")
    print()
    
    print("  Previous Claims:")
    print("  Claim #  Claim Date   Amount")
    print("  ---------------------------------")
    for claim in Claims:
        print(f"  {claim[0]}    {claim[1]}    ${float(claim[2]):,.2f}")
    
    # Save policy data
    PolicyData = [NextPolicyNumber, CustomerInfo[0], CustomerInfo[1], CustomerInfo[2], CustomerInfo[3], CustomerInfo[4], CustomerInfo[5], CustomerInfo[6], CustomerInfo[7], CustomerInfo[8], CustomerInfo[9], CustomerInfo[10], CustomerInfo[11], CustomerInfo[12], TotalPremium, ExtraCosts, Hst, TotalCost, MonthlyPayment, FirstPaymentDate]
    SavePolicyData('PolicyData.dat', PolicyData)

    # Increment policy number
    NextPolicyNumber += 1

    # Ask if the user wants to enter another customer
    AnotherCustomer = input("Do you want to enter another customer? (Y/N): ").upper()
    if AnotherCustomer != 'Y':
        break