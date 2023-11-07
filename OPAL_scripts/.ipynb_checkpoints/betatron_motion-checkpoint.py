{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "45046be8-fd24-4f69-8dca-ff78e35e8aae",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "from scipy.integrate import solve_ivp\n",
    "import scipy.constants as SI\n",
    "\n",
    "re = SI.physical_constants['classical electron radius'][0]\n",
    "\n",
    "# Calculate acceleration and change in gamma\n",
    "def oscillator(t, x, A, B, C, D):\n",
    "    # x= [x,v_x, gamma]\n",
    "    v_x = x[1]\n",
    "    gamma = x[2]\n",
    "    a_x = -(C/gamma + A)*v_x - B/gamma*x[0]\n",
    "    d_gamma = C - D*gamma**2*x[0]**2\n",
    "    return np.array([v_x, a_x, d_gamma])\n",
    "\n",
    "# Assume x0 etc is a vector containing appropriate value for each particle\n",
    "def evolve_betatron_motion(x0, ux0, L, gamma, kp):   \n",
    "    # Constants\n",
    "    omega_p = SI.c * kp\n",
    "    n_0 = omega_p**2 * SI.m_e * SI.epsilon_0 / SI.e**2\n",
    "    E0 = 96e9* np.sqrt(n0/1e24) #V/m\n",
    "    Ez = 6.4e9 # V/m\n",
    "\n",
    "    #Plasma constants\n",
    "    tau_r = 2*re/3/SI.c\n",
    "    K = kp/ np.sqrt(2)\n",
    "\n",
    "    A = tau_r * SI.c**2 * K**2\n",
    "    B = SI.c**2 * K**2\n",
    "    C = wp*Ez/E0\n",
    "    D = tau_r * SI.c**2 * K**4\n",
    "\n",
    "    beta_matched = np.sqrt(2*gamma)/kp\n",
    "    lambda_beta = 2*np.pi*beta_matched\n",
    "\n",
    "    #Find the appropriate ammount of steps to resolve each oscillation\n",
    "    T = L/SI.c\n",
    "    n_per_beta = 100\n",
    "    n = round(L_plasma/lambda_beta * n_per_beta)\n",
    "    t, dt = np.linspace(0,T,n, retstep = True)\n",
    "    \n",
    "    lenght = len(x0)\n",
    "\n",
    "    #Vectors to store final x position, gamma factor, and momentum for each particle\n",
    "    xs = np.zeros(length)\n",
    "    gammas = np.zeros(length)\n",
    "    uxs = np.zeros(length)\n",
    "    \n",
    "    for x_, vx, gamma_ in zip(x0, ux0, gamma0):\n",
    "        # Find initial velocity\n",
    "        x_dot0 = vx * SI.c / gamma0\n",
    "        # Initial values\n",
    "        sysinit = np.array([x_, x_dot0, gamma])\n",
    "        # Solve the radiation reaction eqaution of motion\n",
    "        solution = solve_ivp(fun = oscillator, y0 = sysinit, method='RK45', \\\n",
    "                             t_span = (0,T), t_eval = t, args = (A, B, C, D))\n",
    "    \n",
    "        x_ = solution.y[0, -1]\n",
    "        xs[i] = x_\n",
    "        \n",
    "        vx = solution.y[1, -1]\n",
    "        \n",
    "        gamma_ = solution.y[2, -1]\n",
    "        gammas[i] = gamma_\n",
    "        \n",
    "        ux_ = vx * gamma / SI.c\n",
    "        uxs[i] = ux_\n",
    "        \n",
    "\n",
    "    return xs, uxs, gammas"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e43e3f88-5ba4-493f-a99f-73ea09b8a085",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
