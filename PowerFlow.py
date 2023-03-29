import numpy as np
import System as System

# TEMPORARY BUS DATA
# Bus 1: Slack Bus -  𝑉=1.0 pu, 𝛿=0^∘
# Bus 2: 𝑃_𝐿=0, 𝑄_𝐿=0
# Bus 3:𝑃_𝐿=110 "MW", 𝑄_𝐿=50" Mvar"
# Bus 4: 𝑃_𝐿=100" MW", 𝑄_𝐿=70" Mvar"
# Bus 5: 𝑃_𝐿=100" MW",𝑄_𝐿=65" Mvar"
# Bus 6: 𝑃_𝐿=0 "MW", 𝑄_𝐿=0" Mvar"
# Bus 7:𝑃_𝐺=200 "MW", 𝑉=1.0,  𝑃_𝐿=0, 〖 𝑄〗_𝐿=0
# p_given[0] = 0


class PowerFlow:

    def __init__(self, System):
        self.p_arr = []
        self.q_arr = []

        # set given values
        p_given = np.zeros(len(System.buses))
        q_given = np.zeros(len(System.buses))

        # find slack & voltage controlled buses
        self.swing_bus = None
        for k in range(len(System.buses)):
            if System.buses["Bus" + str(k + 1)].bus_type == "Swing Bus":
                self.swing_bus = k
            if System.buses["Bus" + str(k + 1)].bus_type == "Voltage Controlled Bus":
                self.voltage_controlled_bus = k
                break

        # Power mismatch

        # flat start
        V = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        delta = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # Array for P and Q
        p_arr = np.zeros(len(System.buses))
        q_arr = np.zeros(len(System.buses))

        # calculate mismatch, ignoring the slack bus

        for k in range(len(System.buses)):
            # if slack bus, skip
            if k == self.swing_bus:
                continue

            for n in range(len(System.buses)):
                p_arr[k] += V[k] * V[n] * abs(System.y_matrix_new[k, n]) * np.cos(delta[k] - delta[n] - np.angle(System.y_matrix_new[k, n]))
                if k == self.voltage_controlled_bus:
                    continue
                q_arr[k] += V[k] * V[n] * abs(System.y_matrix_new[k, n]) * np.sin(delta[k] - delta[n] - np.angle(System.y_matrix_new[k, n]))

        # P excluding slack bus
        p_mis = p_given - p_arr
        p_mis = p_mis[1:7]


        # Q excluding slack bus and VCB
        q_mis = q_given - q_arr
        q_mis = q_mis[1:6]
        
        # Calculate Jacobian Matrix
        j1 = np.zeros((len(System.buses) - 1, len(System.buses) - 1))
        j2 = np.zeros((len(System.buses) - 1, len(System.buses) - 1))
        j3 = np.zeros((len(System.buses) - 1, len(System.buses) - 1))
        j4 = np.zeros((len(System.buses) - 1, len(System.buses) - 1))

        skip = 0

        for k in range(len(System.buses)):
            # if slack bus skip
            if k == self.swing_bus:
                skip = 1
                continue
            for n in range(len(System.buses)):
                if k == n:
                    for z in range(len(System.buses)):
                        j2[k-skip, n-skip] += abs(System.y_matrix_new[k, z]) * V[z] * np.cos(delta[k] - delta[z] - np.angle(System.y_matrix_new[k, z]))
                        j4[k-skip, n-skip] += abs(System.y_matrix_new[k, z]) * V[z] * np.sin(delta[k] - delta[z] - np.angle(System.y_matrix_new[k, z]))

                        if z == k:
                            continue

                        j1[k-skip, n-skip] += abs(System.y_matrix_new[k, z]) * V[z] * np.sin(delta[k] - delta[z] - np.angle(System.y_matrix_new[k, z]))
                        j3[k-skip, n-skip] += abs(System.y_matrix_new[k, z]) * V[z] * np.cos(delta[k] - delta[z] - np.angle(System.y_matrix_new[k, z]))

                    # Fixing negative difference in k == n Jacobian
                    j1[k-skip, n-skip] = -j1[k-skip, n-skip] * V[k]
                    j2[k-skip, n-skip] = j2[k-skip, n-skip] + (V[k] * abs(System.y_matrix_new[k, n]) * np.cos(np.angle(System.y_matrix_new[k, n])))
                    j3[k-skip, n-skip] = (j3[k-skip, n-skip] * V[k])
                    j4[k-skip, n-skip] = j4[k-skip, n-skip] - (V[k] * abs(System.y_matrix_new[k, n]) * np.sin(np.angle(System.y_matrix_new[k, n])))

                else:
                    j1[k-skip, n-skip] = V[k] * abs(System.y_matrix_new[k, n]) * V[n] * np.sin(delta[k] - delta[n] - np.angle(System.y_matrix_new[k, n]))
                    j2[k-skip, n-skip] = V[k] * abs(System.y_matrix_new[k, n]) * np.cos(delta[k] - delta[n] - np.angle(System.y_matrix_new[k, n]))
                    j3[k-skip, n-skip] = -V[k] * abs(System.y_matrix_new[k, n]) * V[n] * np.cos(delta[k] - delta[n] - np.angle(System.y_matrix_new[k, n]))
                    j4[k-skip, n-skip] = V[k] * abs(System.y_matrix_new[k, n]) * np.sin(delta[k] - delta[n] - np.angle(System.y_matrix_new[k, n]))

        # Combine Jacobian
        J = np.block([[j1, j2], [j3, j4]])

        # Delete slack bus 1 or 7, here if it is 1
        J_temp = np.delete(J, 11, 1)
        J = J_temp
        J_temp = np.delete(J, 11, 0)
        J = J_temp

        print("Jacobian Matrix")
        i = 0
        while i < len(J):
            j = 0
            print("\nRow " + str(i + 1))
            while j < len(J):
                print(J[i][j])
                j += 1
            i = i + 1

        # calculate change in voltage and phase angle
        J_inv = np.linalg.inv(J)



