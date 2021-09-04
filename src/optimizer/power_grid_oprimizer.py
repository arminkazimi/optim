import pulp as pl



class PowerGridOptimizer:
    def __init__(self, df, problem_data):
        self.df = df
        self.problem_data = problem_data

    def optimizer(self):

        d = self.df.demand.values.tolist()
        problem2 = pl.LpProblem("power_bill", pl.LpMinimize)
        x = dict()
        var_b = dict()
        abs_vars = dict()

        # Define variables
        for index, value in self.df.iterrows():
            x[f'x{index}'] = pl.LpVariable(f'x{index}', lowBound=0)
            # var_b[f'b{index}'] = pl.LpVariable(f'b{index}')
            abs_vars[f'abs{index}'] = pl.LpVariable(f'abs{index}')
        off = pl.LpVariable('off', lowBound=0)
        on = pl.LpVariable('on', lowBound=0)
        semi = pl.LpVariable('semi', lowBound=0)
        # max0 = pl.LpVariable('max',lowBound=0)
        max1 = pl.LpVariable('max1', lowBound=0)

        #  Define Objective function
        problem2 += (pl.lpSum(value.cost * x[f'x{index}'] for index, value in self.df.iterrows())
                     + pl.lpSum(self.problem_data['eps'] * abs_vars[f'abs{index}'] for index, value in self.df.iterrows())
                     + off * self.problem_data['off_pick_price']
                     + on * self.problem_data['on_pick_price']
                     + semi * self.problem_data['semi_pick_price']
                     + (max1 - self.problem_data['max0']) * self.problem_data['max_pick_price']
                     )

        #  Define Constraints
        for index, value in self.df.iterrows():

            problem2 += (max1 >= x[f'x{index}'])
            if value.pick == 'off':
                problem2 += (off >= x[f'x{index}'])
            if value.pick == 'on':
                problem2 += (on >= x[f'x{index}'])
            if value.pick == 'semi':
                problem2 += (semi >= x[f'x{index}'])

            problem2 += (pl.lpSum(x[f'x{i}'] for i in range(index + 1)) + self.problem_data['b0'] >= pl.lpSum(
                d[i] for i in range(index + 1)))
            problem2 += (pl.lpSum(x[f'x{i}'] - d[i] for i in range(index + 1)) + self.problem_data['b0'] <= self.problem_data['b_max'])
            problem2 += x[f'x{index}'] - d[index] <= self.problem_data['b_power']
            problem2 += d[index] - x[f'x{index}'] <= self.problem_data['b_power']

            problem2 += abs_vars[f'abs{index}'] >= (x[f'x{index}'] - d[index]) * value.cost
            problem2 += abs_vars[f'abs{index}'] >= -(x[f'x{index}'] - d[index])

        solution = problem2.solve()
        print(str(pl.LpStatus[solution]))
        # print(problem2)
        # print('Answer: ')
        xList = list()
        xDict = dict()
        batteryList = list()
        for item, value in self.df.iterrows():
            # print(abs_vars[f'abs{item}'],': ',abs_vars[f'abs{item}'].varValue)
            # print(x[f'x{item}'],': ',x[f'x{item}'].varValue)
            xDict[f'x{item}'] = x[f'x{item}'].varValue
            xList.append(x[f'x{item}'].varValue)
            batteryList.append(xList[item] - d[item])
        xDict['x'] = xList
        xDict['off'] = off.varValue
        xDict['on'] = on.varValue
        xDict['semi'] = semi.varValue
        xDict['max1'] = max1.varValue
        xDict['opt'] = problem2.objective.value()
        xDict['battery'] = batteryList
        # print(off,': ',off.varValue)
        # print(on,': ',on.varValue)
        # print(semi,': ',semi.varValue)
        # print(max1,': ',max1.varValue)
        # print('OPt = ', problem2.objective.value(),'$')
        # print('\n')
        return xDict
