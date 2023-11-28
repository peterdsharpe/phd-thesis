from common import *
from aerosandbox.tools.statistics import time_series_uncertainty_quantification as tsuq


def get_results(bootstrap_resample=False):

    def read(name):
        time, data = simple_read(name)

        while True:

            if bootstrap_resample:
                splits = np.random.rand(len(time) + 1) * len(time)  # "limit" bootstrapping
                splits[0] = 0
                splits[-1] = len(time)

                weights = np.diff(np.sort(splits))

                # indices = np.random.choice(len(time), size=len(time), replace=True)

                # time_sample = time[indices]
                # data_sample = data[indices]
                #
                # order = np.argsort(time_sample)
                # time_sample = time_sample[order]
                # data_sample = data_sample[order]

            else:
                # time_sample = time + np.random.normal(scale=np.mean(np.diff(time)), size=len(x))
                # data_sample = data
                weights = np.ones_like(time)

            interpolator = interpolate.UnivariateSpline(
                x=time,
                y=data,
                w=weights / tsuq.estimate_noise_standard_deviation(data),
                s=len(data),
            )

            testval = interpolator(np.median(time))
            if np.isnan(testval):
                print("Invalid spline! Trying again...")
            else:
                break

        # derivative_interpolator = interpolate.UnivariateSpline(
        #     x=np.trapz(time),
        #     y=np.diff(data) / np.diff(time),
        #     w=np.ones_like(np.diff(time)) / tsuq.estimate_noise_standard_deviation(np.diff(data) / np.diff(time)),
        #     s=len(data),
        # )

        derivative_interpolator = interpolator.derivative()

        return interpolator, derivative_interpolator

    voltage = read("voltage")[0]
    current = read("current")[0]
    airspeed, airspeed_derivative = read("airspeed")
    altitude, altitude_derivative = read("baro_alt")

    t = np.linspace(0, t_max - 0, 1000)
    dt = np.diff(t)[0]

    def f(x):
        # return x
        return ndimage.gaussian_filter(x, sigma=10 / dt)

    def fd(x):
        # return x
        return ndimage.gaussian_filter(x, sigma=4 / dt)

    opti = asb.Opti()

    mass_total = 9.4

    avionics_power = 5  # opti.variable(init_guess=4, lower_bound=0, upper_bound=20)

    mean_current = np.mean(f(current(t)))
    mean_airspeed = np.mean(f(airspeed(t)))

    propto_rpm = np.softmax(
        f(current(t)) / mean_current,
        1e-3,
        softness=0.01
    ) ** (1 / 3)

    propto_J = (f(airspeed(t)) / mean_airspeed) / propto_rpm

    ### Model 0
    # prop_eff_params = {
    #     "eff": opti.variable(init_guess=0.8, lower_bound=0, upper_bound=1),
    # }
    #
    # prop_efficiency = prop_eff_params["eff"]

    ### Model 1
    prop_eff_params = {
        "Jc" : opti.variable(
            init_guess=propto_J.mean(),
            lower_bound=propto_J.mean() - 3 * propto_J.std(),
            upper_bound=propto_J.mean() + 3 * propto_J.std()
        ),
        "Js" : opti.variable(
            init_guess=propto_J.std(),
            lower_bound=propto_J.std() / 20,
            upper_bound=propto_J.std() * 20
        ),
        "max": opti.variable(init_guess=0.8, lower_bound=0, upper_bound=1),
        "min": opti.variable(init_guess=0.5, lower_bound=0, upper_bound=1),
    }
    opti.subject_to(prop_eff_params["max"] > prop_eff_params["min"])

    prop_efficiency = np.blend(
        (
                (propto_J - prop_eff_params["Jc"]) / prop_eff_params["Js"]
        ),
        prop_eff_params["max"],
        prop_eff_params["min"]
    )

    ### Model 2
    # prop_eff_params = {
    #     "scale"        : opti.variable(init_guess=1, lower_bound=0, upper_bound=1),
    #     "J_pitch_speed": opti.variable(init_guess=2, lower_bound=0),
    #     "sharpness"    : opti.variable(init_guess=10, lower_bound=2, upper_bound=50),
    # }
    #
    # prop_efficiency = np.softmax(
    #     prop_eff_params["scale"] * (
    #             (propto_J / prop_eff_params["J_pitch_speed"]) -
    #             (propto_J / prop_eff_params["J_pitch_speed"]) ** prop_eff_params["sharpness"]
    #     ),
    #         -1,
    #     softness=0.1
    # )

    propulsion_air_power = prop_efficiency * (f(voltage(t)) * f(current(t)) - avionics_power)

    q = 0.5 * 1.225 * f(airspeed(t)) ** 2
    S = 1.499
    CL = mass_total * 9.81 / (q * S)

    CD_params = {
        "CD0"  : opti.variable(init_guess=0.07, lower_bound=0, upper_bound=1),
        "CLCD0": opti.variable(init_guess=0.5, lower_bound=0, upper_bound=1.5),
        "CD2"  : opti.variable(init_guess=0.05, lower_bound=0, upper_bound=10),
        "CD3"  : opti.variable(init_guess=0.05, lower_bound=0, upper_bound=10),
        "CD4"  : opti.variable(init_guess=0.05, lower_bound=0, upper_bound=10),
    }

    CD = (
            CD_params["CD0"]
            + CD_params["CD2"] * np.abs(CL - CD_params["CLCD0"]) ** 2
            + CD_params["CD3"] * np.abs(CL - CD_params["CLCD0"]) ** 3
            + CD_params["CD4"] * np.abs(CL - CD_params["CLCD0"]) ** 4
    )

    drag_power = CD * q * S * f(airspeed(t))

    residuals = (
            propulsion_air_power
            - drag_power
            - mass_total * f(airspeed(t)) * fd(airspeed_derivative(t))
            - mass_total * 9.81 * fd(altitude_derivative(t))
    )

    ##### Objective

    ### L2-norm
    opti.minimize(
        np.mean(residuals ** 2)
    )

    # ### L1-norm
    # abs_residual = opti.variable(init_guess=0, n_vars=np.length(residuals))
    # opti.subject_to([
    #     abs_residual >= residuals,
    #     abs_residual >= -residuals,
    # ])
    # opti.minimize(np.mean(abs_residual))

    ##### Solve

    sol = opti.solve(
        verbose=False
    )

    ##### Post-Process, Print
    # print("\nMean Absolute Error:", np.mean(np.abs(sol(residuals))), "W")
    CD_params = sol(CD_params)
    prop_eff_params = sol(prop_eff_params)

    for k, v in CD_params.items():
        CD_params[k] = np.maximum(0, v)

    from pprint import pprint

    # print("-" * 50)
    # for var in [
    #     "avionics_power",
    #     "prop_eff_params",
    #     "CD_params",
    # ]:
    #     print(var)
    #     pprint(sol(eval(var)))

    ########## Reconstruct Steady-State Solution

    mean_propto_J = np.mean(propto_J)

    def steady_state_CD(CL):
        return (
                CD_params["CD0"]
                + CD_params["CD2"] * np.abs(CL - CD_params["CLCD0"]) ** 2
                + CD_params["CD3"] * np.abs(CL - CD_params["CLCD0"]) ** 3
                + CD_params["CD4"] * np.abs(CL - CD_params["CLCD0"]) ** 4
        )

    def steady_state_prop_efficiency(propto_J):
        # return prop_eff_params["eff"] * np.ones_like(propto_J)

        return np.blend(
            (
                    (propto_J - prop_eff_params["Jc"]) / prop_eff_params["Js"]
            ),
            prop_eff_params["max"],
            prop_eff_params["min"]
        )

        # return np.softmax(
        #     prop_eff_params["scale"] * (
        #             (propto_J / prop_eff_params["J_pitch_speed"]) -
        #             (propto_J / prop_eff_params["J_pitch_speed"]) ** prop_eff_params["sharpness"]
        #     ),
        #     -1,
        #     softness=0.1
        # )

    def steady_state_required_electrical_power(airspeed):
        q = 0.5 * 1.225 * airspeed ** 2
        CL = mass_total * 9.81 / (q * S)
        CD = steady_state_CD(CL)

        drag_power = CD * q * S * airspeed

        opti2 = asb.Opti()
        propto_J = opti2.variable(init_guess=mean_propto_J, n_vars=len(airspeed))

        prop_efficiency = steady_state_prop_efficiency(propto_J)

        required_current = drag_power / (voltage(t).mean() * prop_efficiency)
        required_propto_rpm = np.softmax(
            required_current / mean_current,
            1e-3,
            softness=0.01
        ) ** (1 / 3)
        required_propto_J = (airspeed / mean_airspeed) / required_propto_rpm

        opti2.subject_to(
            propto_J == required_propto_J
        )

        sol2 = opti2.solve(
            verbose=False
        )

        return sol2(
            drag_power / prop_efficiency + avionics_power
        )

    return sol(locals())


if __name__ == '__main__':
    res = get_results(
        True
    )
