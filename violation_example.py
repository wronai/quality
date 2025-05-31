"""
This is an example Python script that intentionally violates SPYQ quality rules.
It's designed to demonstrate SPYQ's validation capabilities.
"""

# This function has too many parameters (violates max_function_params: 4)
def process_data(data1, data2, data3, data4, data5, data6, data7, data8):
    """This function has too many parameters."""
    # This function body is too long (violates max_function_lines: 50)
    result = 0
    for i in range(100):
        # Deeply nested block (violates max_nesting_depth: 4)
        try:
            if i % 2 == 0:
                for j in range(10):
                    if j > 5:
                        while True:
                            if i + j > 50:
                                for k in range(5):
                                    result += i * j * k  # 5 levels deep
            else:
                for j in range(5):
                    if j % 2 == 0:
                        result += j
        except Exception:  # Bare except (violates forbid_bare_except: true)
            pass
    
    # Many more lines to exceed max_function_lines
    print("Processing data...")  # Print statement (violates forbid_print_statements: true)
    print("More processing...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("And more...")
    print("Processing complete!")
    return result

# Global variable (violates forbid_global_vars: true)
global_var = "This is a global variable"

# Function without type hints (violates require_type_hints: true)
def another_function():
    # Function without docstring (violates require_docstrings: true)
    x = 10
    y = 20
    return x + y

# Class with too many methods (to increase file size)
class ExampleClass:
    def __init__(self):
        self.value = 0
    
    def method1(self):
        pass
        
    def method2(self):
        pass
        
    def method3(self):
        pass
        
    def method4(self):
        pass
        
    def method5(self):
        pass
        
    def method6(self):
        pass
        
    def method7(self):
        pass
        
    def method8(self):
        pass
        
    def method9(self):
        pass
        
    def method10(self):
        pass

# More functions to increase file size
def helper1():
    pass

def helper2():
    pass

def helper3():
    pass

def helper4():
    pass

def helper5():
    pass

# Main execution
if __name__ == "__main__":
    # Call the function with too many parameters
    process_data(1, 2, 3, 4, 5, 6, 7, 8)
    
    # Use the global variable
    print(global_var)
    
    # Call the function without type hints
    result = another_function()
    print(f"Result: {result}")
    
    # Create an instance of the class
    example = ExampleClass()
    example.method1()
    
    print("Script execution completed.")
