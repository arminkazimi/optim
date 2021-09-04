import pyomo.environ as pyo


class WindSolarOptimizer:
    def __init__(self, df, battery_max_capacity, battery_0, eps, solar_cost, wind_cost):
        self.df = df
        self.battery_max_capacity = battery_max_capacity
        self.battery_0 = battery_0
        self.eps = eps
        self.solar_cost = solar_cost
        self.wind_cost = wind_cost

    def optimizer(self):
        battery_max_capacity = 100
        battery_0 = 3
        eps = 0.02
        solar_cost = 3
        wind_cost = 3
        d = self.df.demand.values.tolist()
        # define variables
        model = pyo.ConcreteModel(name='365_days')
        model.wind = range(len(self.df.wind_power))
        model.solar = range(len(self.df.solar_power))
        model.battery_waste = range(len(self.df.battery))
        model.w = pyo.Var(model.wind, bounds=(0.0, None))
        model.s = pyo.Var(model.solar, bounds=(0.0, None))
        model.bw = pyo.Var(model.battery_waste, bounds=(None, None))
        # define obj func
        model.obj = pyo.Objective(expr=sum(self.solar_cost * model.s[index] for index in model.solar)
                                       + sum(self.wind_cost * model.w[index] for index in model.wind)
                                       + sum(self.eps * model.bw[index] for index in model.battery_waste),
                                  sense=pyo.minimize)
        # define constraints
        model.cover_the_demands = pyo.ConstraintList()
        model.battery_less_than_max_cap = pyo.ConstraintList()
        for index, value in self.df.iterrows():
            model.cover_the_demands.add(sum(model.s[i] + model.w[i] for i in range(index + 1)) + self.battery_0 >= sum(
                d[i] for i in range(index + 1)))
            model.cover_the_demands.add(
                sum(model.s[i] + model.w[i] - d[i] for i in range(index + 1)) + self.battery_0 <= self.battery_max_capacity)
            model.cover_the_demands.add(model.s[index] <= value.solar_power)
            model.cover_the_demands.add(model.w[index] <= value.wind_power)
            model.cover_the_demands.add(
                model.bw[index] >= (model.s[index] + model.w[index] - d[index]) * ((self.solar_cost + self.wind_cost) / 2))
            model.cover_the_demands.add(model.bw[index] >= -(model.s[index] + model.w[index] - d[index]))
        results = pyo.SolverFactory('glpk').solve(model)
        # results.write()
        if results.solver.termination_condition == 'optimal':
            print(model.obj())
