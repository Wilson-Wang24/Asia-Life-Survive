"""Estimate monthly take-home pay from official average gross wages (single, no dependants)."""


def brackets(x, table):
    tax, low = 0.0, 0.0
    for top, rate in table:
        if x <= low:
            break
        tax += (min(x, top) - low) * rate
        low = top
    return tax


INF = float('inf')


def taiwan(annual):  # 2024 tax year rules
    monthly_regular = annual / 13.5
    labour = 0.025 * min(monthly_regular, 45800) * 12
    health = 0.0517 * 0.30 * monthly_regular * 12
    taxable = max(0, annual - 97000 - 131000 - 218000)
    tax = brackets(taxable, [(590000, .05), (1330000, .12), (2660000, .20), (INF, .30)])
    return (annual - labour - health - tax) / 12


def korea(annual):
    m = annual / 12
    pension = 0.045 * min(m, 6170000) * 12
    health = 0.03545 * annual
    care = health * 0.1295
    employment = 0.009 * annual
    si = pension + health + care + employment
    ded = 12000000 + 0.05 * (annual - 45000000)
    taxable = annual - ded - 1500000 - pension - health - care - employment
    tax = brackets(taxable, [(14e6, .06), (50e6, .15), (88e6, .24), (INF, .35)])
    credit = min(715000 + (tax - 1.3e6) * .3, max(740000 - (annual - 33e6) * .008, 660000))
    tax = (tax - credit) * 1.1
    return (annual - si - tax) / 12


def china(monthly, hpf=0.07):
    si = monthly * (0.08 + 0.02 + 0.005 + hpf)
    taxable = max(0, (monthly - si - 5000) * 12)
    tax = brackets(taxable, [(36000, .03), (144000, .10), (300000, .20), (420000, .25), (INF, .30)])
    return monthly - si - tax / 12


def japan(annual):
    si = annual * (0.04955 + 0.0915 + 0.0055)
    eid = annual * 0.2 + 440000 if annual <= 8.5e6 else 1.95e6
    income = annual - eid
    basic = 680000 if income <= 4.89e6 else (630000 if income <= 6.55e6 else 580000)
    it = brackets(income - si - basic, [(1.95e6, .05), (3.3e6, .10), (6.95e6, .20), (9e6, .23), (INF, .33)]) * 1.021
    rt = (income - si - 430000) * 0.10 + 5000 - 2500
    return (annual - si - it - rt) / 12


def singapore(annual):
    cpf = 0.20 * min(annual, 7400 * 12)
    chargeable = annual - cpf - 1000
    tax = brackets(chargeable, [(20000, 0), (30000, .02), (40000, .035), (80000, .07), (120000, .115), (INF, .15)])
    return (annual - cpf - tax) / 12


def thailand(monthly):
    sso = min(monthly, 15000) * 0.05
    annual = monthly * 12
    taxable = annual - min(annual * .5, 100000) - 60000 - sso * 12
    tax = brackets(taxable, [(150000, 0), (300000, .05), (500000, .10), (INF, .15)])
    return monthly - sso - tax / 12


def san_francisco(annual):
    fed = brackets(annual - 15750, [(11925, .10), (48475, .12), (103350, .22), (197300, .24), (INF, .32)])
    fica = annual * 0.0765
    ca = brackets(annual - 5540, [(10756, .01), (25499, .02), (40245, .04), (55866, .06), (70606, .08), (360659, .093), (INF, .103)]) - 149
    sdi = annual * 0.012
    return (annual - fed - fica - ca - sdi) / 12


def sydney(annual):
    tax = brackets(annual, [(18200, 0), (45000, .16), (135000, .30), (190000, .37), (INF, .45)])
    return (annual - tax - annual * 0.02) / 12


rows = {
    'Taipei': (947000, taiwan(947000)),
    'Taichung': (673000, taiwan(673000)),
    'Kaohsiung': (687000, taiwan(687000)),
    'Seoul': (4765000 * 12, korea(4765000 * 12)),
    'Shanghai': (12577 * 12, china(12577)),
    'Beijing': (12117 * 12, china(12117)),
    'Chengdu': (8056 * 12, china(8056)),
    'Qingdao': (97736, china(97736 / 12)),
    'Singapore': (86376, singapore(86376)),
    'Tokyo': (6444000, japan(6444000)),
    'Bangkok': (21565 * 12, thailand(21565)),
    'San-Francisco': (48.19 * 2080, san_francisco(48.19 * 2080)),
    'Sydney': (2160 * 52, sydney(2160 * 52)),
}
for k, (g, n) in rows.items():
    print(f"{k:14s} gross/mo {g/12:12,.0f}  net/mo {n:12,.0f}  take-home {n/(g/12):.1%}")
