"""
Post-process wrdata output of switching_loss_double_pulse to extract E_on/E_off
by numerically integrating v(sw)*i_sw over the two switching transitions, and
compare against the textbook's ideal linear-ramp formula (eq3.8/eq3.9, rei3.2).

wrdata columns (pairs of time,value repeated because ngspice wrdata writes
"t val t val t val ..." for each requested vector):
  0,1: v(sw)   2,3: v(vtop)   4,5: v(gate)   6,7: i(l1)   8,9: @d1[id]
"""
import os
import numpy as np

data = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dpt_switching_loss.txt"))
t = data[:, 0]
vsw = data[:, 1]
vgate = data[:, 5]
il1 = data[:, 7]
id1 = data[:, 9]

isw = il1 - id1  # KCL at "sw" node: switch current = inductor current - freewheel diode current

def transition_span(t0, t1, label):
    mask = (t >= t0) & (t <= t1)
    tw, vw = t[mask], vsw[mask]
    vlo, vhi = vw.min(), vw.max()
    thresh_lo = vlo + 0.1 * (vhi - vlo)
    thresh_hi = vlo + 0.9 * (vhi - vlo)
    print(f"{label}: v(sw) range in window = [{vlo:.3f},{vhi:.3f}]V, n_samples={mask.sum()}")
    return mask

def integrate_window(t0, t1, label):
    mask = (t >= t0) & (t <= t1)
    tw = t[mask]
    p = vsw[mask] * isw[mask]
    e = np.trapezoid(p, tw)
    imax, imin = isw[mask].max(), isw[mask].min()
    print(f"{label}: window [{t0*1e9:.2f}ns,{t1*1e9:.2f}ns] n={mask.sum()} E={e*1e6:.3f} uJ, I_sw range=[{imin:.3f},{imax:.3f}]A")
    return e

print("=== Turn-off transition (end of pulse 1, t~5150-5200ns) — full resolution dump ===")
mask = (t >= 5.148e-6) & (t <= 5.152e-6)
for i in np.where(mask)[0]:
    print(f"  t={t[i]*1e9:9.4f}ns v(sw)={vsw[i]:9.4f} i(l1)={il1[i]:9.4f} i(d1)={id1[i]:9.4f} i(sw)={isw[i]:9.4f}")

print()
print("=== Energies (wide window to capture full transient ringing) ===")
e_off = integrate_window(5.10e-6, 5.30e-6, "E_off (pulse1 turn-off)")
e_on = integrate_window(6.20e-6, 6.40e-6, "E_on (pulse2 turn-on)")

print()
print(f"Simulated E_on={e_on*1e6:.3f} uJ, E_off={e_off*1e6:.3f} uJ, sum={(e_on+e_off)*1e6:.3f} uJ")

V, I, ton_ideal = 100.0, 10.0, 50e-9
e_ideal = 0.5 * V * I * ton_ideal
print(f"Ideal (eq3.8/3.9, rei3.2 given t_on=t_off=50ns): E_on=E_off={e_ideal*1e6:.3f} uJ each, sum={2*e_ideal*1e6:.3f} uJ")

# Estimate the *actual* transition duration achieved in this sim (Coss-charge-limited,
# not gate-drive-limited) to explain why E differs from the idealized rei3.2 numbers.
C_oss = 470e-12
I_est = 10.1
dt_est = C_oss * 100.0 / I_est
e_coss_est = 0.5 * 100.0 * I_est * dt_est  # equals 0.5*C*V^2 exactly, sanity check below
print(f"\nCoss-limited estimate: dt=C*dV/I={dt_est*1e9:.3f}ns, 0.5*V*I*dt={e_coss_est*1e6:.3f}uJ, 0.5*C*V^2={0.5*C_oss*100.0**2*1e6:.3f}uJ (should match)")
