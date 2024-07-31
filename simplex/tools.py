def is_entier (num, tolerance=1e-6):
    rounded_num = round(num)
    if abs(num - rounded_num) < tolerance:
        return True 
    return False