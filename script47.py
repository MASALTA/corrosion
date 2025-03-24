import math

# Constants
O2 = 7.0  # mg/L
Ea = 64170  # J/mol
R = 8.314  # J/mol•K

def compute_thickness_per_year(T_max, k_value):
    delta_T = 0.15 * T_max  # Adjusting delta_T based on T_max
    T_min = T_max - delta_T
    T_average_kelvin = ((T_max + T_min) / 2) + 273.15  # Convert average temperature from Celsius to Kelvin
    rate_term = T_max * T_min / (T_max + T_min)
    ln_rate_term = math.log(rate_term) if rate_term > 0 else 0  # Use the natural logarithm of rate term
    rate = k_value * O2 * math.exp(-Ea / (R * T_average_kelvin)) * ln_rate_term
    
    # Convert to mm/year
    density = 7.99  # g/cm^3 for 316L stainless steel (average value)
    molar_mass = 55.845  # g/mol for iron
    valence = 2
    faraday_const = 96485  # C/mol
    return rate * molar_mass * 60 * 24 * 365.25 / (density * valence * faraday_const)

# Observed data
temperatures_max = [200, 300, 800, 897, 983]
observed_rates = [0.02, 0.03, 3.07, 6.73, 11.03]

# Initial k_value
k_values = [1, 10, 100, 1000, 10000, 100000]

best_fit_k = 0
smallest_difference = float("inf")

for k_value in k_values:
    computed_rates = [compute_thickness_per_year(T_max, k_value) for T_max in temperatures_max]
    differences = [abs(computed_rate - observed_rate) for computed_rate, observed_rate in zip(computed_rates, observed_rates)]
    
    if sum(differences) < smallest_difference:
        smallest_difference = sum(differences)
        best_fit_k = k_value

print(f"The best fit k value is: {best_fit_k}")
print("Comparing the computed rates with the observed rates:")
computed_rates = [compute_thickness_per_year(T_max, best_fit_k) for T_max in temperatures_max]
for i, T_max in enumerate(temperatures_max):
    print(f"Temperature: {T_max}°C, Computed rate: {computed_rates[i]:.2f} mm/year, Observed rate: {observed_rates[i]} mm/year")

