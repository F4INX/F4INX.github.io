import numpy as np
import skrf as rf
import matplotlib.pyplot as plt

# Branchline coupler schematic
#
#                    --------
# Port 1 --------+--|   Z1   |--+-------- Port 2
#                |   --------   |
#              ----            ----
#             |    |          |    |
#             | Z2 |          | Z2 |
#             |    |          |    |
#             |    |          |    |
#              ----            ----
#                |   --------   |
# Port 4 --------+--|   Z2   |--+-------- Port 3
#                    --------

# Define the frequency range
freq = rf.Frequency(start=0, stop=2, npoints=1001, unit='GHz')

# Characteristic impedance of ports
z0_ports = 50

# Calculate impedance and propagation constant for branch lines
z0_main = z0_ports / np.sqrt(2)
z0_branches = z0_ports
beta = freq.w / rf.c
line_branches = rf.media.DefinedGammaZ0(frequency=freq, z0=z0_branches, gamma=0 + beta * 1j)
line_main = rf.media.DefinedGammaZ0(frequency=freq, z0=z0_main, gamma=0 + beta * 1j)

# Electrical length for 90 degrees at 1 GHz
d = line_branches.theta_2_d(90, deg=True)  # @ 90°(lambda/4)@ 1 GHz is ~ 75 mm

# Create the branch lines and main lines
branch1 = line_branches.line(d, unit='m', name='branch1')
branch2 = line_branches.line(d, unit='m', name='branch2')
main1 = line_main.line(d, unit='m', name='main1')
main2 = line_main.line(d, unit='m', name='main2')

# Create the ports
port1 = rf.Circuit.Port(freq, name='port1')
port2 = rf.Circuit.Port(freq, name='port2')
port3 = rf.Circuit.Port(freq, name='port3')
port4 = rf.Circuit.Port(freq, name='port4')

# Create the branchline coupler network with the defined connections
# Note that the order of appearance of the port in the setup is important
connections = [
    [(port1, 0),   (main1, 0),   (branch1, 0)],
    [(port2, 0),   (main1, 1),   (branch2, 0)],
    [(port3, 0),   (main2, 1),   (branch2, 1)],
    [(port4, 0),   (main2, 0),   (branch1, 1)]
]

# Create the network from the connections
network = rf.Circuit(connections).network

# Renormalize the ports to 50 Ohms
network.renormalize(50)

# Plot the S-parameters
network.plot_s_db(m=0, n=1, label='S21')
network.plot_s_db(m=0, n=2, label='S31')
network.plot_s_db(m=0, n=3, label='S41')
network.plot_s_db(m=0, n=0, label='S11')

plt.ylim(-20, 0)
plt.title('Branchline Coupler S-Parameters')
plt.legend()
plt.show()

# Export the S-parameters to an S4P file
network.frequency.unit = 'Hz'
network.write_touchstone('branchline_coupler.s4p')
