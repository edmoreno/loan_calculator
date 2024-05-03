import math
import argparse
import sys


# figure out which argument is missing
def determine_misssing_argument(args):
    if args.payment is None and args.type == 'annuity':
        return "payment"
    elif args.principal is None:
        return "principal"
    elif args.periods is None:
        return "periods"
    elif args.type == 'diff':
        return "diff_payment"


# based on which argument is missing, calculate it using the other arguments
def calculate_payment(args):
    principal = args.principal
    # convert annual interest rate to decimal form (div by 100) and then to monthly rate (div by 12)
    monthly_interest = args.interest / 100 / 12
    numerator = monthly_interest * ((1 + monthly_interest) ** args.periods)
    denominator = ((1 + monthly_interest) ** args.periods) - 1
    return principal * (numerator / denominator)


def calculate_principal(args):
    numerator = args.payment
    # convert annual interest rate to decimal form (div by 100) and then to monthly rate (div by 12)
    monthly_interest = args.interest / 100 / 12
    denom_numerator = monthly_interest * ((1 + monthly_interest) ** args.periods)
    denom_denominator = ((1 + monthly_interest) ** args.periods) - 1
    denominator = denom_numerator / denom_denominator
    return round(numerator / denominator)


def calculate_periods(args):
    numerator = args.payment
    # convert annual interest rate to decimal form (div by 100) and then to monthly rate (div by 12)
    monthly_interest = args.interest / 100 / 12
    denominator = args.payment - (monthly_interest * args.principal)
    months = math.log((numerator / denominator), 1 + monthly_interest)
    return math.ceil(months)

def calculate_diff_payment(args):
    p = args.principal
    n = args.periods
    i = args.interest / 100 / 12

    diff_payments = list()
    for m in range(1, n + 1):
        d_m = (p / n) + (i * (p - ((p * (m - 1)) / n)))
        diff_payments.append(math.ceil(d_m))

    return diff_payments


def check_args(args):
    if args.type not in ["annuity", "diff"]:
        return True
    elif args.type == "diff" and args.payment is not None:
        return True
    elif args.interest is None:
        return True
    elif len(sys.argv) < 5:
        return True
    elif args.principal is not None and float(args.principal) < 0:
        return True
    elif args.payment is not None and float(args.payment) < 0:
        return True
    elif args.periods is not None and int(args.periods) < 0:
        return True
    elif args.interest is not None and float(args.interest) < 0:
        return True
    else:
        return False


def main():
    # set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--payment", type=float)
    parser.add_argument("--principal", type=float)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)
    parser.add_argument("--type", type=str)

    args = parser.parse_args()
    if check_args(args):
        print("Incorrect parameters")
        return 0

    match determine_misssing_argument(args):
        case "payment":
            payment = math.ceil(calculate_payment(args))
            total_paid = args.periods * payment
            overpayment = math.ceil(total_paid - args.principal)
            print(f"Your monthly payment = {payment}!")
            print(f"Overpayment: {overpayment}")
        case "principal":
            principal = calculate_principal(args)
            total_paid = args.payment * args.periods
            overpayment = math.ceil(total_paid - principal)
            print(f"Your loan principal = {principal}!")
            print(f"Overpayment: {overpayment}")
        case "periods":
            total_months = calculate_periods(args)
            # convert total months to year value and if remainder, remaining months
            years = total_months // 12
            remaining_months = total_months % 12
            total_paid = args.payment * total_months
            overpayment = math.ceil(total_paid - args.principal)
            print(f"It will take {years} years and {remaining_months} months to repay this loan!")
            print(f"Overpayment: {overpayment}")
        case "diff_payment":
            monthly_payments = calculate_diff_payment(args)
            total_paid = sum(monthly_payments)
            overpayment = math.ceil(total_paid - args.principal)
            for i, value in enumerate(monthly_payments):
                print(f"Month {i + 1}: payment is {value}")
            print(f"Overpayment: {overpayment}")


if __name__ == "__main__":
    main()
