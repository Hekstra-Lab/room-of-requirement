# How to add function

Define your function in `methods.py` that accepts `X, y, bw` and returns a numpy array. Add the function name to `__all__`. Then run `python compare.py` to see results

# setting up cython
To build cython `python cython_setup.py build_ext --inplace`. Try not to push the resulting `.so` or `.pyd` files because its not clear how well they will translate across different setups.


# Results
On Ian's desktop:  
CPU - Ryzen 5 2600x  
GPU - RX 470 (N/A as it doesn't work with Jax)  

| function | Time (s) |
| ---------| -------- |
| numpy_for_loop |	19.675134225999955|
jax_map|	6.14440042199999
cython_Ofast_simple|	19.23067425199997
cython_Ofast_full|	13.728920615999868
cython_O3_simple|	18.733726350000097
cython_O3_full|	26.02228353600003

with `OFast` the results are wrong with a percent error of `~10e-5`
