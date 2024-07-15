now_population = 312032486
sec_per_year = 365 * 24 * 60 * 60

birth_per_year = sec_per_year // 7
death_per_year = sec_per_year // 13
immigrant_per_year = sec_per_year // 45

for year in range(1,6):
    population_change_per_year = birth_per_year - death_per_year + immigrant_per_year
    now_population += population_change_per_year
    print(f"Year {year}: Population is {now_population}")