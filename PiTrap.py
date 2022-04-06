'''
Computes an approximation of pi by calculating the area under the quarter circle
inscribed within the upper-right quadrant unit square using the trapzoid rule.

The ratio of the quarter-circle's area to the unit square area multiplied by 4
gives us our approximation of pi.

The more trapazoidal sections we use to calculate the quarter cirle area,
the closer our approximation should be to "real" pi.
'''
import math

def f(x):
    return math.sqrt(1 - (x * x))

def trap_area(a, b, half_section):
    return (a + b) * half_section

def pi_trap(n_sections):
    section_width = 1.0 / float(n_sections)
    section_half_width = section_width / 2.0
    y_vals = [f(float(i) * section_width) for i in range(n_sections)]
    t_areas = [trap_area(y_vals[i-1], y2, section_half_width) for i, y2 in enumerate(y_vals[1:], 1)]
    area_sum = sum(t_areas)
    pi_approx = area_sum * 4.0
    return pi_approx

if __name__ == '__main__':

    for i in range(1, 7):
        n_sections = int(math.pow(10, i))
        pi_approx = pi_trap(n_sections)
        pi_diff = math.pi - pi_approx
        print(f"n_sections={n_sections:-7d} pi_approx={pi_approx:.10f} pi_diff={pi_diff:.4e}")
