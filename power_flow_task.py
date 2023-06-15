import numpy as np
from pypower.api import runpf, ppoption

def main():
    """
    Solves a power flow problem for a system with 4 buses using the Newton-Raphson method.
    The system consists of PQ and PV buses, with specified bus types, real power injections, and voltage magnitudes.
    """

    # Power base
    baseMVA = 100

    # Bus data
    # bus_i type Pd Qd Gs Bs area Vm Va baseKV zone Vmax Vmin
    bus = np.array([
        [1, 1, 1, 0, 0, 0, 1, 1.0, 0, 230, 1, 1.1, 0.9],  # Bus 1: PQ bus with a voltage magnitude of 1.0 pu
        [2, 2, 0, 0, 0, 0, 1, 1.1, 0, 230, 1, 1.1, 0.9],  # Bus 2: PV bus with a voltage magnitude of 1.1 pu
        [3, 2, 0, 0, 0, 0, 1, 1.05, 0, 230, 1, 1.1, 0.9],  # Bus 3: PV bus with a voltage magnitude of 1.05 pu
        [4, 1, 2, 0, 0, 0, 1, 1, 0, 230, 1, 1.1, 0.9],  # Bus 4: PQ bus
    ])

    # Generator data
    # bus, Pg, Qg, Qmax, Qmin, Vg, mBase, status, Pmax, Pmin
    gen = np.array([
        [2, 2, 0, 100, -100, 1.1, baseMVA, 1, 2.5, -2.5],  # Generator at Bus 2 with a real power injection of 2 MW
        [3, 1, 0, 100, -100, 1.05, baseMVA, 1, 2.5, -2.5],  # Generator at Bus 3 with a real power injection of 1 MW
    ])

    # Branch data
    # fbus, tbus, r, x, b, rateA, rateB, rateC, ratio, angle, status
    branch = np.array([
        [1, 2, 0.02, 0.06, 0.03, 100, 100, 100, 0, 0, 1],  # Branch connecting Bus 1 and Bus 2
        [2, 3, 0.06, 0.18, 0.02, 100, 100, 100, 0, 0, 1],  # Branch connecting Bus 2 and Bus 3
        [3, 4, 0.01, 0.03, 0.01, 100, 100, 100, 0, 0, 1],  # Branch connecting Bus 3 and Bus 4
    ])

    # Create PYPOWER case dict
    ppc = {"version": '2', "baseMVA": baseMVA, "bus": bus, "gen": gen, "branch": branch}

    # Run power flow
    ppo = ppoption(OUT_ALL=0)
    result, success = runpf(ppc, ppo)

    # Print results
    if success:
        print('Power flow converged!\n')
        voltage_magnitudes = result['bus'][:, 7]
        voltage_angles = result['bus'][:, 8]
        
        for i in range(len(voltage_magnitudes)):
            print('Bus {}: Voltage magnitude = {:.4f} p.u., Voltage angle = {:.4f} degrees'.format(i+1, voltage_magnitudes[i], voltage_angles[i]))
    else:
        print('Power flow did not converge!')
if __name__ == "__main__":
    main()
