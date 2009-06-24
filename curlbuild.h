#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_curlbuild32_h}"
#elif __WORDSIZE == 64
#include "%{_curlbuild64_h}"
#else
#error "Unknown word size"
#endif
