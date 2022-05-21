from math import log

from fastapi import APIRouter

from dto.v1.credit_model import CreditData

router = APIRouter()


@router.post('/check_credit_available', description='Check credit')
async def check_credit(request: CreditData):
    if request.age >= 65 and request.gender == 'М' or request.age >= 60 and request.gender == 'Ж' or \
            request.credit_sum / request.maturity > request.income_last_year or \
            request.credit_rate == -2 or \
            request.credit_rate == 'безработный' or \
            year_pay(request) > request.income_last_year:
        return dict(result='Кредит не одобрен')
    else:
        return dict(result='Кредит одобрен', sum=year_pay(request))


def year_pay(req):
    pay_sum = req.credit_sum * (1 + req.maturity * (
        percent(req.goal, req.credit_rate, req.credit_sum, req.source_income))) / req.maturity
    return pay_sum


def percent(type, rating, sum, income_type):
    base_percent = 10
    if type == 'ипотека':
        base_percent -= 2
    elif type == 'развитие бизнеса':
        base_percent -= 0.5
    elif type == 'потребительский':
        base_percent += 1.5

    if rating == -1:
        base_percent += 1.5
    elif rating == 1:
        base_percent -= 0.25
    elif rating == 2:
        base_percent -= 0.75

    if income_type == 'пассивный доход':
        base_percent += 0.5
    if income_type == 'наёмный работник':
        base_percent -= 0.25
    if income_type == 'собственный бизнес':
        base_percent += 0.25

    base_percent += -log(sum)

    return base_percent/100
